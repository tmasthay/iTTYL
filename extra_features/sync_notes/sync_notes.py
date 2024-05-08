import glob
from pathlib import Path
from subprocess import check_output as co
import os
from datetime import datetime, timedelta
import re
import base64
from dotenv import dotenv_values
from fetch_icloud import download_share_link
import sys

# temporary hack -- refactor this later on
sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))
import extra_features.custom_times as ct

DEMARK = "*** SCHEDULED TEXT ***\n"
SCHEDULED_TEXTS_DIRECTORY = [
    e
    for e in open('SETTINGS.txt').read().split('\n')
    if e.startswith('SCHEDULED_TEXTS_DIRECTORY')
][0].split('=')[1]

PROJECT_PATH = os.path.abspath(
    os.path.relpath(os.path.dirname(__file__), os.getcwd())
)

f = open('/tmp/sync_notes.txt', 'a')
pr = lambda *args, **kwargs: print(*args, **kwargs, file=f, flush=True)

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)


def strip_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def str_to_timedelta(s, default='m'):
    s = s.lower()
    if 'd' not in s and 'h' not in s and 'm' not in s and 's' not in s:
        s = f'{s}{default}'
    if ':' in s:
        parts = s.split(':')
        if len(parts) == 3:  # days:hours:minutes
            days, hours, minutes = parts
            seconds = 0
        elif len(parts) == 4:  # days:hours:minutes:seconds
            days, hours, minutes, seconds = parts
        else:
            raise ValueError("Invalid time format")
        return timedelta(
            days=int(days),
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
        )
    else:
        day_idx, hour_idx, minute_idx, second_idx = (
            s.find('d'),
            s.find('h'),
            s.find('m'),
            s.find('s'),
        )
        pr(f'{s=}, {day_idx=}, {hour_idx=}, {minute_idx=}, {second_idx=}, {s=}')
        days = int(s[:day_idx]) if day_idx != -1 else 0
        hours = int(s[day_idx + 1 : hour_idx]) if hour_idx != -1 else 0
        minutes = int(s[hour_idx + 1 : minute_idx]) if minute_idx != -1 else 0
        seconds = int(s[minute_idx + 1 : second_idx]) if second_idx != -1 else 0
        return timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        )


def strip_day_of_week(last_modified):
    days_of_week = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    ]
    for day in days_of_week:
        last_modified = last_modified.replace(f'{day}, ', '')
    last_modified = last_modified.replace('\u202f', ' ').replace('at ', '')
    return last_modified


def get_time_legacy(last_modified, text_body):
    header = text_body.split('\n')[1].lower().strip()
    last_modified = strip_day_of_week(last_modified)
    # pr(f'{last_modified=}')
    try:
        last_modified_time = datetime.strptime(
            last_modified, '%B %d, %Y %I:%M:%S %p'
        )
        # pr(f'{last_modified_time=}')
    except Exception as e:
        print('Error occurred while parsing last_modified time')
        raise e

    if header.startswith('text '):
        header = header[5:]
    tokens = header.split(' ')
    if len(tokens) == 1:
        return datetime.now()
    elif len(tokens) == 2:
        if tokens[1] == 'now':
            return datetime.now()
        time_string = header.split(' ')[-1]
        time_string = time_string.replace('+', '')
        try:
            delta = str_to_timedelta(time_string)
        except Exception as e:
            raise e
        res = last_modified_time + delta
        s = res.strftime('%B %d, %Y %I:%M:%S %p')
        return last_modified_time + delta
    elif len(tokens) == 6:
        time_string = ' '.join(tokens[1:])
        absolute_time = datetime.strptime(time_string, '%B %d, %Y %I:%M:%S %p')
        return absolute_time
    else:
        raise ValueError(f'Error parsing time from text_body\n{text_body}')

def get_time(last_modified, text_body):
    last_modified = strip_day_of_week(last_modified)
    try:
        last_modified_time = datetime.strptime(
            last_modified, '%B %d, %Y %I:%M:%S %p'
        )
        # pr(f'{last_modified_time=}')
    except Exception as e:
        print('Error occurred while parsing last_modified time')
        raise e
    # header = text_body.split('\n')[0].lower().strip()
    lines = text_body.split('\n')
    if( len(lines) < 3 ):
        raise ValueError('No "true" body to the text')
    time_string = lines[1].strip()
    time_translator = ct.protocol_translator(time_string)
    return time_translator(time_string, last_modified_time)

def text_ready(last_modified, text_body, only_if_ready):
    pr('TEXT_READY CALL')
    last_modified = strip_day_of_week(last_modified)
    last_modified_time = datetime.strptime(
        last_modified, '%B %d, %Y %I:%M:%S %p'
    )
    pr(f'{last_modified_time=}')
    time_since_last_edit = datetime.now() - last_modified_time
    pr(f'{time_since_last_edit=}')
    is_ready = time_since_last_edit > str_to_timedelta(
        env_vars['MAX_IDLE_EDIT_TIME']
    )
    pr(f'{is_ready=}')
    pr(f'{env_vars["MAX_IDLE_EDIT_TIME"]=}')
    pr(f'{str_to_timedelta(env_vars["MAX_IDLE_EDIT_TIME"])=}')
    if only_if_ready:
        is_ready = (
            is_ready and get_time(last_modified, text_body) <= datetime.now()
        )
    return is_ready


# def str_to_timedelta(s):
#     if ':' in s:
#         days, hours, minutes = s.split(':')
#         return timedelta(days=int(days), hours=int(hours), minutes=int(minutes))
#     else:
#         s = s.lower()
#         day_idx, hour_idx, minute_idx = s.find('d'), s.find('h'), s.find('m')
#         days = int(s[:day_idx]) if day_idx != -1 else 0
#         hours = int(s[day_idx + 1 : hour_idx]) if hour_idx != -1 else 0
#         minutes = int(s[hour_idx + 1 : minute_idx]) if minute_idx != -1 else 0
#         return timedelta(days=days, hours=hours, minutes=minutes)


def strip_html_tags(text, strip_img=False):
    """Remove html tags from a string except for img tags."""
    # This pattern matches any tag that is not an img tag
    if not strip_img:
        clean = re.compile('(<(?!img|/img).*?>)')
    else:
        clean = re.compile('(<.*?>)')
    return re.sub(clean, '', text)


def re_ref_imgs(s):
    img_tag_regex = r'<img.*?src="data:image/(.*?);base64,(.*?)".*?>'
    # directory = "/tmp/textschedule/"
    directory = os.path.expanduser('~/Pictures/text_scheduler/')
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists

    # Find the highest current index
    # files = glob.glob(f"{directory}*")
    curr_files = os.listdir(directory)
    counter = len(curr_files)

    for match in re.finditer(img_tag_regex, s):
        ext, data = match.groups()
        img_data = base64.b64decode(data)
        temp_path = f"{directory}{counter}.{ext}"
        with open(temp_path, 'wb') as f:
            f.write(img_data)
        s = s.replace(match.group(), f"@@@IMG {temp_path}@@@")
        counter += 1
    return s


def re_ref_icloud(s):
    icloud_regex = r'(https://share.icloud.com/photos/[A-Za-z0-9\-]{1,50})'

    directory = os.path.expanduser('~/Pictures/text_scheduler/')
    os.makedirs(directory, exist_ok=True)

    curr_files = os.listdir(directory)
    counter = len(curr_files)

    for match in re.finditer(icloud_regex, s):
        url = match.groups()[0]
        pr(f'FOUND ICLOUD LINK: {url}')
        successful_download = download_share_link(url)
        pr(f'{successful_download=}')
        if successful_download:
            most_recent_file = (
                co('ls -t ~/Downloads | head -n 1', shell=True)
                .decode('utf-8')
                .strip()
            )
            file_ext = most_recent_file.split('.')[-1]
            home = os.environ['HOME']
            exit_code = os.system(
                f'mv "{home}/Downloads/{most_recent_file}" {directory}{counter}.{file_ext}'
            )
            if exit_code == 0:
                # s = s.replace(match.group(), f'@@@ICLOUD {url}@@@')
                s = s.replace(
                    match.group(), f'@@@IMG {directory}{counter}.{file_ext}@@@'
                )
            # os.system(
            #     'osascript extra_features/sync_notes/ctrl_right.applescript'
            # )
    return s


def main():
    sync_mode = env_vars['SYNC_MODE'].lower()
    if sync_mode == 'never':
        print('Sync mode is set to "never". Exiting...')
        return
    elif sync_mode == 'always':
        only_if_ready = False
    elif sync_mode in ['conditional', 'only_if_ready']:
        only_if_ready = True
    else:
        raise ValueError(f'Invalid sync mode: {sync_mode}')
    u = co(f'{PROJECT_PATH}/sync_notes.sh', shell=True).decode('utf-8')
    pr(u[:100])
    u = strip_html_tags(u)
    pr(u)
    u = u.replace('\u202f', ' ')
    # if u.startswith('text '):
    #     u = u[5:]

    texts = u.strip().split(DEMARK)[1:]
    if not texts:
        print('No scheduled texts found.')
        return

    for i, text in enumerate(texts):
        lines = text.strip().split('\n')
        last_modified = lines[0].split(' ')[1:]
        last_modified = ' '.join(last_modified).replace('at ', '')
        ref_time = datetime.strptime(last_modified, '%B %d, %Y %I:%M:%S %p')
        header = lines[1].strip()
        if not header.startswith('Text '):
            header = header[0].lower() + header[1:]
            header = 'Text ' + header
        note_id = lines[-1].strip().replace("note id ", "")
        body = '\n'.join(lines[2:-1]).strip()

        if not text_ready(last_modified, text, only_if_ready=only_if_ready):
            # print(f'Text {i+1} not ready. Skipping...')
            continue

        time_mode = header.split(' ')[-1]

        header_meat = " ".join(header.split(" ")[:-1]).strip()

        if time_mode.lower() == 'now':
            scheduled_time = ref_time.strftime('%B %d, %Y %I:%M:%S %p')
            header = f'{header_meat} {scheduled_time}'
        if time_mode[0] == '+':
            delta = str_to_timedelta(time_mode[1:])
            scheduled_time = (ref_time + delta).strftime(
                '%B %d, %Y %I:%M:%S %p'
            )
            header = f'{header_meat} {scheduled_time}'

        filename = f'{header}.txt'
        pr(filename)
        path = os.path.join(SCHEDULED_TEXTS_DIRECTORY, filename)
        sent_path = os.path.join(SCHEDULED_TEXTS_DIRECTORY, 'sent', filename)
        move_note_cmd = f'osascript extra_features/sync_notes/move_note.applescript "{note_id}"'
        print(note_id)
        if os.path.exists(sent_path):
            print(
                f'File "{sent_path}" already exists, meaning message has already been sent. Skipping...'
            )
            os.system(move_note_cmd)
            continue
        if os.path.exists(path):
            print(f'File "{path}" already exists. Skipping...')
            os.system(move_note_cmd)
            continue

        with open(path, 'w') as f:
            body = re_ref_imgs(body)
            body = re_ref_icloud(body)
            pr(body)
            f.write(body.strip())
            os.system(move_note_cmd)
            print(f'File "{path}" created')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pr('Error occurred:', e)
        raise e

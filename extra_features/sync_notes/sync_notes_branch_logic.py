import os
from datetime import datetime, timedelta
import sys
from dotenv import dotenv_values
import re

# temporary hack -- refactor this later on
sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))
import extra_features.custom_times as ct

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)

# f = open('/tmp/branch_out.txt', 'a')
f = sys.stdout
pr = lambda *args, **kwargs: print(*args, **kwargs, file=f, flush=True)


def strip_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def str_to_timedelta(s, default='m'):
    s = s.lower()
    if 'h' not in s and 'm' not in s and 's' not in s:
        s = f, '{s}{default}'
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
    header = text_body.split('\n')[0].lower().strip()
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


def main():
    pr('hello')
    # print(env_vars)
    sync_mode = env_vars['SYNC_MODE'].lower()
    pr(f'{sync_mode=}')
    if sync_mode not in ['always', 'never', 'conditional', 'only_if_ready']:
        pr(
            f'Invalid value for SYNC_MODE: {env_vars["SYNC_MODE"]}'
            f'\nValid values are: always, never, conditional, only_if_ready'
        )
        pr('YOYOY')
        return 1
    if sync_mode == 'never':
        return 1
    if len(sys.argv) != 3:
        raise ValueError(
            'Usage: python sync_notes_branch_logic.py last_modified text_body'
        )
    only_if_ready = sync_mode in ['conditional', 'only_if_ready']
    pr(f'{only_if_ready=}')
    last_modified, text_body = sys.argv[1:]
    pr(f'{last_modified=}')
    pr(f'{datetime.now()=}')
    text_body = strip_html_tags(text_body)
    pr(f'{text_body=}')
    is_ready = text_ready(last_modified, text_body, only_if_ready)
    pr(f'{is_ready=}')
    exit_code = int(not is_ready)
    # rememmber exit_code == 0 is success, hence the "not"
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        pr(f'Error occurred: {e}')
        sys.exit(1)

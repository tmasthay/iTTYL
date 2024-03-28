from subprocess import check_output as co
import os
from datetime import datetime, timedelta

DEMARK = "*** SCHEDULED TEXT ***\n"
SCHEDULED_TEXTS_DIRECTORY = [
    e
    for e in open('SETTINGS.txt').read().split('\n')
    if e.startswith('SCHEDULED_TEXTS_DIRECTORY')
][0].split('=')[1]


def str_to_timedelta(s):
    if ':' in s:
        days, hours, minutes = s.split(':')
        return timedelta(days=int(days), hours=int(hours), minutes=int(minutes))
    else:
        s = s.lower()
        day_idx, hour_idx, minute_idx = s.find('d'), s.find('h'), s.find('m')
        days = int(s[:day_idx]) if day_idx != -1 else 0
        hours = int(s[day_idx + 1 : hour_idx]) if hour_idx != -1 else 0
        minutes = int(s[hour_idx + 1 : minute_idx]) if minute_idx != -1 else 0
        return timedelta(days=days, hours=hours, minutes=minutes)


def main():
    u = co(
        './extra_features/iphone_integration/sync_notes.sh', shell=True
    ).decode('utf-8')
    u = u.replace('\u202f', ' ')

    texts = u.strip().split(DEMARK)[1:]
    if not texts:
        print('No scheduled texts found.')
        return

    for i, text in enumerate(texts):
        lines = text.split('\n')
        last_modified = lines[0].split(' ')[2:]
        last_modified = ' '.join(last_modified).replace('at ', '')
        ref_time = datetime.strptime(last_modified, '%B %d, %Y %I:%M:%S %p')
        header = lines[1].strip()
        if not header.startswith('Text '):
            header[0] = header[0].lower()
            header = 'Text ' + header
        body = '\n'.join(lines[2:])

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
        path = os.path.join(SCHEDULED_TEXTS_DIRECTORY, filename)
        sent_path = os.path.join(SCHEDULED_TEXTS_DIRECTORY, 'sent', filename)
        if os.path.exists(sent_path):
            print(
                f'File "{sent_path}" already exists, meaning message has already been sent. Skipping...'
            )
            continue
        if os.path.exists(path):
            print(f'File "{path}" already exists. Skipping...')
            continue

        with open(path, 'w') as f:
            f.write(body.strip())
            print(f'File "{path}" created')


if __name__ == "__main__":
    main()

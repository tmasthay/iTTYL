from subprocess import check_output as co
import os
from datetime import datetime, timedelta

DEMARK = "*** SCHEDULED TEXT ***\n"
SCHEDULED_TEXTS_DIRECTORY = [
    e
    for e in open('SETTINGS.txt').read().split('\n')
    if e.startswith('SCHEDULED_TEXTS_DIRECTORY')
][0].split('=')[1]


def main():
    u = co('./test.sh', shell=True).decode('utf-8')

    texts = u.strip().split(DEMARK)[1:]
    # input(u.strip().split(DEMARK)[1:])

    for i, text in enumerate(texts):
        lines = text.split('\n')
        header = lines[0].strip()
        body = '\n'.join(lines[1:])

        if header.split(' ')[-1].lower() == 'now':
            header = " ".join(header.split(" ")[:-1]).strip()
            formatted_date = datetime.now().strftime('%B %d, %Y %H:%M')
            header = f'{header} {formatted_date}'
        if header.split(' ')[-1][0] == '+':
            time = header.split(' ')[-1]

            days = 0
            hours = 0
            minutes = 0

            if ':' in time:
                parts = time.split(':')
                if len(parts) == 2:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                elif len(parts) == 3:
                    days = int(parts[0].replace('d', ''))
                    hours = int(parts[1])
                    minutes = int(parts[2])
            else:
                hours = int(time)

            now = datetime.now()
            future_time = now + timedelta(
                days=days, hours=hours, minutes=minutes
            )

            header_body = ' '.join(header.split(' ')[:-1]) + ' '
            header = header_body + future_time.strftime('%B %d, %Y %H:%M')

            # Use the days, hours, and minutes variables as needed

        filename = f'{header}.txt'
        input(filename)
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
            f.write(body)
            print(f'File "{path}" created with following message:\n{body}')


if __name__ == "__main__":
    main()

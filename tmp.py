from subprocess import check_output as co
import os

DEMARK = "*** SCHEDULED TEXT ***\n"
SCHEDULED_TEXTS_DIRECTORY = [
    e
    for e in open('SETTINGS.txt').read().split('\n')
    if e.startswith('SCHEDULED_TEXTS_DIRECTORY')
][0].split('=')[1]


def main():
    u = co('./test.sh', shell=True).decode('utf-8')

    texts = u.strip().split(DEMARK)[1:]
    input(u.strip().split(DEMARK)[1:])

    for i, text in enumerate(texts):
        lines = text.split('\n')
        header = lines[0].strip()
        body = '\n'.join(lines[1:])
        path = f"{SCHEDULED_TEXTS_DIRECTORY}/{header}.txt"
        if os.path.exists(path):
            print(f'File "{path}" already exists. Skipping...')
            continue

        with open(path, 'w') as f:
            f.write(body)
            print(f'File "{path}" created with following message:\n{body}')


if __name__ == "__main__":
    main()

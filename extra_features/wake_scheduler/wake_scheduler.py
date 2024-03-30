from dotenv import dotenv_values
import os
from subprocess import check_output as co
import sys

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)
PROJECT_ROOT = os.getcwd()
REL_PATH = os.path.relpath(os.path.dirname(__file__), PROJECT_ROOT)
PROJECT_PATH = os.path.abspath(REL_PATH)
LAUNCH_DIR = os.path.expanduser(
    env_vars.get("LAUNCHD_DIR", "~/Library/LaunchAgents")
)
TEMPLATE_PLIST_NAME = f'{PROJECT_PATH}/com.template.wakeup_and_text.plist'
TARGET_PLIST_NAME = (
    f'{LAUNCH_DIR}/com.{env_vars["YOUR_NAME"]}.wakeup_and_text.plist'
)


def gen_plist():
    with open(TEMPLATE_PLIST_NAME, 'r') as f:
        plist_content = f.read()
        s = plist_content.replace('REPO_ROOT', PROJECT_ROOT)
        relevant_env_vars = [
            'ABSOLUTE_PYTHON_PATH',
            'OUTPUT_PATH',
            'WAKE_FREQUENCY',
            'YOUR_NAME',
        ]
        for e in relevant_env_vars:
            s = s.replace(e, env_vars[e])
        with open(TARGET_PLIST_NAME, 'w') as f:
            f.write(s)


def user_input(s):
    res = input(s)
    if res.lower() != 'y':
        print('Exiting...')
        sys.exit(1)


def main():
    user_input(
        'Will create a launchd process that wakes '
        ' up the computer and sends scheduled texts automatically. Continue? (y/n): '
    )
    if os.path.exists(TARGET_PLIST_NAME):
        user_input('Launchd process already exists. Overwrite? (y/n): ')

    print(f'Generating {TARGET_PLIST_NAME}...', end='')
    gen_plist()
    print('done.')

    launchd_process_name = f'com.{env_vars["YOUR_NAME"]}.wakeup_and_text'
    if os.system(f'launchctl list | grep {launchd_process_name}') == 0:
        print('Stopping the current launchd process...', end='')
        cmd = f'launchctl unload {TARGET_PLIST_NAME}'
        if os.system(cmd):
            raise RuntimeError(
                f'Failed to stop the launchd process with command\n    {cmd}'
            )
        print('done.')

    if os.system(f'launchctl load {TARGET_PLIST_NAME}'):
        raise RuntimeError('Failed to load the launchd process.')
    else:
        print('Launchd process updated and restarted.')
        return


if __name__ == "__main__":
    main()

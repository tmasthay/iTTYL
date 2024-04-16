from subprocess import check_output as co
from dotenv import dotenv_values


def get_contact_list():
    DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
    env_vars = dotenv_values(DOTENV_SETTINGS_PATH)
    contacts = {k: v for k, v in env_vars.items() if k.lower() == k}
    return contacts


def main():
    path = 'extra_features/group_chats'
    s = co(f'osascript {path}/see_group_chats.applescript', shell=True).decode(
        'utf-8'
    )
    s = s.strip()
    # s = s.replace('iMessage;+;', '')
    lines = s.split('\n')
    clean_lines = [e.split(':')[-1].replace('+', '').replace(';;', ';+;') for e in lines]
    s = '\n'.join(clean_lines)

    contacts = get_contact_list()
    # replace the numbers with names from contact list, if possible
    for k, v in contacts.items():
        if v not in [None, '']:
            s = s.replace(v, k)

    chats = s.split('\n\n')
    d = {}
    for c in chats:
        lines = c.split("\n")
        chat_name = lines[0]
        numbers = [e.strip() for e in lines[1:]]
        d[chat_name] = numbers

    for k, v in d.items():
        print(k)
        for number in v:
            print(f'    {number}')

    print(
        '\n\nThe above group chats were found.\n'
        'Names starting with "chat" are likely not registered in SETTINGS.txt ("chat" is Apple\'s delimiter).\n'
        'To add a chat with descriptive name, simply add line to SETTINGS.txt similar to the below.\n\n'
        '    my_chat_name=chat1234567890\n\n'
    )


if __name__ == "__main__":
    main()

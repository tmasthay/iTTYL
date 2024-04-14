import os
import glob
import subprocess
from datetime import datetime
from dateutil import parser
import shutil
import re
from dotenv import dotenv_values
import traceback
import sys
import time

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)

SMS_CONTACTS_PATH = "./SMS_CONTACTS.txt"
SMS_CONTACTS = open(SMS_CONTACTS_PATH, "r").read().strip().split("\n")


MAX_OVERTIME_MINS = int(env_vars["MAX_OVERTIME_MINS"])

DEBUG_TEXTING = env_vars["DEBUG_TEXTING"] == "True"

SCHEDULED_TEXTS_DIRECTORY = env_vars["SCHEDULED_TEXTS_DIRECTORY"]

# get only files starting with 'text' and ending in .txt or .md in the notes directory
TEXT_FILENAME_PATTERN = re.compile(r"^text.*\.(txt|md)$", re.IGNORECASE)
SEND_IMESSAGE_SCRIPT_PATH = "./send_imessage.applescript"
SEND_SMS_SCRIPT_PATH = "./send_sms.applescript"
SEND_GROUP_IMESSAGE_SCRIPT_PATH = (
    "./extra_features/group_chats/send_group_chat.applescript"
)
PURE_BOT = env_vars["PURE_BOT"].lower()[0] in ['t', 'y', '1']

f = open('/tmp/send_debug.txt', 'a')
pr = lambda *args, **kwargs: print(*args, **kwargs, file=f, flush=True)


def eat_images(s):
    # return s, ''
    lines = s.split('\n')
    image_paths = []
    processed_lines = []
    for line in lines:
        if line.startswith('@@@IMG') and line.endswith('@@@'):
            path = line[7:-3].strip()
            image_paths.append(path)
        else:
            processed_lines.append(line)
    processed_s = '\n'.join(processed_lines)
    processed_paths = ','.join(image_paths)
    pr(f'{processed_s=}')
    pr(f'{processed_paths=}')
    return processed_s, processed_paths


def parse_human_datetime(human_datetime):
    if human_datetime == "now" or human_datetime == "asap":
        return datetime.now()
    return parser.parse(human_datetime)


def get_date_from_filename(filename):
    last_dot_index = filename.rfind(".")
    filename_without_extension = (
        filename[:last_dot_index] if last_dot_index != -1 else filename
    )
    parts = filename_without_extension.split(" ", 2)
    return " ".join(parts[2:])


def parse_datetime_from_filename(filename):
    human_datetime = get_date_from_filename(filename).lower()

    t = parse_human_datetime(human_datetime)

    return t


def file_ready_to_be_sent(filename):
    t = parse_datetime_from_filename(filename)
    now = datetime.now()
    dt_mins = abs((t - now).total_seconds() / 60)
    # t is earlier than now, and the diff
    return t < now and dt_mins <= MAX_OVERTIME_MINS


def move_file_to_sent_directory(file_path):
    dest_dir = f"{SCHEDULED_TEXTS_DIRECTORY}/sent"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    shutil.move(file_path, dest_dir)


def parse_recipient_from_filename(filename):
    return filename.split()[1].lower()


def get_recipient_number_from_filename(contact_name):
    print(f'{contact_name=}', flush=True)
    try:
        recipient = ""
        if contact_name in env_vars:
            recipient = env_vars[contact_name].lower()
        if recipient.startswith("chat"):
            recipient = f"imessage;+;{recipient}"
        elif contact_name not in env_vars:
            # recipient = contact_name # do nothing since arbitrary strings allowed
            split_rec = [e for e in contact_name.split("&amp") if len(e) > 0]
            s = ''
            for rec in split_rec:
                if rec in env_vars:
                    s += env_vars[rec].lower() + '&amp'
                else:
                    s += rec + '&amp'
            if s.endswith('&amp'):
                s = s[:-4]
            recipient = s
        # else:
        #     recipient = contact_name
        # else:
        #     raise ValueError(
        #         f"Error: contact name '{contact_name}' not declared in settings file."
        #     )
        if PURE_BOT or is_sms_recipient(recipient):
            recipient = recipient.replace('_', ' ').strip()
            if recipient.endswith('&amp'):
                recipient = recipient[:-4]
        print(f'in get_recipient...{recipient=}')
        return recipient
    except Exception as e:
        print(f'Unanticipated error getting recipient number for {contact_name}...error below')
        print(e)
        return recipient

def is_sms_recipient(recipient):
    pure_bot = env_vars["PURE_BOT"].lower()
    if pure_bot[0] in ['t', 'y', '1']:
        return True
    split_rec = [e for e in recipient.split("&amp") if len(e) > 0]
    is_sms = False

    F = open('./sms.txt', 'w')

    # see if any contacts are SMS contacts
    for rec in split_rec:
        if rec in SMS_CONTACTS or rec.startswith("sms"):
            is_sms = True
            break
        
        # check if recipient is a raw phone number
        number_found_in_contacts = False
        if rec.replace("+", "").isdigit():
            F.write(f'{rec=}\n')
            # check to see if the number is in the contacts list
            for k, v in env_vars.items():
                if v == rec:
                    number_found_in_contacts = True
                    # check if the associated key is an SMS contact
                    if k in SMS_CONTACTS:
                        F.write('Found in SMS contacts\n')
                        is_sms = True
                        break
            if env_vars['RAW_NUMBER_FALLBACK'].lower() == 'sms' and not number_found_in_contacts:
                F.write('raw fallback\n')
                is_sms = True
                break

    # forcing sms by putting a dummy & at the end of the recipient
    #     Example: "me& now" will force an SMS to "me", even if "me" is iMessage
    #     Logic behind this syntax is that "&" is used for concatenation for
    #         group chat instantiation. So, if "&" is present, it is like we are
    #         treating the empty string as a "raw phone number". 
    #         I don't think this is a hack...it's pretty elegant, but consider
    #         another character maybe for extra clarity?
    force_sms = '&amp' in recipient and env_vars['RAW_NUMBER_FALLBACK'].lower() == 'sms'
    return is_sms or force_sms

def last_keypress():
    cmd="ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
    s = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(s)

def is_group_chat_recipient(phone_number):
    print(f'{phone_number=}')
    return phone_number.startswith("imessage;+;chat")


def send_message(file):
    try:
        contact_name = parse_recipient_from_filename(file.name)
        recipient = get_recipient_number_from_filename(contact_name)
        message = file.read()
        print('PRE-EAT')
        message, images = eat_images(message)
        message = message.replace("&amp", "&").strip()
        print(f'POST-EAT: {message=}, {images=}')
        if DEBUG_TEXTING:
            print(f"DEBUG TEXTING MODE: Would send {recipient}: {message}")
            move_file_to_sent_directory(file.name)
            return

        pr(f'Recipient={recipient}')
        if is_sms_recipient(contact_name):
            print('SMS branch chosen')
            if images != '':
                # give user some time to login if they need to
                buffer_time = int(env_vars["LOGIN_BUFFER_TIME"])
                time.sleep(buffer_time + 1)
                most_recent_keypress = last_keypress()
                print(f'{most_recent_keypress=}, {images=}')
                if most_recent_keypress > buffer_time:
                    # user is not active, meaning computer is probably asleep
                    #     or locked. We won't send the message since in this
                    #     case, we need GUI interaction spoofing to send the
                    #     message.
                    print('User inactive for image-based SMS message...not sending message until user becomes active again')
                    return
            try:
                message = message.replace('"', '\"').strip()
                pr(f'{recipient=}, {message=}, {images=}')
                subprocess.run(
                    [
                        "osascript",
                        SEND_SMS_SCRIPT_PATH,
                        recipient,
                        message,
                        images,
                    ],
                    check=True,
                )
                move_file_to_sent_directory(file.name)
            except subprocess.CalledProcessError as e:
                print("error sending iMessage:", e)
        elif is_group_chat_recipient(recipient):
            print('group iMessage branch chosen')
            message = message.replace('"', '\"').replace("&amp", "").strip()
            cmd = f'osascript {SEND_GROUP_IMESSAGE_SCRIPT_PATH} "{recipient}" "{message}" "{images}"'
            print(cmd, flush=True)
            try:
                # subprocess.run(
                #     [
                #         "osascript",
                #         SEND_GROUP_IMESSAGE_SCRIPT_PATH,
                #         f"'{recipient}'",
                #         f"'message'",
                #     ],
                #     check=True,
                # )
                # obviously not ideal for security reasons but it works
                #     I'm misinterpreting something with subprocess.run.
                #     Key is that I need to protect shell expansion of the recipient and message variables.
                subprocess.check_output(cmd, shell=True)
                move_file_to_sent_directory(file.name)
            except subprocess.CalledProcessError as e:
                print("error sending group iMessage:", e)
        else:
            print('regular iMessage branch chosen')
            try:
                print(f'{recipient=}, {message=}, {images=}')
                message = message.replace('"', '\"').replace('&amp', '').strip()
                subprocess.run(
                    [
                        "osascript",
                        SEND_IMESSAGE_SCRIPT_PATH,
                        recipient,
                        message,
                        images,
                    ],
                    check=True,
                )
                move_file_to_sent_directory(file.name)
            except subprocess.CalledProcessError as e:
                print("error sending iMessage:", e)
    except Exception as e:
        print(f'Error sending {file}...error below')
        print(e)


def send_messages(directory):
    pr('SEND_MESSAGES CALL')
    files = []
    for file_path in glob.glob(os.path.join(directory, "*")):
        filename = os.path.basename(file_path)
        try:
            if TEXT_FILENAME_PATTERN.match(filename) and file_ready_to_be_sent(
                filename
            ):
                with open(file_path, "r", encoding="utf-8") as file:
                    send_message(file)
                print(f'Sent {filename} successfully')
        except Exception as e:
            print(f'Error sending {filename}...error below')
            print(f'    {e}')
            traceback.print_exc(file=sys.stdout)

    return files


if __name__ == "__main__":
    send_messages(SCHEDULED_TEXTS_DIRECTORY)

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

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)


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
    try:
        recipient = env_vars[contact_name].lower()
        if recipient.startswith("chat"):
            recipient = f"imessage;+;{recipient}"
        return recipient
    except KeyError:
        raise ValueError(
            f"Error: contact name '{contact_name}' not declared in settings file."
        )


def is_sms_recipient(recipient):
    return recipient.split("_")[0] == "sms"


def is_group_chat_recipient(phone_number):
    return phone_number.startswith("imessage;+;chat")


def send_message(file):
    try:
        contact_name = parse_recipient_from_filename(file.name)
        recipient = get_recipient_number_from_filename(contact_name)
        message = file.read()
        print('PRE-EAT')
        message, images = eat_images(message)
        print(f'POST-EAT: {message=}, {images=}')
        if DEBUG_TEXTING:
            print(f"DEBUG TEXTING MODE: Would send {recipient}: {message}")
            move_file_to_sent_directory(file.name)
            return

        pr(f'Recipient={recipient}')
        if is_sms_recipient(contact_name):
            print('SMS branch chosen (shouldnt happend)')
            try:
                subprocess.run(
                    ["osascript", SEND_SMS_SCRIPT_PATH, recipient, message],
                    check=True,
                )
                move_file_to_sent_directory(file.name)
            except subprocess.CalledProcessError as e:
                print("error sending SMS:", e)
        elif is_group_chat_recipient(recipient):
            print('group iMessage branch chosen')
            message = message.replace('"', '\"')
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
                pr(f'{recipient=}, {message=}, {images=}')
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

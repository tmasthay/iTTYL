import yaml
import datetime
import os
import re


class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_times.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)


def tonight(time_string, last_modified_time):
    c = CustomTimesNamespace.cfg['tonight']

    tokens = time_string.strip().lower().split(' ')
    if len(tokens) > 1:
        c['time'] = ' '.join(tokens[1:])

    # Calculate what time today at midnight is
    today = datetime.date.today()
    now = datetime.datetime.now()

    # Read in format in HH:MM AM/PM format relative to today
    # time = datetime.datetime.strptime(c['time'], '%I:%M %p'
    time = datetime.datetime.strptime(c['time'], '%I:%M %p')
    send_time = datetime.datetime.combine(today, time.time())

    return send_time


def now(time_string, last_modified_time):
    return datetime.datetime.now()


def plus(time_string, last_modified_time):
    time_string = time_string.replace('+', '')
    day_index = time_string.rfind('d')
    hour_index = time_string.rfind('h')
    minute_index = time_string.rfind('m')

    days = 0 if day_index == -1 else int(time_string[:day_index])
    hours = (
        0 if hour_index == -1 else int(time_string[day_index + 1 : hour_index])
    )
    minutes = (
        0
        if minute_index == -1
        else int(time_string[hour_index + 1 : minute_index])
    )

    u = last_modified_time + datetime.timedelta(
        days=days, hours=hours, minutes=minutes
    )
    print(u)
    return u


def protocol_translator(s):
    c = CustomTimesNamespace.cfg
    s = s.lower()

    # do special regex for XdYhZm
    # if s.startswith('+') or re.match(r'^\d+[dhms]$', s):
    #     return plus

    if re.match(r'^(?:\d+d)?(?:\d+h)?(?:\d+m)?$', s):
        return plus

    for k in c.keys():
        if s == k or ('aliases' in c[k] and s in c[k]['aliases']):
            # dynamically import the function from this file
            return globals()[k]
    else:
        # read absolute time
        def helper(time_string, last_modified_time):
            input(s)
            return datetime.datetime.strptime(s, '%B %d, %Y %I:%M:%S %p')

        return helper


def main():
    print(
        'custom_times is not meant to be a "true" addon to be executed at command line.'
        'It is meant to be an easy way to extend custom times for scheduling.'
        'An example would be "tonight" to translate to "calculate today at 8:00PM".'
    )

    print(protocol_translator(''))


if __name__ == "__main__":
    main()

import yaml
import datetime
import os

class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_times.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)

def tonight(time_string, last_modified_time):
    c = CustomTimesNamespace.cfg['tonight']

    tokens = time_string.strip().lower().split(' ')
    if( len(tokens) > 1 ):
        c['time'] = ' '.join(tokens[1:])

    # Calculate what time today at midnight is 
    today = datetime.date.today()
    now = datetime.datetime.now()

    # Read in format in HH:MM AM/PM format relative to today
    # time = datetime.datetime.strptime(c['time'], '%I:%M %p'
    time = datetime.datetime.strptime(c['time'], '%I:%M %p')
    send_time = datetime.datetime.combine(today, time.time())

    # If the time has already passed, then it is for tomorrow
    if now > send_time:
        send_time += datetime.timedelta(days=1)
    
    return send_time

def protocol_translator(s):
    c = CustomTimesNamespace.cfg
    s = s.lower()
    for k in c.keys():
        if s in c[k] or ('aliases' in c[k] and s in c[k]['aliases']):
            # dynamically import the function from this file
            return globals()[k]
    else:
        # read absolute time
        def helper(time_string, last_modified_time):
            return datetime.datetime.strptime(s, '%B %d, %Y %I:%M:%S %p')
        return helper



def main():
    print('custom_times is not meant to be a "true" addon to be executed at command line.'
          'It is meant to be an easy way to extend custom times for scheduling.'
          'An example would be "tonight" to translate to "calculate today at 8:00PM".')

    print(protocol_translator(''))
    

if __name__ == "__main__":
    main()
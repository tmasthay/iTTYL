import yaml
import datetime
import os
import re


class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_formats.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)

def daily_mailly(text):
    text = text.strip()
    if not text.startswith('DAILY MAILLY'):
        text = f'DAILY MAILLY\n{text}'

def protocol_translator(s):
    c = CustomTimesNamespace.cfg
    u = s.strip().split('\n')
    if len(u) == 0:
        return s
    else:
        u = u[0]

    for k in c.keys():
        aliases = c[k].get('aliases', [])
        if u.startswith(k) or (
            any([u.startswith(a) for a in aliases])
        ):
            # dynamically import the function from this file
            return globals()[k](s)
    else:
        return s
    

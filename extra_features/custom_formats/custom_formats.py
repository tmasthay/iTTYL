import yaml
import datetime
import os
import re


class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_formats.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)

def daily_mailly(text):
    text = text.strip()
    lines = text.split('\n')
    if len(lines) == 0:
        return text
    elif not lines[0].startswith('DAILY MAILLY'):
        lines[0] = 'DAILY MAILLY'
    text = '\n'.join(lines).strip()
    return text

def protocol_translator(s):
    c = CustomTimesNamespace.cfg
    u = s.strip().split('\n')
    if len(u) == 0:
        return s
    else:
        u = u[0].lower().strip()

    for k in c.keys():
        aliases = c[k].get('aliases', [])
        if u.startswith(k) or (
            any([u.startswith(a) for a in aliases])
        ):
            # dynamically import the function from this file
            return globals()[k](s)
    else:
        return s
    

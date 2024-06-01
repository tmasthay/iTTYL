import yaml
import datetime
import os
import re


class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_formats.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)

def daily_mailly(text, *, contact_name=None):
    text = text.strip()
    lines = text.split('\n')
    if len(lines) == 0:
        return text
    
    header = 'DAILY MAILLY\n\n'
    # Ensure the first line is "DAILY MAILLY"
    if not lines[0].startswith('DAILY MAILLY'):
        lines.pop(0)
    
    # Join the lines back into a single text
    text = '\n'.join(lines).strip()

    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')

    # Split the text into submessages using double new lines as the separator
    submessages = text.split('\n\n')

    # Create a numbered list from the submessages
    numbered_submessages = []
    img_submarker = 0
    for i, submessage in enumerate(submessages, start=1):
        submsg = submessage.strip()
        image_marker = '@@@IMG'
        if image_marker in submsg:
            img_submarker += 1
            submsg = f'{i}.\n[IMG {img_submarker}]\n{submsg}'
        else:
            submsg = f'{i}.\n{submsg}'
        numbered_submessages.append(submsg)

    # Join the header and the numbered submessages back into the final text
    final_text = header + '\n\n'.join(numbered_submessages)

    return final_text

def general_mail(text, *, contact_name=None):
    c = CustomTimesNamespace.cfg
    if contact_name not in c['general_mail']['people'].keys():
        contact_name = 'default'
        
    text = text.strip()
    lines = text.split('\n')
    if len(lines) == 0:
        return text
    
    header = 'DAILY MAILLY\n\n'
    # Ensure the first line is "DAILY MAILLY"
    if not lines[0].startswith('DAILY MAILLY'):
        lines.pop(0)
    
    # Join the lines back into a single text
    text = '\n'.join(lines).strip()

    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')

    # Split the text into submessages using double new lines as the separator
    submessages = text.split('\n\n')

    # Create a numbered list from the submessages
    numbered_submessages = []
    img_submarker = 0
    for i, submessage in enumerate(submessages, start=1):
        submsg = submessage.strip()
        image_marker = '@@@IMG'
        if image_marker in submsg:
            img_submarker += 1
            submsg = f'{i}.\n[IMG {img_submarker}]\n{submsg}'
        else:
            submsg = f'{i}.\n{submsg}'
        numbered_submessages.append(submsg)

    # Join the header and the numbered submessages back into the final text
    final_text = header + '\n\n'.join(numbered_submessages)

    return final_text



def protocol_translator(s, *, contact_name=None):
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
            return globals()[k](s, contact_name=contact_name)
    else:
        return s
    

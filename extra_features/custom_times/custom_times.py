import yaml
import datetime
import os
import re
from datetime import datetime, timedelta
import random


class CustomTimesNamespace:
    path = os.path.dirname(__file__) + '/custom_times.yaml'
    cfg = yaml.load(open(path), Loader=yaml.FullLoader)


class Helpers:
    @staticmethod
    def star_box(heading, spaces, line_width):
        if heading is None:
            return ""

        # Split the heading into lines based on the line_width
        words = heading.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= line_width:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word

        # Add the last line
        if current_line:
            lines.append(current_line)

        # Calculate the width of the box
        max_line_length = max(len(line) for line in lines)
        total_width = (
            max_line_length + spaces * 2 + 2
        )  # 2 for the stars at the sides

        # Create the top and bottom borders
        border = '*' * total_width

        # Create the empty lines with stars at the sides
        space_char = "😈"
        empty_line = '*' + ' ' * (total_width - 2) + '*'

        # Create the lines with heading text
        heading_lines = [
            '*'
            + ' ' * spaces
            + line
            + ' ' * (total_width - len(line) - spaces - 2)
            + '*'
            for line in lines
        ]

        # Construct the star box
        star_box_str = '\n'.join(
            [border, empty_line] + heading_lines + [empty_line, border]
        )

        # valid_star_emojis = ["😍", "🐕", "🥺"] 
        # valid_space_emojis = ["🐭", "🤩", "🐶"]
        valid_star_emojis = ['*']
        valid_space_emojis = ['.']

        # randomly select a star replacement emoji
        rand_idx = random.randint(0, len(valid_star_emojis) - 1)
        star_char = valid_star_emojis[rand_idx]

        # randomly select a space replacement emoji
        rand_idx = random.randint(0, len(valid_space_emojis) - 1)
        space_char = valid_space_emojis[rand_idx]

        have_fun = False
        if have_fun:
            # Replace the stars and spaces with the emojis
            star_box_str = star_box_str.replace('*', star_char)
            star_box_str = star_box_str.replace(' ', space_char)

        return star_box_str

    @staticmethod
    def weird_star_box(heading, spaces, line_width):
        if heading is None:
            return ""

        # Split the heading into lines based on the line_width
        words = heading.split()
        lines = []
        current_line = ""

        for word in words:
            if (
                len(current_line) + len(word) + (1 if current_line else 0)
                <= line_width
            ):
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word

        # Add the last line
        if current_line:
            lines.append(current_line)

        # Calculate the width of the box
        max_line_length = max(len(line) for line in lines)
        total_width = (
            max_line_length + spaces * 2 + 2
        )  # 2 for the stars at the sides

        # Create the top and bottom borders
        border = '*' * total_width

        # Create the empty lines with stars at the sides
        empty_line = '*' + ' ' * (total_width - 2) + '*'

        # Create the lines with heading text
        heading_lines = []
        for line in lines:
            space_left = (
                total_width - len(line) - 2
            )  # total space minus stars and line length
            left_padding = spaces
            right_padding = space_left - left_padding
            heading_line = (
                '*' + ' ' * left_padding + line + ' ' * right_padding + '*'
            )
            heading_lines.append(heading_line)

        # Construct the star box
        star_box_str = '\n'.join(
            [border, empty_line] + heading_lines + [empty_line, border]
        )

        return star_box_str

    @staticmethod
    def make_line(edge_char, fill_char, meat_text, line_width):
        assert len(meat_text) <= line_width

        num_edges = 2
        num_fills = line_width - num_edges - len(meat_text)
        left_fills = num_fills // 2
        right_fills = num_fills - left_fills
        left_filler = fill_char * left_fills
        right_filler = fill_char * right_fills

        s = edge_char + left_filler + meat_text + right_filler + edge_char
        return s

    @staticmethod
    def get_rand_elem(lst):
        return lst[random.randint(0, len(lst) - 1)]

    @staticmethod
    def make_line(edge_char, fill_char, meat_text, line_width):
        assert len(meat_text) <= line_width

        num_edges = 2
        num_fills = line_width - num_edges - len(meat_text)
        left_fills = num_fills // 2
        right_fills = num_fills - left_fills
        left_filler = fill_char * left_fills
        right_filler = fill_char * right_fills

        s = edge_char + left_filler + meat_text + right_filler + edge_char
        return s

    @staticmethod
    def fun_star_box_selected(edge_char, fill_char, meat_text, line_width):
        assert max([len(e) for e in meat_text.strip().split()]) <= line_width

        num_fill_lines = 2
        top_border = Helpers.make_line(edge_char, fill_char, "", line_width)
        bottom_border = Helpers.make_line(edge_char, fill_char, "", line_width)
        filler_line = Helpers.make_line(edge_char, fill_char, "", line_width)
        filler_line = num_fill_lines * (filler_line + "\n")

        # figure out true line width based on fact that characters only take up one space
        # and emojis take up two spaces
        # extra_emojis = -int(0.3333 * len(meat_text))
        # extra_emojis = int(0.333 * len(meat_text))

        meat_line = ""
        tokens = meat_text.split()
        for token in tokens:
            assert len(token) <= line_width
            extra_emojis = int(0.5 * len(token))
            if fill_char == '.':
                extra_emojis = 0
            meat_line += Helpers.make_line(edge_char, fill_char, token, line_width + extra_emojis) + "\n"

        s = (
            top_border
            + "\n"
            + filler_line
            + meat_line
            + filler_line
            + bottom_border
        )
        return s

    @staticmethod
    def fun_star_box(header, width_pad, iphone_width):
        # edge_char_choices = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊"]
        # fill_char_choices = ["🤩", "🥺", "🤯", "🤪", "🤓", "🤠", "🤡"]
        edge_char_choices = ['*']
        fill_char_choices = ['.']

        edge_char = Helpers.get_rand_elem(edge_char_choices)
        fill_char = Helpers.get_rand_elem(fill_char_choices)

        return Helpers.fun_star_box_selected(edge_char, fill_char, header, iphone_width)


class FormatProtocols:
    @staticmethod
    def header_list(text, *, contact_name=None, header, width_pad, height_pad, raw_header):
        text = text.strip()
        lines = text.split('\n')
        if len(lines) == 0:
            return text

        # make a box of stars around the header
        iphone_width = 26
        # header = Helpers.weird_star_box(header, width_pad, iphone_width) + '\n\n'
        if not raw_header:
            header = Helpers.fun_star_box(header, width_pad, iphone_width) + '\n\n'

        # Ensure the first line is "DAILY MAILLY"
        # if not lines[0].startswith('DAILY MAILLY'):
        #     lines.pop(0)

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

        if "/" in final_text:
            print(final_text)
        return final_text


class TimeProtocols:
    @staticmethod
    def leapfrog(last_modified_time, *, time_of_day, day_of_week, week_jump):
        # Parse the input strings into datetime objects
        # last_modified_time = datetime.strptime(last_modified_time, "%A %B %d, %Y %I:%M %p")
        if time_of_day.lower() == "now":
            time_of_day_dt = datetime.now().time()
        else:
            time_of_day_dt = datetime.strptime(time_of_day, "%I:%M %p").time()
        day_of_week_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        # Handle the special case for 'closest'
        if day_of_week.lower() == "closest":
            today_occurrence = datetime.combine(
                last_modified_time.date(), time_of_day_dt
            )
            if today_occurrence > last_modified_time:
                res = today_occurrence
            else:
                res = today_occurrence + timedelta(days=1)
            if week_jump > 0:
                res += timedelta(days=7 * week_jump)
            return res

        if day_of_week.lower() == "now":
            return datetime.now()

        # Find the target day of week as an integer
        target_day = day_of_week_map[day_of_week.lower()]

        # Calculate the next occurrence of the target day of week
        days_ahead = target_day - last_modified_time.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        # Create the next occurrence datetime object
        next_occurrence_date = last_modified_time + timedelta(days=days_ahead)
        next_occurrence = datetime.combine(
            next_occurrence_date.date(), time_of_day_dt
        )

        # If the calculated next occurrence is before or at the last modified time, add 7 days
        if next_occurrence <= last_modified_time:
            next_occurrence += timedelta(days=7)

        if week_jump > 0:
            next_occurrence += timedelta(days=7 * week_jump)

        return next_occurrence

    @staticmethod
    def tonight(time_string, last_modified_time):
        c = CustomTimesNamespace.cfg['tonight']
        ref_time = c['time']

        tokens = time_string.strip().lower().split(' ')
        if len(tokens) > 1:
            ref_time = ' '.join(tokens[1:])

        # Calculate what time today at midnight is
        today = datetime.date.today()
        # now = datetime.now()

        # Read in format in HH:MM AM/PM format relative to today
        # time = datetime.strptime(c['time'], '%I:%M %p'
        time = datetime.strptime(ref_time, '%I:%M %p')
        send_time = datetime.combine(today, time.time())

        return send_time

    @staticmethod
    def night(time_string, last_modified_time):
        c = CustomTimesNamespace.cfg['night']
        ref_time = c['time']

        tokens = time_string.strip().lower().split(' ')

        # Calculate what time today at midnight is
        today = datetime.date.today()
        # now = datetime.now()

        # Read in format in HH:MM AM/PM format relative to today
        # time = datetime.strptime(c['time'], '%I:%M %p'
        if len(tokens) == 1:
            additional_days = 0
        else:
            additional_days = int(tokens[1])
            if len(tokens) > 2:
                ref_time = ' '.join(tokens[2:])
            else:
                ref_time = c['time']
        print(f'{additional_days=}')
        the_time = datetime.strptime(ref_time, '%I:%M %p')
        print(f'{the_time=}')

        # add additional days as specified
        the_time = the_time + datetime.timedelta(days=additional_days)

        send_time = datetime.combine(
            today, the_time.time()
        ) + datetime.timedelta(days=additional_days)

        print(f'{the_time=} {send_time=}')

        return send_time

    @staticmethod
    def now(time_string, last_modified_time):
        return datetime.now()

    @staticmethod
    def plus(time_string, last_modified_time):
        time_string = time_string.replace('+', '')
        day_index = time_string.rfind('d')
        hour_index = time_string.rfind('h')
        minute_index = time_string.rfind('m')

        days = 0 if day_index == -1 else int(time_string[:day_index])
        hours = (
            0
            if hour_index == -1
            else int(time_string[day_index + 1 : hour_index])
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


class TransformProtocols:
    @staticmethod
    def general_mail(last_modified_time, text):
        c = CustomTimesNamespace.cfg
        text = text.strip()
        lines = text.split('\n')
        if len(lines) <= 2:
            return ""

        contact_name, time_str = lines[:2]
        contact_name = contact_name.lower().strip()

        gm = c['general_mail']

        if contact_name not in gm['people'].keys():
            contact_name = 'default'

        if time_str not in gm['people'][contact_name]['time']:
            time_str = 'closest'

        week_jump = gm['people'][contact_name]['week_jump']
        day_of_week = gm['people'][contact_name]['day']
        time_of_day = gm['people'][contact_name]['time']
        header = gm['people'][contact_name]['header']
        width_pad = gm['people'][contact_name]['width_pad']
        height_pad = gm['people'][contact_name]['height_pad']
        raw_header = gm['people'][contact_name]['raw_header']

        send_time = TimeProtocols.leapfrog(
            last_modified_time=last_modified_time,
            time_of_day=time_of_day,
            day_of_week=day_of_week,
            week_jump=week_jump,
        )
        reformatted_text = FormatProtocols.header_list(
            '\n'.join(lines[2:]),
            contact_name=contact_name,
            header=header,
            width_pad=width_pad,
            height_pad=height_pad,
            raw_header=raw_header
        )
        return send_time, reformatted_text


class TransformDispatcher:
    @staticmethod
    def get_dispatch_method(id):
        id = id.lower()
        c = CustomTimesNamespace.cfg
        for k in c.keys():
            aliases = [k] + c[k].get('aliases', [])
            if id in aliases:
                res = getattr(TransformProtocols, k)
                return res
        return None

    @staticmethod
    def dispatch(last_modified_time, text_body):
        callback_id = text_body.strip().lower().split('\n')[1].strip()
        callback = TransformDispatcher.get_dispatch_method(callback_id)
        res = callback(last_modified_time, text_body)
        if '/' not in res[1]:
            print(res[1])
        return res


def main():
    print(
        'custom_times is not meant to be a "true" addon to be executed at command line.'
        'It is meant to be an easy way to extend custom times for scheduling.'
        'An example would be "tonight" to translate to "calculate today at 8:00PM".'
    )

    # test general_mail
    text = """
    Scar
    gm
    Hello this is some text.

    Here is some more.
    @@@IMG 4@@@

    @@@IMG 5@@@

    @@@IMG 6@@@
    Here is another image.
    """
    text = '\n'.join([e.strip() for e in text.strip().split('\n')])
    last_modified_time = datetime.now()
    print("\n\n")
    send_time, reformatted_text = TransformProtocols.general_mail(
        last_modified_time, text
    )

    print(f'{send_time=}\n')
    print(reformatted_text)


if __name__ == "__main__":
    main()

import os
import re
import argparse

PROJECT_PATH = os.path.abspath(
    os.path.relpath(os.path.dirname(__file__), os.getcwd())
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', '-i', help='Input file', default='contacts_direct.yaml'
    )
    parser.add_argument(
        '--output', '-o', help='Output file', default='contacts.txt'
    )
    parser.add_argument(
        '--regenerate',
        '-r',
        help='Regenerate base yaml file',
        action='store_true',
    )
    parser.add_argument(
        '--alphabetical',
        '-a',
        help='Sort contacts alphabetically',
        action='store_true',
    )
    args = parser.parse_args()
    if not args.input.startswith(os.sep):
        args.input = os.path.join(PROJECT_PATH, args.input)
    if not args.output.startswith(os.sep):
        args.output = os.path.join(PROJECT_PATH, args.output)
    return args


def main():
    args = parse_args()
    if args.regenerate or not os.path.exists(args.input):
        print(
            f'Regenerating base contacts and storing in file below'
            f'\n\n    {args.input}\n\n'
            'This may take a minute or two...',
            end='',
            flush=True,
        )
        os.system(
            f'osascript {PROJECT_PATH}/see_contacts.applescript > {args.input}'
        )
        print('Done')
    with open(args.input, 'r') as f:
        lines = f.read().strip().split('\n')
        lines = [e for e in lines if len(e) > 0]
        for i, e in enumerate(lines):
            try:
                key, value = e.split(': ')
                key = key.lower().replace(' ', '_')
            except ValueError:
                print(
                    f'Error in line {i + 1}: {e if len(e) > 0 else "empty line"}'
                )
                raise
            value = re.sub(r'[\(\) +-]', '', value)
            unique_numbers = set(value.split(','))
            for j, number in enumerate(unique_numbers):
                if j == 0:
                    lines[i] = key + ': ' + number
                else:
                    lines[i] += f'\n{key}_{j+1}: {number}'

        # sort the lines by key alphabetically
        if args.alphabetical:
            lines.sort(key=lambda x: x.split(': ')[0])

        try:
            with open(args.output, 'w') as f:
                s = '\n'.join(lines)
                ext = args.output[args.output.rfind('.') :].lower()
                if ext not in ['.yaml', '.yml', '.txt', '.env']:
                    raise ValueError(
                        f'Invalid file extension: {ext}...must be .yaml, .yml, .txt, or .env'
                    )
                elif ext in ['.txt', '.env']:
                    s = s.replace(': ', '=')
                f.write(s)
                print(
                    f'YAML contacts to env contacts format conversion complete.\n'
                    'Copy and paste the contacts you want from the file below into the SETTINGS.txt file.\n\n'
                    f'    {args.output}\n'
                )
        except Exception as e:
            print(f'Error writing to contacts file: {e}')


if __name__ == "__main__":
    main()

import os
import re
import argparse


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
    return parser.parse_args()


def main():
    args = parse_args()
    if args.regenerate or not os.path.exists(args.input):
        print(
            f'Regenerating base contacts and storing in {args.input}...may take a minute or two...',
            end='',
            flush=True,
        )
        os.system(f'osascript see_contacts.applescript > {args.input}')
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


if __name__ == "__main__":
    main()

import time
import pyperclip
import re
import json


def main():
    clipboard_contents = pyperclip.paste()
    clipboard_modified = False
    # Search for: http or https, ://, any of the domains in the (), non-whitespace, literal ?
    question_mark_search = re.compile('https?://(twitter.com|x.com|cdn.discordapp.com)\S+\?')

    clipboard_contents = clipboard_contents.splitlines()
    for index, line in enumerate(clipboard_contents):
        if '//twitter.com' in line:
            clipboard_modified = True
            line = line.replace('twitter.com', 'vxtwitter.com')
            print(f'Replaced: {line}')
        elif '//x.com' in line:
            clipboard_modified = True
            line = line.replace('x.com', 'fixupx.com')
            print(f'Replaced: {line}')
        elif '//www.reddit.com' in line:
            clipboard_modified = True
            line = line.replace('www.reddit.com', 'old.reddit.com')

        # question_mark_matched = re.search(question_mark_search, line)
        # if question_mark_matched:
        if any(x in line for x in ('twitter.com', 'x.com', 'cdn.discordapp.com')) and '?' in line:
            clipboard_modified = True
            line = line.rsplit('?')[0]
            print(f'Replaced: {line}')

        if '/ref' in line and 'amazon.com' in line:
            clipboard_modified = True
            line = line.rsplit('/ref')[0]
            print(f'Replaced: {line}')

        clipboard_contents[index] = line

    if clipboard_modified:
        clipboard_contents = '\n'.join(clipboard_contents)
        pyperclip.copy(clipboard_contents)


def read_config():
    pass


def write_config():
    pass


def replace_text() -> str:
    pass


def strip_partial_line() -> str:
    pass


if __name__ == '__main__':
    while True:
        try:
            main()
            time.sleep(.5)
        except pyperclip.PyperclipWindowsException as e:
            pass

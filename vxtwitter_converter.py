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


def read_config() -> dict:
    with open('config.json', 'r') as f:
        return json.load(f)


def write_config() -> None:
    with open('config.json', 'w') as f:
        __config = {
            'line_replace': [
                {'find': '/twitter.com', 'replace': '/vxtwitter.com'},
                {'find': 'x.com', 'replace': 'fixupx.com'},
                {'find': 'www.reddit.com', 'replace': 'old.reddit.com'}
            ],
            'line_partial_strip': [
                {'urls': ('twitter.com', 'x.com', 'cdn.discordapp.com'), 'characters_to_strip_after': '?'},
                {'urls': ('amazon.com', 'amazon.ca'), 'characters_to_strip_after': '/ref'}]
        }
        json.dump(__config, f, indent=4)


def replace_text(__config: dict, __clipboard_input: str) -> str:
    """Find/replace using the config as rules"""
    changed_text = ''
    for find_replace_rule in __config['line_replace']:
        if find_replace_rule['find'] in __clipboard_input:
            changed_text = __clipboard_input.replace(find_replace_rule['find'], find_replace_rule['replace'])
            # Stop because the intent is only to match one rule
            break
    return changed_text or __clipboard_input


def strip_partial_line(__config: dict, __clipboard_input: str) -> str:
    changed_text = ''
    for strip_partial_line_rule in __config['line_partial_strip']:
        if any(x in __clipboard_input for x in strip_partial_line_rule['urls']) \
                and strip_partial_line_rule['characters_to_strip_after'] in __clipboard_input:
            __clipboard_input = __clipboard_input.rsplit(strip_partial_line_rule['characters_to_strip_after'])[0]
    return changed_text or __clipboard_input


def clipboard_scan_and_replace(__config):
    clipboard_contents = pyperclip.paste()
    # print(clipboard_contents)
    modified_clipboard = clipboard_contents

    modified_clipboard = replace_text(config, modified_clipboard)
    modified_clipboard = strip_partial_line(config, modified_clipboard)
    # print(f'returned: {replace_text(config, modified_clipboard)}')

    # Only update the clipboard if it's been changed
    if clipboard_contents != modified_clipboard:
        pyperclip.copy(modified_clipboard)
        print(f'Modified: {modified_clipboard}')


if __name__ == '__main__':
    # old = True
    old = False
    if old:
        while True:
            try:
                main()
                time.sleep(.5)
            except pyperclip.PyperclipWindowsException as e:
                print(e)
    else:
        write_config()
        config = read_config()

        while True:
            try:
                clipboard_scan_and_replace(config)
                time.sleep(.5)

            except pyperclip.PyperclipWindowsException as e:
                print(e)


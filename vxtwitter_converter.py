import time
import pyperclip
import re
import json
from pprint import pprint


def read_config(__config_file_name='config.json') -> dict:
    with open(__config_file_name, 'r') as f:
        return json.load(f)


def write_config() -> None:
    with open('config.json', 'w') as f:
        __config = {
            'clipboard_monitor_interval': '.5',
            'line_replace': [
                {'find': '/twitter.com', 'replace': '/vxtwitter.com'},
                {'find': '/x.com', 'replace': '/fixupx.com'},
                {'find': 'www.reddit.com', 'replace': 'old.reddit.com'},
                {'find': 'www.furaffinity.net', 'replace': 'www.fxfuraffinity.net'},
            ],
            'line_partial_strip': [
                {'urls': ('twitter.com', 'x.com',), 'characters_to_strip_after': '?'},
                {'urls': ('amazon.com', 'amazon.ca'), 'characters_to_strip_after': '/ref'},
                {'urls': ('amazon.com', 'amazon.ca'), 'characters_to_strip_after': '?ref'},
                {'urls': ('amazon.com', 'amazon.ca'), 'characters_to_strip_after': '&ref'}]
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
    """Looks for characters from config and strips the str after them"""
    changed_text = ''
    for strip_partial_line_rule in __config['line_partial_strip']:
        if any(x in __clipboard_input for x in strip_partial_line_rule['urls']) \
                and strip_partial_line_rule['characters_to_strip_after'] in __clipboard_input:
            __clipboard_input = __clipboard_input.rsplit(strip_partial_line_rule['characters_to_strip_after'])[0]
    return changed_text or __clipboard_input


def clipboard_scan_and_replace(__config) -> None:
    """Main loop function, updates the clipboard"""
    clipboard_contents = pyperclip.paste()
    # print(clipboard_contents)
    modified_clipboard = clipboard_contents

    modified_clipboard = replace_text(__config, modified_clipboard)
    modified_clipboard = strip_partial_line(__config, modified_clipboard)
    # print(f'returned: {replace_text(config, modified_clipboard)}')

    # Only update the clipboard if it's been changed
    if clipboard_contents != modified_clipboard:
        pyperclip.copy(modified_clipboard)
        print(f'Modified: {modified_clipboard}')


if __name__ == '__main__':
    write_config()
    config = read_config()
    print('Loaded rules:')
    pprint(config, width=120)
    print(f'Now scanning clipboard every {config['clipboard_monitor_interval']}s')

    while True:
        try:
            clipboard_scan_and_replace(config)
            time.sleep(float(config['clipboard_monitor_interval']))

        except pyperclip.PyperclipWindowsException as e:
            print(e)


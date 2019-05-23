#!/usr/bin/env python3

from tkinter import *
import os
import re
import secretstorage
import subprocess
import sys
import time

browsers = {
    '/usr/lib/chromium/chromium',
    '/usr/lib/firefox/firefox',
}

os.environ["DISPLAY"] = ':0.0'
os.environ["XAUTHORITY"] = os.path.join(os.getenv('HOME'), '.Xauthority')

path = os.path.dirname(os.path.realpath(__file__))
err = open(os.path.join(path, 'stderr'), 'a')

def backtick(*args):
    return subprocess.check_output([*args], stderr=err).decode('UTF-8').strip()

def xdotool(*args):
    subprocess.call(['xdotool', *args], stderr=err)

window_id = backtick('xdotool', 'getwindowfocus')
window_pid = backtick('xdotool', 'getwindowfocus', 'getwindowpid')
window_exe = backtick('readlink', '-f', os.path.join('/proc', str(int(window_pid)), 'exe'))

def emit_password(item):
    xdotool('windowactivate', window_id)
    time.sleep(0.05)
    attrs = item.get_attributes()
    if 'login' in attrs:
        xdotool('type', attrs['login'])
        if window_exe in browsers:
            xdotool('key', 'Tab')
        else:
            xdotool('key', 'Return')
    xdotool('type', item.get_secret())
    xdotool('key', 'Return')

connection = secretstorage.dbus_init()

collection = secretstorage.get_default_collection(connection)
if collection.is_locked():
    collection.unlock()

window = Tk()
window.title('passworder')

listbox = Listbox(window)

items = []
for item in collection.search_items({'service': 'passworder'}):
    items.append(item)
    items.sort(key=lambda x: x.get_label())

for item in items:
    listbox.insert(END, item.get_label())

listbox.pack()

listbox.select_set(0)
listbox.focus_force()

def use_item():
    idx = listbox.curselection()[0]
    window.withdraw()
    emit_password(items[idx])
    window.quit()

def double_click(event):
    use_item()

def key_enter(event):
    xdotool('keyup', 'Return')
    use_item()

def key_escape(event):
    xdotool('windowactivate', window_id)
    window.quit()

listbox.bind("<Double-Button-1>", double_click)
window.bind("<Key-Return>", key_enter)
window.bind("<Key-Escape>", key_escape)

window.mainloop()
err.flush()

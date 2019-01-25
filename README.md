### passworder

Small script that autotypes passwords.

It fetches passwords via D-Bus Secrets API from your keystore (I use GNOME Keyring),
presents them in a simple listbox and types selected one using xdotool.

Keybindings:
- `Return` selects item
- `Escape` closes window

Use `addpw.py` to add passwords. Passwords may have logins attached to them. If present, passworder will type them first.
It detects browsers (currently only Chromium) and separates login from password with single `Tab` key stroke (`Return` is used for everything else, eg terminals).
Password itself is also followed by `Return` key.

Dependencies:
  - secretstorage
  - Tk
  - xdotool

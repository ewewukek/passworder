#!/usr/bin/env python3

from getpass import getpass
import secretstorage

connection = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(connection)
if collection.is_locked():
    collection.unlock()

name = input("name: ")
login = input("login: ")
password = getpass("password: ")

attrs = {'service': 'passworder', 'name': name}
if login != '':
    attrs['login'] = login

collection.create_item(name, attrs, password, replace=True)

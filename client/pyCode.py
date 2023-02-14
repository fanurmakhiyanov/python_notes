import sys
from core.Note import Note
import core.NotesList
import json
from core.functions import checkCommand
from core.functions import execute


def main_loop():
    while True:
        print('Введите команду (commands - для вывода списка команд)')
        command = input().lower()
        if checkCommand(command):
            execute(command)
        else:
            print('Ошибочная команда')
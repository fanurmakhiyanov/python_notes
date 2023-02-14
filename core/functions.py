import sys
from core.Note import Note
import core.NotesList
import json
import datetime
import core.functions

global COMMANDS, NOTE_LIST, ID
ID = 0
COMMANDS = ['commands', 'read', 'find', 'add', 'list', 'change', 'remove', 'save', 'load', "exit"]
NOTE_LIST = []


def execute(command):
    global ID, NOTE_LIST
    if command == 'commands':
        print(COMMANDS)

    if command == 'add':
        new_note = Note(ID)
        ID = ID + 1
        new_note.title = input('Введите заголовок: ')
        new_note.body = input('Введите текст заметки: ')
        NOTE_LIST.append(new_note)
        print('Заметка сохранена. Команда "Save" для сохранения перед выходом')

    if command == "list":
        listNotes(NOTE_LIST)

    if command == "change":
        id = transform(input("Введите ID заметки для обновления: "))
        isExist = False
        for i in range(len(NOTE_LIST)):
            if NOTE_LIST[i].id == id:
                changeNote(NOTE_LIST[i])
                isExist = True
        if not isExist:
            print('Заметки с таким ID не существует, используйте list, чтобы просмотреть ID существующих заметок')

    if command == 'remove':
        id = transform(input("Введите ID заметки для удаления: "))
        isExist = False
        for note in NOTE_LIST:
            if note.id == id:
                NOTE_LIST.remove(note)
                isExist = True
        if not isExist:
            print('Заметки с таким ID не существует, используйте list, чтобы просмотреть ID существующих заметок')

    if command == 'save':
        isCorrect = False
        while not isCorrect:
            print('Введите путь к файлу, для сохранения (оставьте пустым для сохранения по умолчанию)')
            path = input()
            isCorrect = True
            try:
                if path == "": path = 'savedata.json'
                save(path)
                isCorrect = True
            except:
                print('Путь некорректен/недоступен')
        print("Сохранено")

    if command == 'load':
        isCorrect = False
        while not isCorrect:
            print('Введите путь к файлу, для загрузки (оставьте пустым для сохранения по умолчанию)')
            path = input()
            isCorrect = True
            try:
                if path == "": path = 'savedata.json'
                load(path)
                isCorrect = True
            except:
                print('Путь некорректен/недоступен')
        print("Загружено")

    if command == 'find':
        findByDate()

    if command == 'read':
        id = transform(input("Введите ID заметки для чтения: "))
        isExist = False
        for i in range(len(NOTE_LIST)):
            if NOTE_LIST[i].id == id:
                note = NOTE_LIST[i]
                print(
                    f'Заметка ID#{note.id} под заголовком "{note.title}" сообщает "{note.body}". Последнее изменение {note.date} в {note.time}.')
                isExist = True
        if not isExist:
            print('Заметки с таким ID не существует, используйте list, чтобы просмотреть ID существующих заметок')

    if command == 'exit':
        exit = input('Убедитесь, что изменения были сохранены. Введите "exit" повторно для закрытия программы:  ')
        if exit == 'exit':
            sys.exit()


def checkCommand(command):
    return command in COMMANDS


def changeNote(note):
    print(note.title)
    new_title = input("Введите новый заголовок (оставьте пустым, чтобы не вносить изменения): ")
    if not new_title == "":
        note.title = new_title
        note.updateDate()
    print(note.body)
    new_body = input("Введите новый текст заметки (оставьте пустым, чтобы не вносить изменения): ")
    if not new_body == "":
        note.body = new_body
        note.updateDate()


def transform(inp):
    try:
        return int(inp)
    except:
        print("Введено некорректное число")
        return inp


def listNotes(note_list):
    for note in note_list:
        print(str(note))


def save(path):
    global NOTE_LIST
    with open(path, "w") as save_file:
        save_file.write('[\n')
        for note in NOTE_LIST:
            json_string = json.dumps(note.dictionaryJson(), ensure_ascii=False)
            save_file.write(json_string + ',\n')
        save_file.write(']')
    save_file.close()


def load(path):
    global NOTE_LIST, ID
    NOTE_LIST = []
    ID = 0
    used_id = []
    with open("savedata.json", "r") as file:
        parsed_data = json.load(file)
    for el in parsed_data:
        if el['id'] in used_id:
            print('Данные с повторяющимися ID, ошибка')
            break
        used_id.append(el['id'])
        loaded_note = Note(int(el['id']))
        loaded_note.title = el['title']
        loaded_note.body = el['body']
        loaded_note.time = datetime.datetime.strptime(el['time'], '%H:%M:%S')
        loaded_note.date = datetime.datetime.strptime(el['date'], '%Y-%m-%d')
        NOTE_LIST.append(loaded_note)

    ID = max(used_id)


def findByDate():
    global NOTE_LIST
    isCorrect = False
    while not isCorrect:
        date = input('Введите дату, после которой изменена заметка в формате DD/MM/YY: ')
        try:
            date_min = datetime.datetime.strptime(date, '%d/%m/%y').date()
            isCorrect = True
        except ValueError:
            print('Некорректная дата')

    isCorrect = False
    while not isCorrect:
        date = input('Введите дату, до которой изменена заметка в формате DD/MM/YY: ')
        try:
            date_max = datetime.datetime.strptime(date, '%d/%m/%y').date()
            isCorrect = True
        except ValueError:
            print('Некорректная дата')

    notes_subset = []
    for note in NOTE_LIST:
        date_of_note = note.date
        if (date_of_note >= date_min) and (date_of_note <= date_max):
            notes_subset.append(note)
    listNotes(notes_subset)
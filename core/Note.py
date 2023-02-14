from datetime import datetime
from datetime import date

import json


class Note:
    def __init__(self, id):
        self.id = id
        self.title = "Default title"
        self.body = "Some task"
        self.time = datetime.now().strftime("%H:%M:%S")
        self.date = date.today()

    def __str__(self) -> str:
        return f"#{self.id} от {str(self.date)}: {self.title}"

    def __repr__(self) -> str:
        keys = ["id", "title", 'body', 'time', 'date']
        values = [self.id, self.title, self.body, self.time, str(self.date)]
        return json.dumps(dict(zip(keys, values)), ensure_ascii=False)
        # return  dict(zip(keys, values))

    def dictionaryJson(self):
        keys = ["id", "title", 'body', 'time', 'date']
        values = [self.id, self.title, self.body, self.time, str(self.date)]
        return dict(zip(keys, values))

    def updateDate(self):
        self.time = datetime.now().strftime("%H:%M:%S")
        self.date = date.today()
import datetime
from abc import ABC
from abc import abstractmethod
import sqlite3

from myhome_schedule_bot.domain.entity import LastAppartment


class IRepository(ABC):
    @abstractmethod
    def add(self, obj: LastAppartment) -> None:
        ...

    @abstractmethod
    def get(self, id: str) -> LastAppartment:
        ...


class Repository(IRepository):
    def __init__(self):
        self.__con = sqlite3.connect("database.db")

    def migrate(self):
        self.__con.cursor().execute("""CREATE TABLE IF NOT EXISTS myhome (
	                        id integer PRIMARY KEY AUTOINCREMENT,
	                        myhome_id integer unique,
	                        add_time int,
	                        url text
                            );
                        """)

    def add(self, obj: LastAppartment) -> None:
        try:
            self.__con.cursor().execute('INSERT INTO myhome(myhome_id,add_time,url) VALUES (?,?,?)',
                                        (obj.Id, obj.AddDate.timestamp(), obj.Url))
            self.__con.commit()
        except Exception as e:
            print(f"{obj.Id} already exists")

    def get(self, id: str) -> LastAppartment:
        cur = self.__con.cursor()
        cur.execute('SELECT * FROM myhome WHERE myhome_id = ?', (id,))
        raw = cur.fetchone()
        if not raw:
            return None
        return LastAppartment(Id=raw[1], AddDate=datetime.datetime.fromtimestamp(raw[2]), Url=raw[3])

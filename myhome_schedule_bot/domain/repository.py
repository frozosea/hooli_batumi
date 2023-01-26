from abc import ABC
from abc import abstractmethod
import sqlite3

from entity import LastAppartment


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
	                        myhome_id integer,
	                        add_time datetime
                            );
                        """)

    def add(self, obj: LastAppartment) -> None:
        self.__con.cursor().execute('INSERT INTO myhome(myhome_id,add_time) VALUES (?,?)', (obj.Id, obj.AddDate))
        self.__con.commit()

    def get(self, id: str) -> LastAppartment:
        cur = self.__con.cursor()
        cur.execute('SELECT FROM myhome WHERE myhome_id = ?', (id,))
        raw = cur.fetchone()
        if len(raw) == 0:
            return None
        return LastAppartment(raw[1], raw[2])

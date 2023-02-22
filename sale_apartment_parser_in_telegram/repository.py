import sqlite3
from abc import ABC
from abc import abstractmethod


class IRepository(ABC):
    @abstractmethod
    def add(self, message: str) -> int:
        ...

    @abstractmethod
    def delete_all(self) -> None:
        ...

    @abstractmethod
    def exists(self, message: str) -> bool:
        ...


class Repository(IRepository):
    def __init__(self):
        self.__con = sqlite3.connect("database.db")

    def migrate(self) -> IRepository:
        self.__con.cursor().execute("""CREATE TABLE IF NOT EXISTS messages (
	                        id integer PRIMARY KEY AUTOINCREMENT,
	                        message text
                            );"""
                                    )
        return self

    def add(self, message: str) -> int:
        try:
            self.__con.cursor().execute('INSERT INTO messages(message) VALUES (?)',
                                        (message.lower(),))
            self.__con.commit()
        except Exception as e:
            print(e)
            print(f"already exists")

    def exists(self, message: str) -> bool:
        cur = self.__con.cursor()
        cur.execute('SELECT * FROM messages WHERE message = ?', (message.lower(),))
        raw = cur.fetchone()
        return True if raw else False

    def delete_all(self) -> None:
        self.__con.cursor().execute('DROP TABLE IF EXISTS messages')
        self.__con.commit()
        self.migrate()


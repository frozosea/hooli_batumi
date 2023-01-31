import random
from typing import List
from abc import ABC
from abc import abstractmethod
import sqlite3

from entity import LastAppartment
from entity import AddTask


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

    def migrate(self) -> IRepository:
        self.__con.cursor().execute("""CREATE TABLE IF NOT EXISTS ss (
	                        id integer PRIMARY KEY AUTOINCREMENT,
	                        ss_id integer unique,
	                        url text
                            );
                        """)
        return self

    def add(self, obj: LastAppartment) -> None:
        try:
            self.__con.cursor().execute('INSERT INTO ss(ss_id,url) VALUES (?,?)',
                                        (obj.Id, obj.Url,))
            self.__con.commit()
        except Exception as e:
            print(f"{obj.Id} already exists")

    def get(self, id: str) -> LastAppartment:
        cur = self.__con.cursor()
        cur.execute('SELECT * FROM ss WHERE ss_id = ?', (id,))
        raw = cur.fetchone()
        if not raw:
            return None
        return LastAppartment(Id=raw[1], Url=raw[2])


class ICronRepository(ABC):
    @abstractmethod
    def add_job(self, task: AddTask) -> None:
        ...

    @abstractmethod
    def get_jobs(self) -> List[AddTask]:
        ...


class CronRepository(ICronRepository):
    def __init__(self):
        self.__con = sqlite3.connect("database.db")

    def migrate(self) -> ICronRepository:
        self.__con.cursor().execute("""CREATE TABLE IF NOT EXISTS jobs(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    url text,
                                    group_id int
                                    );""")
        return self

    def add_job(self, task: AddTask) -> None:
        try:
            self.__con.cursor().execute('INSERT INTO jobs(url,group_id) VALUES (?,?)',
                                        (task.Url, task.GroupId,))
            self.__con.commit()
        except Exception as e:
            print(f"{task.GroupId} already exists")

    def get_jobs(self) -> List[AddTask]:
        cur = self.__con.cursor()
        cur.execute('SELECT * FROM jobs')
        all = cur.fetchall()
        if len(all) > 0:
            return [AddTask(Url=item[1], GroupId=item[2]) for item in all]
        return []


class IProxyRepository(ABC):
    @abstractmethod
    def get(self) -> str:
        ...


class ProxyRepository(IProxyRepository):
    def __init__(self, proxies: List[str]):
        self.__proxies = proxies

    def get(self) -> str:
        return self.__proxies[random.Random().randint(0, len(self.__proxies) - 1)]

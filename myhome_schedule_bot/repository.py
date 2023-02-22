import random
import sqlite3
from abc import ABC
from typing import List
from abc import abstractmethod

from entity import AddTask
from entity import Apartment


class IRepository(ABC):
    @abstractmethod
    def add(self, obj: Apartment) -> None:
        ...

    @abstractmethod
    def check_exists(self, id: str) -> bool:
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
        self.__con.commit()
        return self

    def add(self, obj: Apartment) -> None:
        try:
            self.__con.cursor().execute('INSERT INTO myhome(myhome_id,add_time,url) VALUES (?,?,?)',
                                        (obj.Id, obj.AddDate.timestamp(), obj.Url))
            self.__con.commit()
        except Exception as e:
            print(f"{obj.Id} already exists")

    def check_exists(self, id: str) -> bool:
        cur = self.__con.cursor()
        cur.execute('SELECT * FROM myhome WHERE myhome_id = ?', (id,))
        raw = cur.fetchone()
        if not raw:
            return False
        return True


class ICronRepository(ABC):
    @abstractmethod
    def add_job(self, task: AddTask) -> None:
        ...

    @abstractmethod
    def get_jobs(self) -> List[AddTask]:
        ...

    @abstractmethod
    def delete(self, id: str) -> None:
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

    def delete(self, id: str) -> None:
        try:
            self.__con.cursor().execute('DELETE FROM jobs WHERE group_id = ?',
                                        (id,))
            self.__con.commit()
        except Exception as e:
            print(f"{id} cannot delete error: {e}")


class IProxyRepository(ABC):
    @abstractmethod
    def get(self) -> str:
        ...


class ProxyRepository(IProxyRepository):
    def __init__(self, proxies: List[str]):
        self.__proxies = proxies

    def get(self) -> str:
        return self.__proxies[random.Random().randint(0, len(self.__proxies) - 1)]

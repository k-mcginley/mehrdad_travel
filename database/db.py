import random
from typing import Tuple
import sqlite3

class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("./database/holidays.db")
        self.__cursor = self.__conn.cursor()
    
    def add_new_customer(self, forename: str, surname: str, telephone: str):
        id = forename[0] + surname[:2] + str(random.randint(100, 999))

        self.__cursor.execute(f"INSERT INTO CUSTOMER VALUES ('{id}', '{forename}', '{surname}', '{telephone}')")

        self.__conn.commit()

    def get_all_customers(self) -> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM CUSTOMER").fetchall()

        return records
        

db = Database()

if __name__ == "__main__":
    db.add_new_customer("Martin", "Davies", "+85212345678")

    print(db.get_all_customers())
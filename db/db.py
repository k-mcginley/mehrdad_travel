from typing import Tuple
from random import randint
import sqlite3

# test


class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("./db/holidays.db")
        self.__cursor = self.__conn.cursor()
    
    def add_new_customer(self, forename: str, surname: str, telephone: str):
        id_ = forename[0] + surname[:2].upper() + str(randint(111, 999))

        self.__cursor.execute(f"INSERT INTO Customer VALUES ('{id_}', '{forename}', '{surname}', '{telephone}')")

        self.__conn.commit()

    def get_all_customers(self) -> Tuple[Tuple]:
    
        records = self.__cursor.execute("SELECT * FROM Customer").fetchall()

        return records
    


        


db = Database()


if __name__ == "__main__":
    # tests
    db.add_new_customer("Martin", "Davies", "+8524561845123")
    print(db.get_all_customers())

    # should see martin davies
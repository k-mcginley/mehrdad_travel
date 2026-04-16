import random
from typing import Tuple
import sqlite3

class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("./database/holidays.db")
        self.__cursor = self.__conn.cursor()
    
    
    def close(self):
        self.__conn.close()


    def add_new_customer(self, forename: str, surname: str, telephone: str):
        id = forename[0] + surname[:2] + str(random.randint(100, 999))

        self.__cursor.execute(f"INSERT INTO Customer VALUES ('{id}', '{forename}', '{surname}', '{telephone}')")

        self.__conn.commit()


    def delete_customer(self, id: str):
        self.__cursor.execute(f"DELETE FROM Customer WHERE CustomerID = ?", (id,)).fetchall()



    def get_all_customers(self) -> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM Customer").fetchall()

        return records
        

    def get_holidays(self, location: str) -> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM Holiday WHERE Location = ?", (location,)).fetchall()
        
        return records


    def book_holidays(self, customer_id):
        booking_id = "BK"
        self.__cursor.execute(f"INSERT INTO Booking VALUES ('{booking_id}')")

db = Database()

if __name__ == "__main__":
    # tests

    print(db.get_holidays("New York"))


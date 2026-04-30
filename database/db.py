import random
from typing import Tuple
import sqlite3
from models import Holiday, Customer, Booking, Guest, Allergen, Food

class DatabaseError(Exception):
    pass

class Database:
    def __enter__(self):
        self.__conn = sqlite3.connect("./database/holidays.db")
        self.__cursor = self.__conn.cursor()
        return self
    
    
    def __exit__(self, *args):
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
        

    def get_holidays_by_location(self, location: str) -> Tuple[Holiday]:
        records = self.__cursor.execute("SELECT * FROM Holiday WHERE Location = ?", (location,)).fetchall()
        
        return [Holiday(*record) for record in records]


    def book_holidays(self, customer_id):
        booking_id = "BK"
        self.__cursor.execute(f"INSERT INTO Booking VALUES ('{booking_id}')")

    
    def get_holiday_by_id(self, holiday_id) -> Holiday | None:
        # TODO
        record = self.__cursor.execute("SELECT * FROM Holiday WHERE HolidayId = ?", (holiday_id,)).fetchone()
        return Holiday(*record)


    def create_new_customer(self, forename: str, surname: str, telephone: str) -> Customer:
        '''work out new customer's id
        write new customer to database
        return new Customer object'''

    
    def get_customer_by_names(self, forename: str, surname: str) -> Customer | None:
        '''look in database to find customer
        if exists return customer as customer
        if doesnt return None'''


    def get_allergen_by_name(self, allergen_name) -> Allergen | None:
        '''look in database to find an allergen
        if exists return allergen object
        if doesn't return None'''


    def create_new_guest(self, guest_name: str, allergies: list[Allergen], food: Food) -> Guest:
        '''write new guest to database (primary key will be made automatically)
        return new guest as Guest'''


    def create_new_booking(self, customer_id: str, holiday_id: str) -> Booking:
        '''write new booking to the database
        return the new booking as a Booking'''


    def get_food_choice_by_name(self, food_choice: str) -> Food:
        pass


    def process_booking(self, form_data) -> tuple[Customer, Booking, list[Guest]]:
        '''validates that data received from front end is acceptable, 
        return models if valid, otherwise raise exception'''

        # check if id exists and is in database
        holiday_id = form_data.get("holiday_id")
        forename = form_data.get("forename")
        surname = form_data.get("surname")
        telephone = form_data.get("telephone")
        guests = form_data.get("guests")

        if holiday_id is None:
            raise AttributeError("holiday_id was not found")
        
        if not isinstance(holiday_id, str):
            raise TypeError("holiday_id not a string")

        holiday = self.get_holiday_by_id(holiday_id)

        if not holiday:
            raise DatabaseError(f"holiday_id {holiday_id} not found in database")


        if not forename:
            raise DatabaseError(f"forename {forename} not found in database")
        
        if not isinstance(forename, str):
            raise TypeError("forename not a string")
        
        
        if not surname:
            raise DatabaseError(f"surname {surname} not found in database")
        
        if not isinstance(surname, str):
            raise TypeError("surname not a string")


        # if yes make customer object
        customer = self.get_customer_by_names(forename, surname)
        if customer is None:
            customer = self.create_new_customer           # if phone num doesnt match then update

        
        booking = self.create_new_booking(customer.id, holiday.id)
        
        # check if geust data present
        if not guests:
            raise AttributeError("guest data missing from post request")
        
        if not isinstance(guests, list):
            raise TypeError("guests is not a list")
        

        for guest in guests:

            # TODO: client deals with missing data/duplicates
            # assume everything OK (guest names)if we got to this point

            name = guest.get("name")
            meal = guest.get("meal")
            allergies = guest.get("allergies")

            if not meal:
                raise AttributeError(f"guest {name}'s meal missing from post request data")

            if not allergies:
                raise AttributeError(f"guest {name}'s allergies missing from post request data")

        # make list of guest objects


    
    
        return holiday, customer, booking, guests, allergies


if __name__ == "__main__":
    # tests

    pass


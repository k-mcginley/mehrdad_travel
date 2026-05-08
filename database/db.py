import random
from typing import Tuple
import sqlite3


import sys
from pathlib import Path

# Path to the directory of the current script
current_dir = Path(__file__).resolve().parent

# Add the parent directory (one level up) to sys.path
sys.path.append(str(current_dir.parent))

from models import *

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
        self.__conn.commit()

    
    def get_holiday_by_id(self, holiday_id) -> Holiday | None:
        record = self.__cursor.execute("SELECT * FROM Holiday WHERE HolidayId = ?", (holiday_id,)).fetchone()
        return Holiday(*record)


    def create_new_customer(self, forename: str, surname: str, telephone: str) -> Customer:
        '''work out new customer's id
        write new customer to database
        return new Customer object'''
        id = forename[0] + surname[:1] + str(random.randint(0, 999)).zfill(3)
        self.__cursor.execute(f"INSERT INTO Customer VALUES ('{id}', '{forename}', '{surname}', '{telephone}')")
        self.__conn.commit()
        return Customer(id, forename, surname, telephone)

    
    def get_customer_by_names(self, forename: str, surname: str) -> Customer | None:
        '''look in database to find customer
        if exists return customer as Customer
        if doesnt return None'''
        record = self.__cursor.execute(f"SELECT * FROM Customer WHERE Forename = '{forename}' AND Surname = '{surname}'").fetchone()
        if record:
            return Customer(*record)
        return None


    def get_allergen_by_name(self, allergen_name) -> Allergen | None:
        '''look in database to find an allergen
        if exists return allergen object
        if doesn't return None'''
        record = self.__cursor.execute(f"SELECT * FROM Allergen WHERE AllergenName = '{allergen_name}'").fetchone()
        if record:
            return Allergen(*record)
        return None


    def create_new_guest(self, booking: Booking, guest_name: str, allergies: list[Allergen], meal: Food) -> Guest:
        '''write new guest to database (primary key will be made automatically)
        associate new guest with their allergies
        return new guest as Guest'''
        guest_id = self.__cursor.execute("INSERT INTO Guest VALUES (NULL, ?, ?) RETURNING Guest.GuestID", (booking.id, guest_name)).fetchone()[0]
        self.__conn.commit()

        query = ""
        for allergen in allergies:
            query += f"INSERT INTO GUEST_ALLERGEN VALUES ({guest_id}, {allergen.id}),"
        print(query)
        self.__cursor.execute(query[:-1])
        self.__conn.commit()

        return Guest(guest_id, booking, guest_name, allergies, meal)


    def finalise_new_booking(self, booking: Booking, 
                             customer: Customer, 
                             holiday: Holiday) -> Booking:
        '''finalise the new booking by adding it to the database
        return the finalised booking as a Booking'''
        booking.id = str(random.randint(0, 999999)).zfill(6)
        booking.customer_id = customer.id
        booking.holiday_id = holiday.id

        self.__cursor.execute((f"INSERT INTO Booking VALUES ('{booking.id}', '{customer.id}', '{holiday.id}', {len(booking.guests)})"))
        self.__conn.commit()
        return booking


    def add_new_guest(self, booking: Booking, new_guest: Guest) -> Booking:
        booking.guests.append(Guest)
        return booking

    
    def create_new_food_choice(self, guest: Guest, food_choice: str):
        food_id = self.__cursor.execute("INSERT INTO GUEST_FOOD VALUES (NULL, ?, ?) RETURNING GUEST_FOOD.FoodID", (guest.id, food_choice)).fetchone()
        self.__conn.commit()

        return Food(food_id, guest, food_choice)


    def get_food_choice_by_name(self, food_choice: str) -> Food:
        record = self.__cursor.execute(f"SELECT * FROM GUEST_FOOD WHERE FoodChoice = '{food_choice}'").fetchone()
        if record:
            return Food(*record)
        return None


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

        
        #booking = self.create_new_booking(customer, holiday)
        booking = Booking()


        
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
            allergens: list[str] = guest.get("allergens")

            if not name:
                raise AttributeError(f"guest name missing from post request data")

            if not meal:
                raise AttributeError(f"guest {name}'s meal missing from post request data")
                

            if allergens is None:
                raise AttributeError(f"guest {name}'s allergies missing from post request data")
            
            valid_allergens: list[Allergen] = []
            for allergen in allergens:
                allergen = self.get_allergen_by_name(allergen)
                if not allergen:
                    raise DatabaseError(f"allergen {allergen} does not exist in database")
                valid_allergens.append(allergen)
                
            guest = self.create_new_guest(booking, name, valid_allergens, meal)
            booking = self.add_new_guest(guest)
            food_choice = self.create_new_food_choice(guest, meal)

        booking = self.finalise_new_booking(booking, customer, holiday)

        return booking


def tests():
    with Database() as db:
        x = db.create_new_customer("Testy", "Testington", "12345678")
        assert type(x) == Customer
        assert x.forename == "Testy"


tests()


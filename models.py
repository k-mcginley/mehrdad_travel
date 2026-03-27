from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class Holiday:
    duration: int
    id: str
    location: str
    departure_date: date

@dataclass
class Customer:
    forename: str
    surname: str
    id: str
    telephone: str

@dataclass
class Booking:
    customer: Customer
    holiday: Holiday

@dataclass
class Flight:
    airline: str
    flight_number: str
    departure_time: datetime
    duration: int
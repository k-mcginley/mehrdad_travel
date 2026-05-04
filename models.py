from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class Holiday:
    id: str
    location: str=""
    departure_date: date=None
    duration: int=0
    outbound_plane_id: str=""
    return_plane_id: str=""

    def __post_init(self):          # validation
        '''
        if len(self.id) != 6 or not self.id[:2].isalpha() or not self.id[3:].isdigit():
            raise Exception(f"Invalid holiday id: {self.id}")
        if len(self.outbound_plane_id) != 5 or not self.outbound_plane_id[:1].isalpha() or not self.outbound_plane_id[2:].isdigit():
            raise Exception(f"Invalid outbound plane id: {self.outbound_plane_id}")
        if len(self.return_plane_id) != 5 or not self.return_plane_id[:1].isalpha() or not self.return_plane_id[2:].isdigit():
            raise Exception(f"Invalid return plane id: {self.return_plane_id}")
        '''
        if len(self.id) != 5:
            raise Exception(f"Invalid holiday id {self.id}")



@dataclass
class Customer:
    id: str
    forename: str
    surname: str
    telephone_number: str
    
@dataclass
class Booking:
    id: str
    customer: Customer
    holiday: Holiday
    guests: list[Guest]=None

@dataclass
class Allergen:
    id: int
    name: str

@dataclass
class Guest:
    id: int
    booking: Booking
    name: str
    allergens: list[Allergen]

@dataclass
class Food:
    id: int
    guest: Guest
    choice: str

@dataclass
class PlaneJourney:
    id: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    airline: str
    duration: int


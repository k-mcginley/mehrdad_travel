from pyodide.http import pyfetch
from json import dumps

async def post_request_booking(booking_data: dict):

    print(booking_data)
    print(type(booking_data))
    
    response = await pyfetch("/api/bookings/new", 
                             method="POST", 
                             headers={"Content-Type": "application/json"}, 
                             body = dumps(booking_data))
    data = await response.json()

    return data


async def get_request_holidays(location):

    location = location.replace(" ", "%20")

    response = await pyfetch(f"/api/holidays?location={location}")     # end point to allow server to respond
    data = await response.json()
    return data
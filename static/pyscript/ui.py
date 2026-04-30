from pyscript import document, when, display

from api import get_request_holidays, post_request_booking

from dto import parse_booking, parse_guest

@when("change", "#trip")
def select_holiday(e):
    form = document.getElementsByClassName("booking")[0]
    inputs = form.querySelectorAll("input, button, select")

    for input_ in inputs:
        input_.disabled = False


def create_booking() -> dict:
    # get stuff from fields
    cust_name = document.getElementById("cust-name").value
    cust_tel = document.getElementById("cust-tel").value
    guest_name = document.getElementById("guest1").value
    guest_meal = document.getElementById("meal").value
    allergies = [allergy.name for allergy in \
                 document.querySelectorAll('input[type="checkbox"]') \
                    if allergy.checked]

    holiday_id = document.getElementById("trip").value

    # TODO: come back to multiple guests later

    guest = parse_guest(guest_name, allergies, guest_meal)

    guests = [guest]

    booking = parse_booking(cust_name, cust_tel, holiday_id, guests)

    return booking


@when("click", "#book_holiday")
async def click_book_holiday(e):
    '''Triggers request to add new booking to database'''
    booking = create_booking()
    feedback = await post_request_booking(booking)

    display(feedback)


# @when()
def click_add_another_guest():
    '''Duplicates customer form for another guest'''
    pass
    

def save_for_later():
    '''Save partially completed form using cookies'''
    pass


@when("click", ".search-cta")
async def click_go(e):
    '''Triggers request to database to find holidays matching 
    the location the user enters'''
    location_input = document.getElementById("dest")
    location = location_input.value
    holidays = await get_request_holidays(location)
    load_holidays_to_select_trip_dropdown(holidays)


def load_holidays_to_select_trip_dropdown(holidays):
    # get select parent element and store in variable
    select_menu = document.getElementById("trip")
    # enable it
    select_menu.disabled = False
    for holiday in holidays:
        duration = holiday["duration"]
        location = holiday["location"]
        date = holiday["departure_date"]
        
        option = document.createElement("option")
        option.innerHTML = f"Go to {location} on {date} for {duration} days"
        
        option.value = holiday["id"]

        select_menu.appendChild(option)




from pyscript import document, when

from api import get_request_holidays, post_request_booking


@when("change", "#trip")
def select_holiday(e):
    form = document.getElementsByClassName("booking")[0]
    inputs = form.getElementsByTagName("input")
    for input_ in inputs:
        input_.disabled = False
    holiday = e.target.innerHTML 


def create_booking():
    # get stuff from fields
    cust_name = document.getElementById("cust-name").value.split(" ")
    cust_forename = cust_name[0]
    cust_surname = cust_name[1]
    cust_tel = document.getElementById("cust-tel").value
    guest_name = document.getElementById("guest1").value
    allergy_boxes = document.getElementsByClassName("checkboxes")[0]
    guest_allergies = []
    for child in allergy_boxes.children:
        if child.checked:
            guest_allergies.append(child.name)

    # make dictionary (which contains a Holiday object, Customer object... etc.)
    

@when()
async def click_book_holiday(e):
    '''Triggers request to add new booking to database'''
    booking = create_booking()
    feedback = await post_request_booking(booking)


@when()
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
        # make text to go in option
        option_text = f"Go to {location} on {date} for {duration} days"
        # make option + add text
        option = document.createElement("option")
        option.innerHTML = option_text
        # add child to parent tag
        select_menu.appendChild(option)




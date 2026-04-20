from pyscript import document, when

from api import get_request_holidays

@when("click", ".search-cta")
async def click_go(e):
    holidays = await get_request_holidays()
    print(holidays)

# go_button = document.getElementsByClassName("search-cta")[0]



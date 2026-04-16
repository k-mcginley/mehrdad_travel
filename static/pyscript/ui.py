from pyscript import document, when

@when("click", ".search-cta")
def click_go():
    holidays = get_request_holidays()
    print(holidays)

# go_button = document.getElementsByClassName("search-cta")[0]



from pyscript import fetch

async def get_request_holidays():
    response = await fetch("/api/holidays")     # end point to allow server to respond
    data = await response.json()
    return data
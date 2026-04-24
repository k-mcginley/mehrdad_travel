from pyodide.http import pyfetch

async def get_request_holidays(location):

    location = location.replace(" ", "%20")

    response = await pyfetch(f"/api/holidays?location={location}")     # end point to allow server to respond
    data = await response.json()
    return data
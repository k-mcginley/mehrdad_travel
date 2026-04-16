from pyodide.http import pyfetch

async def get_request_holidays():
    response = await pyfetch("/api/holidays")   
    data = await response.json()
    return data

import os
import time
import requests
import gspread

def get_magento_token():
    url = 'https://www.kokbedden.nl/rest/V1/integration/admin/token'
    credentials = {
        "username": os.getenv("MAGENTO_ADMIN_USERNAME"),
        "password": os.getenv("MAGENTO_ADMIN_PASSWORD")
    }
    response = requests.post(url, json=credentials)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Magento login failed: {response.text}")

def update_google_sheet(token):
    gc = gspread.Client(None)  # unauthenticated
    gc.session = gspread.auth.DEFAULT_SESSION  # use default session
    sheet = gc.open_by_url(os.getenv("SPREADSHEET_URL")).sheet1
    sheet.update_acell("A2", token)

while True:
    try:
        token = get_magento_token()
        update_google_sheet(token)
        print("Token updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3 * 60 * 60)

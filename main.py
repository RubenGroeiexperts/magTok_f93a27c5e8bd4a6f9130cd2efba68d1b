import os
import requests

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

def send_to_webapp(token):
    webapp_url = os.getenv("WEBAPP_URL")
    response = requests.post(webapp_url, data={'token': token})
    if response.status_code != 200:
        raise Exception(f"Failed to send token: {response.text}")

def main():
    token = get_magento_token()
    send_to_webapp(token)
    print("Token sent to sheet.")

if __name__ == "__main__":
    main()

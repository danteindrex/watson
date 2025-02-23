import requests
import json
import base64
from datetime import datetime, timedelta

# --- QuickBooks API Configuration ---
QB_CLIENT_ID = "ABvBOXqS8acivQUuPJGL2mZnXPtv6hCbDpaH5XlxmvUhNedUFq" #sample from account i made
QB_CLIENT_SECRET = "NrYcOwHrjRGDp0tzW5T8sc8Z3ZAZVowbNzdI4orM" #still for my account
QB_REALM_ID = "9341454144425377"  # Company ID
QB_REDIRECT_URI = "https://ibm.com/ibm/customers" # Must match what you set in your QB app.
QB_ACCESS_TOKEN = "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..i6GaEZw-oXwsL1gZyEitSw.54aR21uP-QbgmwZeQm7mCxm-1teILUPfnsIIYyL3xwO8N6bGLBqAb_5gWvxaHcTAY43MktK_S8fw_7Mi-GzZQcZVSfzD54_tBOoJvgl0IOBVFe4GrBBq17TeY09LL2sK-tuWoHplXWJ-jnv2zQ81b1MJUKsV-UeCXHr0EL7wg3IOdXgEDFiLG1QmXWQO6M-40SQvqH9gIb1aTN4FilNDheAnbJWvSNIjOIsA7emymfYUS_N327wIksvKs0x_H_LSHzC0QULVh3UiyaMoopGqvNCRDMbPhc0t0xBrSYqYas4gglkGZNGM7qqAwRY-SnA-JxGs729IabC3GPV-d9q07FwSkZuFj4tpGqQd2u5CAVtVhzz_vuF2vFGBrVt6A63fXolKlxJDDL17o_mLYr3K--MnscyigLwgcyrHq8RyVrz0ZQQBdvHojNWZz2Gdwg8u6Q66J-yhHFHUX51xNt0NA0NG5CwaHVA2E1S8lneMjfgqK6UwlRIHLBkzLMz9td7u4U8Cbrg7KmCGIMUa_MYDBDjuZk8z4FUaE8Mg-aJvG2zP3EmQZZoHcWMo1yoIX_kymEmLJPmw_igKcu0jY_jIPJGiBpoUM6kcz5UxovcQpsyLBNZ8vAwNKQsbb8eLaN17NTjeheWIVJq38-g4FmuV8CqsoPWOgfG480O204gD-2dT-tuVVrT-Zgy8sNRJNtOzMyVHiE4HXcxawdHDDFPOuvcQTN-KhzjH0SuOUUvdjqvVAFyxWHMFBCT2lG9SwkfVkp5JkgyZ-Grr8pLpLdbtMhhtKAMT0UF0awVOYNxVZ0_Z-etmJVdsq6Vfc81Gppw6Opj3pGGLmKHdj0OYrmmn1pdtaKPnXJQwkgYj6V_Y7Pc.oaVRHEFWf44zQQ53wiQqlQ" # Store and refresh these!
QB_REFRESH_TOKEN = "AB11748993181z8i2fr8rzZj4arOwFbQ14SgoZWkYa9r79hgrA" # Store these securely! Probably expired by now
QB_BASE_URL = "https://quickbooks.api.intuit.com/v3/company/" + QB_REALM_ID

# --- Zendesk API Configuration ---
ZD_SUBDOMAIN = input("YOUR_ZENDESK_SUBDOMAIN")
ZD_EMAIL = input("YOUR_ZENDESK_EMAIL")
ZD_API_TOKEN = input("YOUR_ZENDESK_API_TOKEN")
ZD_BASE_URL = f"https://{ZD_SUBDOMAIN}.zendesk.com/api/v2"

def refresh_quickbooks_token():
    """Refreshes the QuickBooks access token."""
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    auth_str = base64.b64encode(f"{QB_CLIENT_ID}:{QB_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": QB_REFRESH_TOKEN,
    }
    response = requests.post(token_url, headers=headers, data=data) #API call made here
    if response.status_code == 200:
        token_data = response.json()
        global QB_ACCESS_TOKEN, QB_REFRESH_TOKEN
        QB_ACCESS_TOKEN = token_data["access_token"]
        QB_REFRESH_TOKEN = token_data["refresh_token"]
        # **Important:** Store the new tokens securely!
        print("QuickBooks token refreshed successfully.")
        return True
    else:
        print(f"Failed to refresh QuickBooks token: {response.status_code}, {response.text}")
        return False


from crewai.tools import tool


@tool("quickbooks")
def get_quickbooks_customers(QB_ACCESS_TOKEN,QB_BASE_URL): #getting customers
    """Fetches customer data from QuickBooks."""
    headers = {
        "Authorization": f"Bearer {QB_ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    url = f"{QB_BASE_URL}/query?query=select * from Customer" #specify customer or customers you want to fetch here
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("QueryResponse", {}).get("Customer", [])
    else:
        print(f"Failed to get QuickBooks customers: {response.status_code}, {response.text}")
        return []

def get_zendesk_tickets(start_time=None): # getting tickets
    """Fetches Zendesk tickets, optionally after a start time."""
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{ZD_EMAIL}/token:{ZD_API_TOKEN}'.encode()).decode()}",
        "Content-Type": "application/json",
    }

    url = f"{ZD_BASE_URL}/tickets.json"
    if start_time:
        url += f"?start_time={int(start_time.timestamp())}"

    tickets = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tickets.extend(data["tickets"])
            url = data["next_page"]
        else:
            print(f"Failed to get Zendesk tickets: {response.status_code}, {response.text}")
            break
    return tickets

def main(): #this is where you choose how to make use of the data. Optionally you can decide to send this stuff to your database
    if not QB_ACCESS_TOKEN: #if you have no token, you need to get one first, this example only refreshes.
        print("Quickbooks access token missing. Please get one first.")
        return

    if refresh_quickbooks_token():
        qb_customers = get_quickbooks_customers()
        print(f"Fetched {len(qb_customers)} QuickBooks customers.")

    # Example: Fetching Zendesk tickets from the last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    zd_tickets = get_zendesk_tickets(yesterday)
    print(f"Fetched {len(zd_tickets)} Zendesk tickets.")

    # Example: Print some data
    if qb_customers:
        print("Example QuickBooks Customer:")
        print(json.dumps(qb_customers[0], indent=2))

    if zd_tickets:
        print("Example Zendesk Ticket:")
        print(json.dumps(zd_tickets[0], indent=2))

if __name__ == "__main__":
    main()

#you can create functions to retrieve specific data as detailed by quickbooks' documentation e.g. opening a bank account
authScopepayements = "com.intuit.quickbooks.payment"
authScopeaccounting = 'com.intuit.quickbooks.accounting'
#create all the quickbooks info in the intuit developer portal
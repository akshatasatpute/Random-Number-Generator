import streamlit as st
import gspread
import requests
from google.oauth2 import service_account
import random


st.markdown(
    "<h1 style='color: black; font-weight: bold;'>Random Number Generator</h1>", 
    unsafe_allow_html=True
)

# Function to generate random number
def generate_random_number():
    # Generate a random number between 1 and 100
    return random.randint(1000, 9999)
    

# Create a unique key for the button widget
random_number_button_key = 'random_number_button_key'

# Create a button in the Streamlit app with a unique key
if st.button('Generate Random Number', key=random_number_button_key):
    random_number = generate_random_number()
    st.write(f"Random Number: {random_number}")
    
    # Fetch service account credentials from Supabase storage
    supabase_credentials_url = "https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/studied-indexer-431906-h1-e3634918ab42.json?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svc3R1ZGllZC1pbmRleGVyLTQzMTkwNi1oMS1lMzYzNDkxOGFiNDIuanNvbiIsImlhdCI6MTcyNjkwMzEzNywiZXhwIjoxNzU4NDM5MTM3fQ.d-YWFIIV3ue7eUwUIemVHKrxVSgsdy3Dm34bCfkKBPE&t=2024-09-21T07%3A18%3A57.318Z"
    response = requests.get(supabase_credentials_url)
    
    if response.status_code == 200:
        # Decode the content of the response as a JSON keyfile and create service account credentials
        service_account_info = response.json()
        
        # Use the service account info to create credentials
        creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        client = gspread.authorize(creds)

        
        
        # Insert the random number into the Google Sheet
        sheet_key = '175j97xicFqFA1eKPBjzXzQJaKyIfaJYwpwhaL6qGFDg'
        row_index_to_update = 1  # Update this with the desired row index
    
        # Open the Google Sheet by key and retrieve the specific worksheet
        sheet = client.open_by_key(sheet_key).sheet1  # Update with the correct sheet name or index
    
        # Prepare the 2D list of values to update in the cell
        values_to_update = [[random_number]]  # Wrap the random number in a list
    
        # Define the cell range to update
        cell_range = f'A{row_index_to_update}'  # Assuming the random number will be updated in column A
    
        # Update the specific cell with the random number
        sheet.update(cell_range, values_to_update)  # Update the cell in the specified row with the random number
    
    else:
        print("Failed to fetch the service account credentials. Status code:", response.status_code)

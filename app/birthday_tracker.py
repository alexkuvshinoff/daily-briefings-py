# app/birthday_tracker.py

from dotenv import load_dotenv
import os
from app import APP_ENV
from datetime import date, datetime

import json
from pprint import pprint

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import APP_ENV
from app.email_service import send_email

load_dotenv()

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "Products")

#
# AUTHORIZATION
#

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

#
# READ SHEET VALUES
#

client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>

doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>

print("-----------------")
print("SPREADSHEET:", doc.title)
print("-----------------")

sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

rows = sheet.get_all_records() #> <class 'list'>

email_brithdays = []
todaysDate = date.today()

for row in rows:
    rowDate = datetime.strptime(row['DOB:'],"%m/%d/%Y").date().replace(year=todaysDate.year)
    if rowDate == todaysDate:
        print(row) #> <class 'dict'>





import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import xlsxwriter
from time import sleep

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1LnKPu7JfB9tpyvoEEVEDh3PFxTNYsO3IwECJojNIjBM"

def main():
    #os.chdir(r"C:\Users\PC\VsCodeProjects\WebScrappingProj\.venv\KabumScraper\KabumScraper\spiders")
    #os.system("scrapy crawl kabumspider")
    
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("C:/Users/PC/VsCodeProjects/WebScrappingProj/.venv/KabumScraper/credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
            
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        
        with open('C:/Users/PC/VsCodeProjects/WebScrappingProj/.venv/KabumScraper/KabumData.json') as json_file:
            json_data = json.load(json_file)
        
        row = 1
        
        for dict in json_data:
            row += 1
            row_data = []
            for key in dict:
                row_data.append(dict[key])
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f'KabumProducts!A{row}', valueInputOption='USER_ENTERED', body={'values': [row_data]}).execute()
            sleep(1)
            print(row_data[0])
            
            
        
    except HttpError as error:
        print(error)
        
if __name__ == "__main__":
    main()
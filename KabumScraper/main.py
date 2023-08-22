import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time import sleep

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1LnKPu7JfB9tpyvoEEVEDh3PFxTNYsO3IwECJojNIjBM"

def main():
    
    #If JSON file does not exists: create file
    if(not os.path.exists('C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/KabumData.json')):
        KabumData = open('C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/KabumData.json', 'x')
    
    #Change working directory to use Scrapy in Command Prompt
    os.chdir("C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/KabumScraper/spiders")
    
    #Activating Scrapy crawling with kabumspider
    os.system("scrapy crawl KabumSpider")
    
    #Code block to get the API token
    credentials = None
    if os.path.exists("C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/token.json", "w") as token:
            token.write(credentials.to_json())
    
    #Getting access to the spreadsheet
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        
        with open('C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/KabumData.json') as json_file:
            json_data = json.load(json_file)
        
        row = 1
        
        #Iterating through products in JSON
        for dict in json_data:
            #Changing spreadsheet row
            row += 1
            row_data = []
            for key in dict:
                row_data.append(dict[key])
            #Updating spreadsheet
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f'KabumProducts!A{row}', valueInputOption='USER_ENTERED', body={'values': [row_data]}).execute()
            #Delay to prevent quota error
            sleep(1)
        
    #Error handling
    except HttpError as error:
        print(error)
        
if __name__ == "__main__":
    main()
# KabumScrapping 🕸
Web Scrapping application to scrape data from a brazilian hardware website and pass it to a google spreadsheet trough an API

## Spreadsheet Row Example
![image](https://github.com/VictorEbeling/KabumScrapping/assets/114254186/ad8ddd13-ef41-45d8-9509-177eb5f77ff7)

## Requirements:
```python
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time import sleep
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.log import configure_logging
import logging
```



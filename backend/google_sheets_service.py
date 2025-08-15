import json
import os
import logging
from datetime import datetime
from pathlib import Path
from google.auth import credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.sheet_id = None
        self.service_account_file = None
        self.service = None
        self._initialized = False
    
    def _initialize_service(self):
        """Initialize the Google Sheets API service"""
        if self._initialized:
            return
            
        try:
            self.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
            self.service_account_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
            
            if not self.service_account_file or not self.sheet_id:
                raise ValueError(f"Missing Google Sheets credentials or sheet ID. Sheet ID: {self.sheet_id}, File: {self.service_account_file}")
            
            # Create credentials from the service account file
            creds = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=creds)
            self._initialized = True
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
            raise
    
    def add_signup(self, email: str) -> bool:
        """Add a new signup to the Google Sheet"""
        try:
            self._initialize_service()
            
            if not self.service:
                raise ValueError("Google Sheets service not initialized")
            
            # Prepare the data
            timestamp = datetime.utcnow().isoformat() + 'Z'
            source = "P.A.R. Landing Page"
            
            # Data to append
            values = [[email, timestamp, source]]
            
            # Prepare the request
            body = {
                'values': values
            }
            
            # Execute the request
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range='Signups!A:C',  # Append to columns A, B, C
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Successfully added signup: {email}")
            return True
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to add signup: {str(e)}")
            return False
    
    def setup_sheet_headers(self):
        """Set up the header row in the sheet (call this once)"""
        try:
            self._initialize_service()
            
            if not self.service:
                raise ValueError("Google Sheets service not initialized")
            
            # Check if headers already exist
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Signups!A1:C1'
            ).execute()
            
            values = result.get('values', [])
            
            # If no headers or incorrect headers, add them
            if not values or values[0] != ['Email', 'Timestamp', 'Source']:
                headers = [['Email', 'Timestamp', 'Source']]
                body = {'values': headers}
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheet_id,
                    range='Signups!A1:C1',
                    valueInputOption='RAW',
                    body=body
                ).execute()
                
                logger.info("Sheet headers set up successfully")
            else:
                logger.info("Sheet headers already exist")
                
        except Exception as e:
            logger.error(f"Failed to setup sheet headers: {str(e)}")
            raise

# Global instance (will be initialized lazily)
sheets_service = GoogleSheetsService()
import json
import os
import logging
from datetime import datetime
from google.auth import credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        self.service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the Google Sheets API service"""
        try:
            if not self.service_account_json or not self.sheet_id:
                raise ValueError("Missing Google Sheets credentials or sheet ID")
            
            # Parse the JSON credentials
            creds_dict = json.loads(self.service_account_json)
            
            # Create credentials from the service account info
            creds = service_account.Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
            raise
    
    def add_signup(self, email: str) -> bool:
        """Add a new signup to the Google Sheet"""
        try:
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

# Global instance
sheets_service = GoogleSheetsService()
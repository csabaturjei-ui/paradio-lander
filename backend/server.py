from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import re
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import List
import uuid
from datetime import datetime
from google_sheets_service import sheets_service
import resend

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Resend — requires postapocalypticradio.com to be verified in the Resend dashboard
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
FROM_ADDRESS = 'P.A.R. <hello@postapocalypticradio.com>'
NOTIFY_ADDRESS = 'hello@postapocalypticradio.com'

CONFIRMATION_HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="background:#0a0a0a;margin:0;padding:40px 20px;font-family:'Courier New',monospace;">
  <div style="max-width:480px;margin:0 auto;background:#0f0f0f;border:1px solid rgba(57,255,20,0.3);border-radius:8px;padding:40px;">
    <p style="font-size:11px;letter-spacing:0.15em;color:#29a331;margin:0 0 24px;text-transform:uppercase;">Post Apocalyptic Radio</p>
    <h1 style="font-size:22px;color:#39ff14;margin:0 0 20px;line-height:1.2;">📡 Signal Received</h1>
    <p style="color:#29a331;line-height:1.7;font-size:14px;margin:0 0 16px;">
      You're on the waitlist. We're building the first decentralized music streaming platform —
      <span style="color:#39ff14;">0% cut to artists</span>, community-curated playlists,
      IPFS storage, and instant Solana payments.
    </p>
    <p style="color:#29a331;line-height:1.7;font-size:14px;margin:0 0 32px;">
      We'll reach out when beta access opens.
    </p>
    <div style="border-top:1px solid rgba(57,255,20,0.2);padding-top:20px;">
      <p style="color:#29a331;font-size:12px;margin:0;">
        Post Apocalyptic Radio &middot;
        <a href="https://postapocalypticradio.com" style="color:#39ff14;text-decoration:none;">postapocalypticradio.com</a>
      </p>
    </div>
  </div>
</body>
</html>
"""

def send_signup_emails(email: str) -> None:
    """Send confirmation to the user and notification to the owner. Best-effort — never raises."""
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set — skipping email send")
        return
    resend.api_key = RESEND_API_KEY
    try:
        resend.Emails.send({
            "from": FROM_ADDRESS,
            "to": [email],
            "subject": "📡 You're on the P.A.R. waitlist",
            "html": CONFIRMATION_HTML,
        })
        resend.Emails.send({
            "from": FROM_ADDRESS,
            "to": [NOTIFY_ADDRESS],
            "subject": f"New P.A.R. signup: {email}",
            "html": f'<p style="font-family:monospace;">New waitlist signup: <strong>{email}</strong></p>',
        })
    except Exception as e:
        logger.error(f"Resend error for {email}: {e}")

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class EmailSignup(BaseModel):
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email address')
        return v.lower().strip()

class SignupResponse(BaseModel):
    success: bool
    message: str

# Original routes
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# New signup endpoint
@api_router.post("/signup", response_model=SignupResponse)
async def create_signup(signup: EmailSignup):
    try:
        # Add to Google Sheets
        success = sheets_service.add_signup(signup.email)
        
        if success:
            send_signup_emails(signup.email)
            return SignupResponse(
                success=True,
                message="Successfully joined the waitlist!"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to save signup. Please try again."
            )
            
    except ValueError as e:
        # Email validation error
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to save signup. Please try again."
        )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize Google Sheets on startup"""
    try:
        sheets_service.setup_sheet_headers()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to setup Google Sheets: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
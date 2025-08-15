# API Contracts - Post Apocalyptic Radio Landing Page

## Backend Implementation Requirements

### Google Sheets Integration
- **Sheet ID**: `1eN0tMEULiGkN-a-wWoWb1ezWKLeS05CvbGnoVKl2hPI`
- **Sheet Name**: `Signups`
- **Service Account**: `par-signups@par-beta-signups.iam.gserviceaccount.com`

### Data Structure
Each signup will contain:
1. **Email**: User's email address
2. **Timestamp**: ISO format datetime when signup occurred
3. **Source**: "P.A.R. Landing Page"

### API Endpoints

#### POST /api/signup
**Purpose**: Save email signup to Google Sheets

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response Success (200)**:
```json
{
  "success": true,
  "message": "Successfully joined the waitlist!"
}
```

**Response Error (400)**:
```json
{
  "success": false,
  "error": "Invalid email address"
}
```

**Response Error (500)**:
```json
{
  "success": false,
  "error": "Failed to save signup. Please try again."
}
```

### Frontend Integration Changes

#### Remove Mock Data
- Replace `mockEmailSignup()` calls with actual API calls to `/api/signup`
- Remove mock.js import for email functionality (keep other mock data)

#### Updated Form Submission
- Change form submission to POST to `/api/signup`
- Handle loading states during API call
- Display success/error messages via toast notifications

### Dependencies to Install
- `google-auth`
- `google-auth-oauthlib` 
- `google-auth-httplib2`
- `google-api-python-client`

### Environment Variables
- Store Google Service Account JSON in `/app/backend/.env` as `GOOGLE_SERVICE_ACCOUNT_JSON`
- Store Sheet ID as `GOOGLE_SHEET_ID`

### Error Handling
- Validate email format on backend
- Handle Google API rate limits
- Handle network connectivity issues
- Log errors for debugging while showing user-friendly messages
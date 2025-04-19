from flask import Flask, redirect, request, session, render_template
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Use a fixed secret for session persistence
app.config.update({
    'SESSION_COOKIE_NAME': 'gmail-auth-session',
    'PERMANENT_SESSION_LIFETIME': 600,  # 10 minutes
    'SESSION_COOKIE_SECURE': False,      # For local development
    'SESSION_COOKIE_SAMESITE': 'Lax'
})

# OAuth configuration
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = 'http://localhost:5000/callback'

# Initialize OAuth flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route('/')
def index():
    """Home page with login button"""
    if 'credentials' in session:
        return redirect('/emails')
    return render_template('login.html')

@app.route('/authorize')
def authorize():
    """Initiate Google OAuth flow"""
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='select_account'
    )
    session.permanent = True  # Make session persistent
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    """Handle OAuth callback"""
    # Check for state in session and request
    if 'oauth_state' not in session:
        return redirect('/authorize')
    
    if 'state' not in request.args:
        return redirect('/authorize')
    
    # Validate state parameter
    if session['oauth_state'] != request.args.get('state'):
        session.pop('oauth_state', None)
        return redirect('/authorize')
    
    try:
        # Fetch tokens
        flow.fetch_token(authorization_response=request.url)
        
        # Store credentials
        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'scopes': credentials.scopes
        }
        session.pop('oauth_state', None)
        
    except Exception as e:
        return f"Authentication failed: {str(e)}", 400
    
    return redirect('/emails')

@app.route('/emails')
def show_emails():
    """Display emails page"""
    if 'credentials' not in session:
        return redirect('/')
    
    try:
        # Build service from credentials
        credentials = flow.credentials
        service = build('gmail', 'v1', credentials=credentials)
        
        # Retrieve emails
        result = service.users().messages().list(
            userId='me',
            maxResults=10
        ).execute()
        
        messages = []
        for msg in result.get('messages', []):
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            messages.append({
                'id': message['id'],
                'from': headers.get('From', 'Unknown'),
                'subject': headers.get('Subject', '(No Subject)'),
                'date': headers.get('Date', 'Unknown Date')
            })
        
        return render_template('emails.html', emails=messages)
    
    except Exception as e:
        session.clear()
        return f"Error fetching emails: {str(e)}", 500

@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Local development only
    app.run(host='localhost', port=5000, debug=True)
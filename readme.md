# Gmail Viewer

## Overview
Gmail Viewer is a Flask-based web application that allows users to authenticate with their Google account and view their recent Gmail messages. The application uses the Gmail API to fetch email metadata (sender, subject, and date) and displays them in a clean, responsive interface.

## Features
- **Google OAuth Authentication**: Secure login using Google OAuth 2.0.
- **Email Listing**: Displays the 10 most recent emails from the user's Gmail inbox.
- **Responsive UI**: Modern, user-friendly interface for both login and email display.
- **Session Management**: Persistent session handling with secure cookie settings.
- **Logout Functionality**: Easy logout to clear session data.

## Advanced Features
- **AI-Powered Automation**: Utilizes Gemini AI for smart email management.
- **Voice Recognition**: Integrated voice recognition for hands-free email interaction.
- **Semantic Search**: Implements FAISS and sentence transformers for advanced email search capabilities.
- **Smart Reply Generation**: Automatically generates context-aware email replies.
- **Automated Labeling**: Intelligently categorizes emails based on content.
- **Email Triage**: Prioritizes emails based on importance and urgency.
- **Priority Detection**: Identifies high-priority emails for immediate attention.
- **Dashboard Analytics**: Provides insights and analytics on email usage and trends.

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- A Google Cloud project with the Gmail API enabled
- OAuth 2.0 credentials (client ID and client secret)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gmail-viewer
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use `myenv\\Scripts\\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure OAuth credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API.
   - Create OAuth 2.0 credentials (Web application type).
   - Set the authorized redirect URI to `http://localhost:5000/callback`.
   - Download the credentials and save them as `credentials.json` in the project root.

## Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`.

## Configuration
- **Secret Key**: The application uses a fixed secret key for session management. For production, replace `'your-secret-key-123'` in `app.py` with a secure, randomly generated key.
- **OAuth Credentials**: Ensure `credentials.json` is correctly configured with your Google Cloud project credentials.

## User Interface
- **Login Page**: A clean, centered login button that initiates the Google OAuth flow.
- **Emails Page**: Displays a list of recent emails with sender, subject, and date. Each email is presented in a card format with hover effects for better user experience.

## Security Notes
- **OAuth Credentials**: Keep your `credentials.json` secure and never commit it to version control.
- **Session Security**: The application uses secure session settings. For production, ensure `SESSION_COOKIE_SECURE` is set to `True` and use HTTPS.

## Dependencies
- Flask
- google-api-python-client
- google-auth-oauthlib
- google-auth
- google-auth-httplib2

## Troubleshooting
- **Redirect URI Mismatch**: Ensure the redirect URI in `credentials.json` matches the one in your Google Cloud Console.
- **Authentication Errors**: Check if the Gmail API is enabled and the credentials are correctly configured.
- **Session Issues**: If sessions are not persisting, verify the secret key and session settings in `app.py`.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
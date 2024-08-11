"""
Step 1: Setting Up Google API Access
Create a project in the Google Developers Console:

Go to https://console.developers.google.com/
Create a new project.
Enable the Gmail API:

In the dashboard, navigate to "Enable APIs and Services".
Search for "Gmail API" and enable it.
Create Credentials:

Go to "Credentials" on the sidebar.
Click “Create Credentials” and select "OAuth client ID".
Configure the consent screen as required.
For application type, select "Desktop app" and give it a name.
Download the JSON file which contains your credentials.
Install Google Client Libraries:

You can install these libraries using pip:

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


run email_extractor.py and then authenticate the gmail pop up in unsafe mode.
"""
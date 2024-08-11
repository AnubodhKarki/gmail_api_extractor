import base64
import pandas as pd
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    logging.error('Error loading credentials.')
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def list_messages(service, label_ids=[], q=''):
    response = service.users().messages().list(userId='me', labelIds=label_ids, q=q, maxResults=500).execute()
    messages = response.get('messages', [])
    messages_details = []
    for message in messages:
        details = get_message_details(service, message['id'])
        messages_details.append((details['Date'], message))
    messages_details.sort(key=lambda x: x[0], reverse=True)
    sorted_messages = [message[1] for message in messages_details]
    return sorted_messages

def get_message_details(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    headers = message['payload']['headers']
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
    from_email = next((header['value'] for header in headers if header['name'] == 'From'), '')
    date = next((header['value'] for header in headers if header['name'] == 'Date'), '')
    thread_id = message['threadId']
    in_reply_to = next((header['value'] for header in headers if header['name'] == 'In-Reply-To'), None)

    parts = message['payload'].get('parts', [])
    body = ''
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    
    # Fetch labels
    label_ids = message.get('labelIds', [])
    
    return {'Date': date, 'From': from_email, 'Subject': subject, 'Body': body, 'Message ID': message_id, 'Thread ID': thread_id,'In-Reply-To ID': in_reply_to, 'Label IDs': label_ids}


if __name__ == '__main__':
    logging.basicConfig(filename='gmail_api.log', level=logging.ERROR)
    gmail_service = get_gmail_service()
    print("Gmail service retrieved successfully.")
    inbox_messages = list_messages(gmail_service)
    if inbox_messages:
        print(f"Number of inbox messages: {len(inbox_messages)}")
        inbox_message_details = []
        for inbox_message in inbox_messages:
            print(f"Processing message ID: {inbox_message['id']}")
            details = get_message_details(gmail_service, inbox_message['id'])
            if details:
                inbox_message_details.append(details)
            else:
                print(f"Failed to retrieve details for message ID: {inbox_message['id']}")
        if inbox_message_details:
            df = pd.DataFrame(inbox_message_details)
            df.to_csv('inbox_messages.csv', index=False)
            print('Inbox messages saved successfully.')
        else:
            print('No inbox message details found.')
    else:
        print('No inbox messages found.')

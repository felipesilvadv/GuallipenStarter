from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request




def setupService():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://mail.google.com/',
              'https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/gmail.compose',
              'https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                credentials_path = os.path.join("..", "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
            except FileNotFoundError:
                credentials_path = "credentials.json"
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)

            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

    # Call the Gmail API



if __name__ == "__main__":
    setupService()

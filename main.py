import auth
from google.oauth2.credentials import Credentials
import tkinter as tk
from tkinter import messagebox
from googleapiclient.discovery import build
from flask import Flask

import contacts
from contacts import get_labels

def get_contact_labels():
    address_book = Contacts.ABAddressBook.sharedAddressBook()
    labels = []
    for group in address_book.groups():
        label = group.valueForProperty_(Contacts.kABGroupNameProperty)
        if label:
            labels.append(label)
    return labels


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


class MainWindow(tk.Frame):
    def __init__(self, root, creds):
        super().__init__(root)
        self.creds = creds
        self.root = root
        self.root.geometry('300x200')
        self.root.title('Main')

        self.share_label = tk.Label(self.root, text='Share with email:')
        self.share_label.pack(pady=10)
        self.share_entry = tk.Entry(self.root)
        self.share_entry.pack()

        self.label_selection = tk.Label(self.root, text='Select labels to share:')
        self.label_selection.pack(pady=10)
        self.label_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.label_listbox.pack()
        self.populate_label_listbox()

        self.share_button = tk.Button(self.root, text='Share', command=self.share_labels)
        self.share_button.pack(pady=20)

    def populate_label_listbox(self):
        # Use the get_labels() function from the gmail module to get a list of all labels
        labels = get_labels(self.creds)

        # Add each label to the label_listbox
        for label in labels:
            self.label_listbox.insert(tk.END, label['name'])

    def share_labels(self):
        share_email = self.share_entry.get()

        # Get a list of the indices of the currently selected labels in the label_listbox
        selected_indices = self.label_listbox.curselection()

        # Create a list of the selected labels based on the selected indices
        selected_labels = [self.label_listbox.get(idx) for idx in selected_indices]

        # Create a confirmation message with the selected labels and the email to share with
        confirmation_message = f'Are you sure you want to share the following labels with {share_email}?\n'
        confirmation_message += '\n'.join(selected_labels)

        # Ask the user to confirm that they want to share the selected labels
        confirmation = tk.messagebox.askyesno(title='Confirmation', message=confirmation_message)

        # If the user confirms, share the selected labels with the specified email address
        if confirmation:
            service = build('drive', 'v3', credentials=self.creds)

            # Get the label IDs for the selected labels
            label_ids = [self.get_label_id(label_name) for label_name in selected_labels]

            # Share the selected labels with the specified email address
            share_labels(service, share_email, label_ids)

    def get_label_id(self, label_name):
        # Use the get_labels() function from the gmail module to get a list of all labels
        labels = get_labels(self.creds)

        # Find the label with the specified name and return its ID
        for label in labels:
            if label['name'] == label_name:
                return label['id']


class ContactsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contacts App")
        self.geometry("300x250")

        self.label = tk.Label(self, text="Welcome to Contacts App!")
        self.label.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

def login(self):
    # Specify the scopes required for the app
    scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/gmail.labels']


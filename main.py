import auth
import tkinter as tk


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
        # TODO: Implement logic to populate the label listbox
        pass

    def share_labels(self):
        share_email = self.share_entry.get()
        selected_labels = [self.label_listbox.get(idx) for idx in self.label_listbox.curselection()]

        # TODO: Implement label sharing logic here

        confirmation_message = f'Are you sure you want to share the following labels with {share_email}?\n'
        confirmation_message += '\n'.join(selected_labels)
        confirmation = tk.messagebox.askyesno(title='Confirmation', message=confirmation_message)

        if confirmation:
            service = build('drive', 'v3', credentials=self.creds)
            label_ids = [self.get_label_id(label_name) for label_name in selected_labels]
            share_labels(service, share_email, label_ids)


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
        scopes = ['https://www.googleapis.com/auth/contacts']
        creds = auth.authenticate(scopes)
        if creds:
            self.label.config(text="You are logged in!")
            self.login_button.config(state="disabled")
            self.show_main_window(creds)

    def show_main_window(self, creds):
        main_window = MainWindow(self, creds)
        main_window.pack(fill=tk.BOTH, expand=True)


class ConfirmationDialog(tk.Frame):
    def __init__(self, master, share_email, label_id):
        super().__init__(master)
        self.share_email = share_email
        self.label_id = label_id
        self.master = master

        self.message = tk.Label(self, text=f"Are you sure you want to share label {label_id} with {share_email}?")
        self.message.pack(pady=10)

        self.confirm_button = tk.Button(self, text='Confirm', command=self.confirm)
        self.confirm_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self, text='Cancel', command=self.cancel)

    def confirm(self):
        # TODO: Implement label sharing confirmation logic here

        # Close the confirmation dialog
        self.master.destroy()

    def cancel(self):
        # Close the confirmation dialog without sharing the label
        self.master.destroy()


if __name__ == '__main__':
    app = ContactsApp()
    app.mainloop()

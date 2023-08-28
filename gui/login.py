import customtkinter as ctk
from functions.accountmanager import save_user_creds

class Login(ctk.CTkToplevel):
    def __init__(self, master, *args):
        super().__init__(master=master, *args)
        self.title("Login")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 300
        self.window_height = 200
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.protocol("WM_DELETE_WINDOW", self._disable_exit)
        self.lift()
        self.grab_set()

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(column=1, sticky='nswe', row=1, pady=20, padx=20)
        self.login_frame.grid_columnconfigure((0,3), weight=1)
        self.login_frame.grid_rowconfigure((0,4), weight=1)

        self.username_label = ctk.CTkLabel(self.login_frame, text='Username:')
        self.username_label.grid(column=1, row=1)

        self.username_variable = ctk.StringVar()
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text='Username', textvariable=self.username_variable)
        self.username_entry.grid(column=2, row=1, padx=(10,0))

        self.password_label = ctk.CTkLabel(self.login_frame, text='Password:')
        self.password_label.grid(column=1, row=2)

        self.password_variable = ctk.StringVar()
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text='Password', textvariable=self.password_variable)
        self.password_entry.grid(column=2, row=2, pady=10, padx=(10,0))

        self.save_btn = ctk.CTkButton(self.login_frame, text="Save", width=60, command=self.save_login_creds)
        self.save_btn.grid(column=1, row=3, pady=10, columnspan=2)
        self.save_btn.configure(state='disabled')

        self.username_variable.trace('w', self.check_entries)
        self.password_variable.trace('w', self.check_entries)
    
    def _disable_exit(self):
        pass

    def check_entries(self, *args):
        user = self.username_variable.get()
        pwd = self.password_variable.get()
        if user.rstrip() and pwd.rstrip():
            self.save_btn.configure(state='normal')
        else:
            self.save_btn.configure(state='disabled')

    def save_login_creds(self):
        user = self.username_variable.get().rstrip()
        pwd = self.password_variable.get().rstrip()
        with open('creds.txt', 'w+') as f:
            f.writelines([i + '\n' for i in [user, pwd]])
        save_user_creds(user, pwd)
        self.destroy()
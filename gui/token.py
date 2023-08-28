import customtkinter as ctk

class Token(ctk.CTkToplevel):
    def __init__(self, master, *args):
        super().__init__(master=master, *args)
        self.title("OpenAI API Key")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 400
        self.window_height = 200
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.protocol("WM_DELETE_WINDOW", self._disable_exit)
        self.lift()
        self.grab_set()

        self.token_frame = ctk.CTkFrame(self)
        self.token_frame.grid(column=1, sticky='nswe', row=1, pady=20, padx=20)
        self.token_frame.grid_columnconfigure((0,3), weight=1)
        self.token_frame.grid_rowconfigure((0,4), weight=1)

        self.token_label = ctk.CTkLabel(self.token_frame, text='Token:')
        self.token_label.grid(column=1, row=1)

        self.token_variable = ctk.StringVar()
        self.token_entry = ctk.CTkEntry(self.token_frame, placeholder_text='Token', textvariable=self.token_variable, width=280)
        self.token_entry.grid(column=2, row=1, padx=(10,0))

        self.save_btn = ctk.CTkButton(self.token_frame, text="Save", width=60, command=self.save_api_key)
        self.save_btn.grid(column=1, row=3, pady=10, columnspan=2)
        self.save_btn.configure(state='disabled')

        self.token_variable.trace('w', self.check_entries)
    
    def _disable_exit(self):
        pass

    def check_entries(self, *args):
        token = self.token_variable.get()
        if token.rstrip():
            self.save_btn.configure(state='normal')
        else:
            self.save_btn.configure(state='disabled')

    def save_api_key(self):
        token = self.token_variable.get().rstrip()
        with open('functions/token.txt', 'w+') as f:
            f.write(token)
        self.destroy()
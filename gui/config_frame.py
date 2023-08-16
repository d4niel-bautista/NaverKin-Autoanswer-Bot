import customtkinter as ctk

class Configs(ctk.CTkFrame):
    def __init__(self, master, width=240, height=380, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.configs_label = ctk.CTkLabel(self, text='Configuration:', font=ctk.CTkFont(family="Arial", size=16))
        self.configs_label.grid(columnspan = 2, padx=20, pady=5, column=0, sticky='w')

        self.configs_container = ctk.CTkScrollableFrame(self)
        self.configs_container.grid(row=2, column=0, sticky='nswe')
        self.configs_container.grid_columnconfigure(0, weight=1)

        self.prescript_label = ctk.CTkLabel(self.configs_container, text='Prescript', font=ctk.CTkFont(family="Arial", size=14))
        self.prescript_label.grid(columnspan = 2, padx=24, pady=0, column=0, sticky='w', row=1)

        self.prescript_textbox = ctk.CTkTextbox(self.configs_container, font=ctk.CTkFont(family="Arial", size=14), height=80)
        self.prescript_textbox.grid(columnspan = 2, padx=20, pady=(0,10), column=0, sticky='we', row=2)

        self.postscript_label = ctk.CTkLabel(self.configs_container, text='Postscript', font=ctk.CTkFont(family="Arial", size=14))
        self.postscript_label.grid(columnspan = 2, padx=24, pady=0, column=0, sticky='w', row=3)

        self.postscript_textbox = ctk.CTkTextbox(self.configs_container, font=ctk.CTkFont(family="Arial", size=14), height=80)
        self.postscript_textbox.grid(columnspan = 2, padx=20, pady=(0,10), column=0, sticky='we', row=4)

        self.prompt_label = ctk.CTkLabel(self.configs_container, text='Prompt', font=ctk.CTkFont(family="Arial", size=14))
        self.prompt_label.grid(columnspan = 2, padx=24, pady=0, column=0, sticky='w', row=5)

        self.prompt_textbox = ctk.CTkTextbox(self.configs_container, font=ctk.CTkFont(family="Arial", size=14), height=80)
        self.prompt_textbox.grid(columnspan = 2, padx=20, pady=(0,10), column=0, sticky='we', row=6)

        self.prescript_textbox.bind("<KeyRelease>", self.update_prescript)
        self.postscript_textbox.bind("<KeyRelease>", self.update_postscript)
        self.prompt_textbox.bind("<KeyRelease>", self.update_prompt)

        self.load_prescript()
        self.load_postscript()
        self.load_prompt()
    
    def update_prescript(self, e):
        content = e.widget.get(1.0, "end-1c").encode('euc-kr')
        with open('prescript.txt', 'wb+') as f:
            f.write(content)

    def update_postscript(self, e):
        content = e.widget.get(1.0, "end-1c").encode('euc-kr')
        with open('postscript.txt', 'wb+') as f:
            f.write(content)

    def update_prompt(self, e):
        content = e.widget.get(1.0, "end-1c").encode('euc-kr')
        with open('prompt.txt', 'wb+') as f:
            f.write(content)

    def load_prescript(self):
        with open('prescript.txt', 'rb+') as f:
            self.prescript_textbox.insert('insert', f.read().decode('euc-kr'))

    def load_postscript(self):
        with open('postscript.txt', 'rb+') as f:
            self.postscript_textbox.insert('insert', f.read().decode('euc-kr'))
    
    def load_prompt(self):
        with open('prompt.txt', 'rb+') as f:
            self.prompt_textbox.insert('insert', f.read().decode('euc-kr'))
        
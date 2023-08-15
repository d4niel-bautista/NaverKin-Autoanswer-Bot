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
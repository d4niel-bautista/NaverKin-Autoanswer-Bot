import customtkinter as ctk

class Interests(ctk.CTkFrame):
    def __init__(self, master, width=240, height=380, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.interests_label = ctk.CTkLabel(self, text='Interests:', font=ctk.CTkFont(family="Arial", size=16))
        self.interests_label.grid(columnspan = 2, padx=20, pady=5, column=0, sticky='w')

        self.interests_container = ctk.CTkScrollableFrame(self)
        self.interests_container.grid(row=2, column=0, sticky='nswe')

        
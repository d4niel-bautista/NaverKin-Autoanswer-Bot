import customtkinter as ctk

class Header(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_propagate(False)
            self.grid_columnconfigure(0, weight=1)
            
            self.title = ctk.CTkLabel(self, text="NaverKin Autoanswer Bot", font=ctk.CTkFont(family="Arial", size=40), anchor="center")
            self.title.grid(pady=20)

            self.description = ctk.CTkLabel(self, text="A bot automating answering on Naver Kin using OpenAI ChatGPT.", font=ctk.CTkFont(family="Arial", size=24), anchor="center", wraplength=400)
            self.description.grid()
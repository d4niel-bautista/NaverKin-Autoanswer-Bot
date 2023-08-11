import customtkinter as ctk
from gui.header import Header
from gui.left_frame import Interests
from gui.right_frame import ProhibitedWords
import os

class NaverKinAnswerBot(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NaverKin Answer Bot")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 700
        self.window_height = 600
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.grid_columnconfigure((0, 3), weight=1)

        self.header = Header(master=self, width = 600, height = 150)
        self.header.grid(pady=(10, 5), columnspan=2, column=1, padx=3)

        self.left_frame = Interests(self, width=160)
        self.left_frame.grid(column=1, row=2, sticky='ewns', padx=3)

        self.right_frame = ProhibitedWords(self, width=350)
        self.right_frame.grid(column=2, row=2, sticky='wens', padx=3)

        self.start_btn = ctk.CTkButton(self, text="Start")
        self.start_btn.grid(column =1, columnspan=2, row=3, pady=10)

if __name__ == "__main__":
    if not os.path.isfile('prohibited_words.txt'):
        with open('prohibited_words.txt', 'a+') as f:
            f.close()
    if not os.path.isfile('creds.txt'):
        with open('creds.txt', 'a+') as f:
            f.close()
    app = NaverKinAnswerBot()
    app.mainloop()
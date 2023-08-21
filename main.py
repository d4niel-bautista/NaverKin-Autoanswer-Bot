import customtkinter as ctk
from gui.header import Header
from gui.interests_frame import Interests
from gui.prohib_words_frame import ProhibitedWords
from gui.answering_configs import Configs
from gui.crawler_configs import CrawlerConfigs
import os
from functions.crawler import NaverKinCrawler
import threading

class NaverKinAnswerBot(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NaverKin Answer Bot")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 920
        self.window_height = 745
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.grid_columnconfigure((0, 4), weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.header = Header(master=self, width = 600, height = 150)
        self.header.grid(pady=(10, 5), columnspan=3, column=1, padx=3)

        self.interests = Interests(self, width=160, height=420)
        self.interests.grid(column=1, row=2, sticky='ewns', padx=3)

        self.prohib_words = ProhibitedWords(self, width=350)
        self.prohib_words.grid(column=2, row=2, sticky='wens', padx=3)

        self.configs = Configs(self, width=350)
        self.configs.grid(column=3, row=2, sticky='wens', padx=3)

    
        self.start_btn = ctk.CTkButton(self, text="Start", command=self.start)
        self.start_btn.grid(column=1, columnspan=3, row=4, pady=10, sticky='ns')

        self.stop_btn = ctk.CTkButton(self, text="Stop", command=self.stop)

        self.naverbot = NaverKinCrawler(obj=self)

        self.crawler_configs = CrawlerConfigs(self, self.naverbot)
        self.crawler_configs.grid(column =1, columnspan=3, row=3, pady=(10,0), ipadx=20)
    
    def start(self):
        self.prohib_words.add_prohib_word_btn.configure(state='disabled')
        for i in self.prohib_words.prohib_words_container.winfo_children():
            i.prohib_word_entry.configure(state='readonly')
            i.delete_button.configure(state='disabled')
        self.configs.prescript_textbox.configure(state='disabled')
        self.configs.postscript_textbox.configure(state='disabled')
        self.configs.prompt_textbox.configure(state='disabled')
        self.start_btn.configure(state='disabled')
        self.start_btn.grid_forget()
        self.stop_btn.grid(column =1, columnspan=3, row=4, pady=10, sticky='ns')
        def start_thread(self):
            self.naverbot.start()
        thread = threading.Thread(target=lambda x=self:start_thread(x), daemon=True)
        thread.start()
    
    def stop(self):
        self.naverbot.stop = True
        self.stop_btn.grid_forget()
        self.start_btn.grid(column =1, columnspan=3, row=4, pady=10, sticky='ns')
    
    def return_widgets_to_normal(self):
        self.prohib_words.add_prohib_word_btn.configure(state='normal')
        for i in self.prohib_words.prohib_words_container.winfo_children():
            i.prohib_word_entry.configure(state='normal')
            i.delete_button.configure(state='normal')
        self.configs.prescript_textbox.configure(state='normal')
        self.configs.postscript_textbox.configure(state='normal')
        self.configs.prompt_textbox.configure(state='normal')
        self.start_btn.configure(state='normal')

if __name__ == "__main__":
    if not os.path.isfile('prohibited_words.txt'):
        with open('prohibited_words.txt', 'a+') as f:
            f.close()
    if not os.path.isfile('creds.txt'):
        with open('creds.txt', 'a+') as f:
            f.close()
    if not os.path.isfile('logs/answered_ids.txt'):
        with open('logs/answered_ids.txt', 'a+') as f:
            f.close()
    if not os.path.isfile('logs/answering_logs.txt'):
        with open('logs/answering_logs.txt', 'a+') as f:
            f.close()
    app = NaverKinAnswerBot()
    app.mainloop()
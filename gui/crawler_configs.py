import customtkinter as ctk
import json

class CrawlerConfigs(ctk.CTkFrame):
    def __init__(self, master, naverbot, **kwargs):
        super().__init__(master, **kwargs)
        self.naverbot = naverbot
        self.grid_columnconfigure((0,4), weight=1)
        self.grid_rowconfigure((0,3), weight=1)

        self.interval_values = ["1 min", "2 mins", "3 mins", "5 mins", "10 mins", "15 mins", "20 mins", "30 mins", "45 mins", "60 mins"]

        self.page_refresh_label = ctk.CTkLabel(self, text="Page refresh:")
        self.page_refresh_label.grid(column=1, row=1, pady=(10, 5), padx=10, sticky='w')

        self.page_refresh_variable = ctk.StringVar()
        self.page_refresh_interval = 0
        self.page_refresh_interval_menu = ctk.CTkOptionMenu(self, values=self.interval_values, variable=self.page_refresh_variable, command=self.set_page_refresh_interval, width=90)
        self.page_refresh_interval_menu.grid(column=1, row=1, padx=(95,15), columnspan=2, sticky='w')

        self.max_page_label = ctk.CTkLabel(self, text="Max page:")
        self.max_page_label.grid(column=1, row=2, pady=(5, 10), padx=10, sticky='w')

        self.max_page_values = [str(i) for i in range(1,15+1)]
        self.max_page_variable = ctk.StringVar()
        self.max_page_menu = ctk.CTkOptionMenu(self, values=self.max_page_values, variable=self.max_page_variable, command=self.set_max_page, width=50, anchor='c')
        self.max_page_menu.grid(column=1, row=2, pady=(5, 10), padx=(80,15), sticky='w', columnspan=2)

        self.next_question_label = ctk.CTkLabel(self, text="Next question:")
        self.next_question_label.grid(column=3, row=1, pady=(10, 5), padx=10, sticky='w')

        self.question_delay_variable = ctk.StringVar()
        self.question_delay_interval = 0
        self.question_delay_interval_menu = ctk.CTkOptionMenu(self, values=self.interval_values, variable=self.question_delay_variable, command=self.set_next_question_interval, width=90)
        self.question_delay_interval_menu.grid(column=3, row=1, padx=(100,0), columnspan=2, sticky='w')

        self.submit_answer_checkbox = ctk.CTkCheckBox(self, text='Submit Answer', command=self.submit_answer, checkbox_height=20, checkbox_width=20)
        self.submit_answer_checkbox.grid(column=3, row=2, pady=(5, 10), padx=10, sticky='w')

        self.init_configs()
    
    def submit_answer(self):
        self.naverbot.submit_answer = self.submit_answer_checkbox.get()
    
    def set_next_question_interval(self, interval):
        interval = interval.split(" ")
        value = int(interval[0]) * 60

        self.question_delay_interval = value
        self.naverbot.question_delay_interval = int(self.question_delay_interval)
        self.save_configs()

    def set_page_refresh_interval(self, interval):
        interval = interval.split(" ")
        value = int(interval[0]) * 60

        self.page_refresh_interval = value
        self.naverbot.page_refresh_interval = int(self.page_refresh_interval)
        self.save_configs()
    
    def set_max_page(self, page_count):
        self.naverbot.max_page = int(page_count)
        self.save_configs()
    
    def default_configs(self):
        self.question_delay_interval_menu.set('15 mins')
        self.page_refresh_interval_menu.set('30 mins')
        self.max_page_menu.set(1)

        self.set_page_refresh_interval('30 mins')
        self.set_next_question_interval('15 mins')
        self.set_max_page(1)

    def init_configs(self):
        try:
            with open('functions/crawler_configs.json', 'r') as f:
                configs = json.load(f)
                self.question_delay_interval_menu.set(configs['next_question_delay'])
                self.page_refresh_interval_menu.set(configs['page_refresh_interval'])
                self.max_page_menu.set(configs['max_page'])

                self.set_page_refresh_interval(configs['page_refresh_interval'])
                self.set_max_page(configs['max_page'])
                self.set_next_question_interval(configs['next_question_delay'])

                print(self.naverbot.submit_answer, self.naverbot.question_delay_interval, self.naverbot.page_refresh_interval, self.naverbot.max_page)
        except Exception as e:
            print('opening json', e)
            self.default_configs()
            self.save_configs()
    
    def save_configs(self):
        with open('functions/crawler_configs.json', 'w+') as f:
            configs = {}
            configs['next_question_delay'] = self.question_delay_interval_menu.get()
            configs['page_refresh_interval'] = self.page_refresh_interval_menu.get()
            configs['max_page'] = int(self.max_page_menu.get())
            configs['submit_answer'] = self.submit_answer_checkbox.get()
            json.dump(configs, f)
        
        

import customtkinter as ctk
import json
from gui.login import Login

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

        self.next_question_label = ctk.CTkLabel(self, text="Submit delay:")
        self.next_question_label.grid(column=3, row=1, pady=(10, 5), padx=10, sticky='w')

        self.question_delay_variable = ctk.StringVar()
        self.question_delay_interval = 0
        self.question_delay_interval_menu = ctk.CTkOptionMenu(self, values=self.interval_values, variable=self.question_delay_variable, command=self.set_next_question_interval, width=90)
        self.question_delay_interval_menu.grid(column=3, row=1, padx=(100,0), columnspan=2, sticky='w')

        self.submit_answer_checkbox = ctk.CTkCheckBox(self, text='Submit Answer', command=self.submit_answer, checkbox_height=20, checkbox_width=20)
        self.submit_answer_checkbox.grid(column=3, row=2, pady=(5, 10), padx=10, sticky='w')

        self.login_account = ctk.CTkButton(self, text="LOGIN\nACCOUNT", command=self.open_login_widget, width=90, height=70)
        self.login_account.grid(column=5, row=1, rowspan=2, padx=(5,20))

        self.answered_questions_label = ctk.CTkLabel(self.master.questions_status, text="Answered questions: 0/")
        self.answered_questions_label.grid(column=1, row=1, sticky='e', pady=(5,0))

        self.max_questions_values = [str(i*10) for i in range(1,10)]
        self.max_questions_values += [str(i*100) for i in range(1,10)]
        self.max_questions_count_variable = ctk.StringVar()
        self.max_questions_answered_per_day = ctk.CTkOptionMenu(self.master.questions_status, values=self.max_questions_values, width=45, height=24, variable=self.max_questions_count_variable, command=self.set_max_questions_count)
        self.max_questions_answered_per_day.grid(column=2, row=1, sticky='w', pady=(5,0))

        self.restart_delay_labels = ctk.CTkLabel(self.master.questions_status, text="Restart after: ")
        self.restart_delay_labels.grid(column=3, row=1, sticky='e', pady=(5,0), padx=(20,0))

        self.restart_delay_values = [str(i) + ' hrs' for i in range(12,25)]
        self.restart_delay_variable = ctk.StringVar()
        self.restart_delay = ctk.CTkOptionMenu(self.master.questions_status, values=self.restart_delay_values, width=45, height=24, variable=self.restart_delay_variable, command=self.set_restart_delay)
        self.restart_delay.grid(column=4, row=1, sticky='w', pady=(5,0))

        self.init_configs()
    
    def open_login_widget(self):
        login = Login(self)
    
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

    def set_max_questions_count(self, max_count):
        max_count = int(max_count)
        self.naverbot.max_questions_answered_per_day = max_count
        self.save_configs()
    
    def set_restart_delay(self, restart_delay):
        restart_delay = (60 * 60) * int(restart_delay.split(' ')[0])
        print(self.naverbot.restart_delay)
        self.naverbot.restart_delay = restart_delay
        print(self.naverbot.restart_delay)
        self.save_configs()
    
    def default_configs(self):
        self.question_delay_interval_menu.set('15 mins')
        self.page_refresh_interval_menu.set('30 mins')
        self.max_page_menu.set(1)
        self.max_questions_answered_per_day.set('10')
        self.restart_delay.set('24 hrs')

        self.set_page_refresh_interval('30 mins')
        self.set_max_page(1)
        self.set_next_question_interval('15 mins')

    def init_configs(self):
        try:
            with open('functions/crawler_configs.json', 'r') as f:
                configs = json.load(f)
                self.question_delay_interval_menu.set(configs['next_question_delay'])
                self.page_refresh_interval_menu.set(configs['page_refresh_interval'])
                self.max_page_menu.set(configs['max_page'])
                self.max_questions_answered_per_day.set(configs['max_answers_per_day'])
                self.restart_delay.set(str(configs['restart_delay']) + ' hrs')

                self.set_page_refresh_interval(configs['page_refresh_interval'])
                self.set_max_page(configs['max_page'])
                self.set_next_question_interval(configs['next_question_delay'])
                self.set_max_questions_count(configs['max_answers_per_day'])
                self.set_restart_delay(str(configs['restart_delay']) + ' hrs')
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
            configs['max_answers_per_day'] = int(self.max_questions_count_variable.get())
            configs['restart_delay'] = int(self.restart_delay_variable.get().split(' ')[0])
            json.dump(configs, f)
        
        

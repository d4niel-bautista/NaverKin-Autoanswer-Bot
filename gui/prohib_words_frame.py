import customtkinter as ctk

class ProhibitedWords(ctk.CTkFrame):
    def __init__(self, master, width=300, **kwargs):
        super().__init__(master, width=width, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.prohib_words_label = ctk.CTkLabel(self, text='Prohibited Words:', font=ctk.CTkFont(family="Arial", size=16))
        self.prohib_words_label.grid(columnspan = 2, padx=20, pady=5, column=0, sticky='w', row=1)

        self.prohib_words_container = ctk.CTkFrame(self)
        self.prohib_words_container.grid(sticky='nswe', column=0, row=2)
        self.prohib_words_container.grid_columnconfigure(0, weight=1)
        self.prohib_words_container.grid_rowconfigure(2, weight=1)

        self.prohibited_words_textbox = ctk.CTkTextbox(self.prohib_words_container, font=ctk.CTkFont(family="Arial", size=14))
        self.prohibited_words_textbox.grid(padx=15, pady=15, column=0, sticky='nsew', row=2)

        self.prohibited_words_textbox.bind("<KeyRelease>", self.update_prohibited_words)

        self.load_prohibited_words()
        # self.add_prohib_word_btn = ctk.CTkButton(self, text='Add Prohibited Word', command=self.add_prohibited_word)
        # self.add_prohib_word_btn.grid(column = 0, columnspan=2, sticky='s', row=3, pady=8)
        # self.init_words()

    def update_prohibited_words(self, e):
        content = e.widget.get(1.0, "end-1c").encode('euc-kr')
        with open('prohibited_words.txt', 'wb+') as f:
            f.write(content)
    
    def load_prohibited_words(self):
        with open('prohibited_words.txt', 'rb+') as f:
            self.prohibited_words_textbox.insert('insert', f.read().decode('euc-kr'))
    
    # def add_prohibited_word(self):
    #     prohib_word = ProhibWordItem(self.prohib_words_container)
    #     prohib_word.grid(pady=3, sticky='we')

    #     with open('prohibited_words.txt', 'ab+') as f:
    #         f.write('\n'.encode('euc-kr'))
    
    # def init_words(self):
    #     with open("prohibited_words.txt", "rb+") as f:
    #         items = [line.decode('euc-kr') for line in f.readlines()]
    #     for i in items:
    #         prohib_word = ProhibWordItem(self.prohib_words_container, i.rstrip())
    #         prohib_word.grid(pady=3)


# class ProhibWordItem(ctk.CTkFrame):
#     def __init__(self, master, prohibited="", height=40, width=340, **kwargs):
#         super().__init__(master, height=height, width=width, **kwargs)
#         self.grid_columnconfigure((0,3), weight=1)
#         self.grid_rowconfigure((0,2), weight=1)
#         self.grid_propagate(False)

#         self.delete_button = ctk.CTkButton(self, text="X", fg_color="transparent", hover_color="gray", width=5, corner_radius=10, command=self.delete_word)
#         self.delete_button.grid(column=2, row=1, padx=3)

#         vcmd_prohib_text = (self.register(self.update_word), r'%P', r'%s')

#         self.prohib_word_entry = ctk.CTkEntry(self, width=290)
#         self.prohib_word_entry.grid(column=1, row=1, padx=3, sticky='we')

#         self.prohib_word_entry.insert(0, '')
#         self.prohib_word_entry.insert(0, prohibited)
#         self.prohib_word_entry.configure(validate='all', validatecommand=vcmd_prohib_text)

#     def update_word(self, P, s):
#         with open("prohibited_words.txt", "rb+") as read:
#             words = [i.decode('euc-kr').rstrip() for i in read.readlines()]
#         prev = s.rstrip()
#         words[words.index(prev)] = P.rstrip()
#         with open("prohibited_words.txt", "wb+") as write:
#             write.writelines(word.encode('euc-kr') + "\n".encode('euc-kr') for word in words)
#         return True

#     def delete_word(self):
#         to_delete = self.prohib_word_entry.get().rstrip()
#         with open("prohibited_words.txt", "rb+") as read:
#             words = [i.decode('euc-kr').rstrip() for i in read.readlines()]
#             words.remove(to_delete)
            
#             with open("prohibited_words.txt", "wb+") as write:
#                 write.writelines(word.encode('euc-kr') + "\n".encode('euc-kr') for word in words)
#         self.destroy()

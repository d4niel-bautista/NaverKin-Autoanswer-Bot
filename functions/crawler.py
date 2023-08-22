import undetected_chromedriver as uc
import time
from selenium.webdriver import ChromeOptions
import pyperclip
from bs4 import BeautifulSoup
import json
from functions.chatgpt import generate_response
from functions.window_getter import bring_window_to_front
import pyautogui
import re
import os
from datetime import datetime
from functions.get_chromedriver import get_chrome_browser_version, download_chromedriver

chrome_data_path = 'AppData/Local/Google/Chrome/User Data'
current_user = os.path.expanduser('~')
user_data_dir = os.path.join(current_user, chrome_data_path)

dirname = os.path.dirname(__file__)
creds_txt = os.path.join(dirname, '../creds.txt')
prohib_words_txt = os.path.join(dirname, '../prohibited_words.txt')
naverkin_cookies_json = os.path.join(dirname, 'naverkin_cookies.json')
HWND_KEYWORDS = ['지식iN', 'Naver Sign in', 'Knowledge iN']
answered_ids_txt = os.path.join(dirname, '../logs/answered_ids.txt')
answering_logs_txt = os.path.join(dirname, '../logs/answering_logs.txt')

class NaverKinCrawler():
    def __init__(self, obj=None):
        self.obj = obj
        self.stop = False
        self.submit_answer = 0
        self.question_delay_interval = 1800
        self.page_refresh_interval = 3600
        self.max_page = 1
        self.max_questions_answered_per_day = 10

    def first_run(self):
        with open(creds_txt) as f:
            creds = [i.rstrip() for i in f.readlines()]
        self.driver.get(r'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fkin.naver.com%2F')
        time.sleep(2)
        pyautogui.press('enter')

        self.driver.execute_script("document.getElementById('keep').click()")

        time.sleep(1)
        pyperclip.copy(creds[0])
        user_field = self.driver.find_element('xpath', '//*[@id="id"]')
        user_field.click()
        time.sleep(1.7)
        user_field.clear()
        time.sleep(1.7)
        user_field.click()
        # for i in creds[0]:
        #     user_field.send_keys(i)
        #     time.sleep(0.2)
        self.focus_browser_window()
        pyautogui.hotkey('ctrl', 'v')

        time.sleep(2)
        pyautogui.press('tab')
        time.sleep(1)
        
        pyperclip.copy(creds[1])
        pwd_field = self.driver.find_element('xpath', '//*[@id="pw"]')
        pwd_field.click()
        time.sleep(1.7)
        pwd_field.clear()
        time.sleep(1.7)
        pwd_field.click()
        # for i in creds[1]:
        #     pwd_field.send_keys(i)
        #     time.sleep(0.2)
        self.focus_browser_window()
        pyautogui.hotkey('ctrl', 'v')

        time.sleep(2)
        login_btn = self.driver.find_element('xpath', '//*[@id="log.login"]')
        login_btn.click()
        time.sleep(3)
        try:
            pwd_field = self.driver.find_element('xpath', '//*[@id="pw"]')
            pwd_field.click()
            self.focus_browser_window()
            pyautogui.hotkey('ctrl', 'v')

            self.sleep(20)

            login_btn = self.driver.find_element('xpath', '//*[@id="log.login"]')
            login_btn.click()
            time.sleep(5)
        except Exception as e:
            print(e)
        self.driver.get('https://kin.naver.com/')
        self.sleep(8)
        self.set_view_type()
        time.sleep(2)
        self.save_cookies()

    def get_interests(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        interests_ul = soup.find('ul', {'class': 'directory_list _interest_list'})
        items = [i.find('a').extract() for i in interests_ul.find_all('li')]
        interests = {}
        for i in items:
            if len(i.find_all()) >= 1:
                for j in range(len(i.find_all())):
                    i.find_all()[j].decompose()
            interests[i.text] = '''[onclick="%s"]''' % i['onclick']
        return interests

    def set_view_type(self):
        self.driver.execute_script('''document.querySelector(`[onclick="nhn.Kin.Utility.nClicks('ldl.con', '', '', event);"]`).click()''')
        self.driver.execute_script('document.getElementsByClassName("type_title _onlyTitleTypeBtn")[0].click()')
        self.driver.execute_script('''document.getElementsByClassName("_countPerPageValue _param('10')")[0].click()''')
        self.driver.execute_script('''document.querySelector(`a[onclick="nhn.Kin.Utility.nClicks('nql_lgd.latest', '', '', event);"]`).click()''')
    
    def get_valid_questions(self):
        question_list = self.driver.find_element('xpath', '//*[@id="questionListTypeTitle"]')
        if question_list.get_attribute('style') == 'display: none;':
            return []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        question_items = soup.find_all('div', class_ = 'answer_box')
        question_links = []

        if len(question_items):
            for i in question_items:
                if len(i.find_all('span', {'class': 'ico_picture sp_common'})) + len(i.find_all('span', {'class': 'ico_file sp_common'})) + int(i.find('span', {'class': 'num_answer'}).find('em').text) == 0:
                    if self.check_if_text_has_prohibited_word(i.find('span', {'class': 'tit_txt'}).text):
                        continue
                    if i.find('a', {'class': '_first_focusable_link'})['href'].rstrip() in self.answered_ids:
                        continue
                    question_links.append(i.find('a', {'class': '_first_focusable_link'})['href'].rstrip())
                    print(i.find('a', {'class': '_first_focusable_link'})['href'].rstrip())
                    print(i.find('span', {'class': 'tit_txt'}).text)
                    break
        return question_links
    
    def answer_question(self, link):
        if link in self.answered_ids:
            return
        self.driver.get('https://kin.naver.com' + link)
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass
        time.sleep(2)
        self.driver.find_element('xpath', '//*[@id="content"]/div[1]/div/div[1]')
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        question_content = soup.select_one('div.c-heading._questionContentsArea')

        [i.decompose() for i in question_content.find_all('span', {'class' : 'blind'})]
        [i.decompose() for i in question_content.find_all('span', {'class' : 'grade-point'})]
        question_content_cleaned = re.sub('\t+', '', question_content.text)
        question_content_cleaned = re.sub('\n{1,}', '\n', question_content_cleaned)
        question_content_cleaned = question_content_cleaned.strip()

        if self.check_if_text_has_prohibited_word(question_content_cleaned):
            return
        
        response = generate_response(question_content_cleaned)
        self.driver.find_element('xpath', "//*[contains(@class, 'se-ff-nanumgothic se-fs15')]")
        time.sleep(1)

        finalized_response = ''
        if self.prescript.rstrip() != '':
            finalized_response += self.prescript + "\n"
        finalized_response += response
        if self.postscript.rstrip() != '':
            finalized_response += '\n' + self.postscript
        
        time.sleep(1)
        pyperclip.copy(finalized_response)
        time.sleep(1)
        self.focus_browser_window()
        textarea = self.driver.find_element('xpath', '//*[@id="smartEditor"]/div/div/div/div[1]/div/section/article')
        textarea.click()
        pyautogui.hotkey('ctrl', 'v')
        self.answering_log(question_content_cleaned, response)

        self.sleep(int(self.question_delay_interval))

        if self.submit_answer:
            self.driver.execute_script("document.querySelector('#answerRegisterButton').click()")
            self.save_answered_id(link)
            self.answered_ids.append(link.rstrip())
            self.questions_answered_count += 1
            self.obj.crawler_configs.answered_questions_label.configure(text=f'Answered questions: {self.questions_answered_count}/')
        self.sleep(int(self.question_delay_interval)/4)

    def load_answered_ids(self):
        with open(answered_ids_txt, 'r+') as f:
            answered_ids = [i.rstrip() for i in f.readlines()]
            return answered_ids

    def save_answered_id(self, id):
        with open(answered_ids_txt, 'a+') as f:
            f.write(id + '\n')

    def answering_log(self, question, response):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        finalized_response = ''
        if self.prescript.rstrip() != '':
            finalized_response += self.prescript + "\n"
        finalized_response += response
        if self.postscript.rstrip() != '':
            finalized_response += '\n' + self.postscript
        
        try:
            with open(answering_logs_txt, 'a+', encoding='euc-kr', errors='replace') as f:
                f.write(str(dt_string + '\n' +
                    question + 
                    '\n---------------\n' + 
                    finalized_response +
                    '\n==================================================\n\n'))
        except Exception as e:
            print('WRITING LOG TO TXT ERROR')
            print(e)
        
        print(dt_string + '\n' +
            question + 
            '\n---------------\n' + 
            finalized_response +
            '\n==================================================\n')
 
    def save_cookies(self):
        with open(naverkin_cookies_json, 'w+') as f:
            json.dump(self.driver.get_cookies(), f)
        print("cookies saved")
    
    def load_cookies(self):
        try:
            with open(naverkin_cookies_json, 'r') as f:
                COOKIES = json.load(f)
            [self.driver.add_cookie(i) for i in COOKIES]
        except Exception as e:
            print(e)

    def load_prohibited_words(self):
        with open(prohib_words_txt, 'rb+') as f:
            prohib_words = [i.decode('euc-kr').rstrip() for i in f.readlines() if i.decode('euc-kr').rstrip()]
            return prohib_words
        
    def load_prescript_and_postcript(self):
        with open('prescript.txt', 'rb+') as f:
            prescript = f.read().decode('euc-kr')
        with open('postscript.txt', 'rb+') as f:
            postscript = f.read().decode('euc-kr')
        return prescript, postscript
    
    def check_if_text_has_prohibited_word(self, text):
        if self.prohibited_words:
            for word in self.prohibited_words:
                if word in text:
                    print('SKIPPED! HAS PROHIBITED WORD: ' + word + '\n')
                    return True
        return False
    
    def init_driver(self):
        options = ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument('--start-maximized')

        if int(get_chrome_browser_version()) >= 115:
            self.driver = uc.Chrome(use_subprocess=True, options=options, driver_executable_path=download_chromedriver())
        else:
            self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(20)
    
    def focus_browser_window(self):
        try:
            bring_window_to_front(HWND_KEYWORDS)
        except:
            pyautogui.press("alt")
            bring_window_to_front(HWND_KEYWORDS)

    def start(self):
        self.stop = False
        try:
            self.init_driver()
        except Exception as e:
            print(e)
            self.obj.return_widgets_to_normal()
            self.obj.stop()
            pass
        try:
            if os.path.isfile(naverkin_cookies_json):
                self.main()
                self.driver.quit()
            else:
                self.first_run()
                self.driver.quit()
        except Exception as e:
            print(e)
            self.driver.quit()
        self.obj.return_widgets_to_normal()
        self.obj.stop()
        print('DONE')
    
    def main(self):
        self.driver.get('https://kin.naver.com/test')
        time.sleep(2)
        self.load_cookies()

        if self.stop:
            return
        self.answered_ids = self.load_answered_ids()

        if self.stop:
            return
        self.driver.get(r'https://kin.naver.com/')
        pyautogui.press('enter')
        self.sleep(10)
        self.save_cookies()

        # if self.stop:
        #     return
        # self.obj.interests.init_interests(list(self.get_interests().keys()))

        if self.stop:
            return
        self.set_view_type()

        if self.stop:
            return
        self.prohibited_words = self.load_prohibited_words()
        self.prescript, self.postscript = self.load_prescript_and_postcript()

        #MAIN LOOP
        while not self.stop:
            self.questions_answered_count = 0
            while self.questions_answered_count < self.max_questions_answered_per_day:
                self.driver.get(r'https://kin.naver.com/')
                try:
                    self.driver.switch_to.alert.accept()
                except:
                    pass
                time.sleep(2)
                self.set_view_type()
                self.sleep(8)
                links = []
                idx = 1
                first_page_done = False
                page = 1
                while page <= self.max_page:
                    try:
                        if self.stop:
                            return
                        page_element = self.driver.find_element('xpath', f'//*[@id="pagingArea1"]/a[{idx}]')
                        page_element.click()
                        time.sleep(1)
                        links += self.get_valid_questions()
                        print(len(links))
                        idx += 1
                        if not first_page_done:
                            if idx > 11:
                                first_page_done = True
                                idx = 3
                        else:
                            if idx > 12:
                                idx = 3
                        time.sleep(2)
                        page += 1
                    except Exception as e:
                        print(e)
                        break
                self.sleep(5)
                for i in links:
                    if self.stop:
                        break
                    self.answer_question(i)
                self.sleep(int(self.page_refresh_interval))
            print(f"MAX ANSWERS COUNT REACHED {self.questions_answered_count}/{self.max_questions_answered_per_day}")
            self.sleep(43200)
        return
    
    def sleep(self, interval):
        for i in range(int(interval)):
            if self.stop:
                break
            time.sleep(1)

if __name__ == '__main__':
    z = NaverKinCrawler()
    z.start()
    
    time.sleep(100000)
        

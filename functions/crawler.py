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

dirname = os.path.dirname(__file__)
creds_txt = os.path.join(dirname, '../creds.txt')
prohib_words_txt = os.path.join(dirname, '../prohibited_words.txt')
naverkin_cookies_json = os.path.join(dirname, 'naverkin_cookies.json')
HWND_KEYWORDS = ['지식iN', 'Naver Sign in']

class NaverKinCrawler():
    def __init__(self, obj=None):
        self.obj = obj
        self.options = ChromeOptions()

    def login_naverkin(self):
        with open(creds_txt) as f:
            creds = [i.rstrip() for i in f.readlines()]
        self.driver.get(r'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fkin.naver.com%2F')

        time.sleep(3)
        self.load_cookies()
        time.sleep(2)
        # user_agent = self.driver.execute_script("return navigator.userAgent;")

        self.driver.execute_script("document.getElementById('keep').click()")

        time.sleep(1)
        pyperclip.copy(creds[0])
        user_field = self.driver.find_element('xpath', '//*[@id="id"]')
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

            time.sleep(20)

            login_btn = self.driver.find_element('xpath', '//*[@id="log.login"]')
            login_btn.click()
            time.sleep(5)
        except Exception as e:
            print(e)

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
        self.driver.execute_script('document.getElementsByClassName("type_title _onlyTitleTypeBtn")[0].click()')
        self.driver.execute_script('''document.getElementsByClassName("_countPerPageValue _param('50')")[0].click()''')

    def get_valid_questions(self):
        self.driver.refresh()
        self.driver.find_element('xpath', '//*[@id="questionListTypeTitle"]')
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        question_items = soup.find_all('a', {'class': '_first_focusable_link'})
        question_links = []
        if len(question_items):
            for i in question_items:
                if len(i.find_all('span', {'class': 'ico_picture sp_common'})) == 0:
                    if self.check_if_text_has_prohibited_word(i.find('span', {'class': 'tit_txt'}).text):
                        continue
                    question_links.append(i['href'].rstrip())
                    print(i.find('span', {'class': 'tit_txt'}).text)
        return question_links
    
    def answer_question(self, link):
        self.driver.get('https://kin.naver.com/' + link)
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
        pyperclip.copy(response)
        time.sleep(1)
        self.focus_browser_window()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # self.driver.execute_script("document.querySelector('#answerRegisterButton').click()")
        time.sleep(15)
 
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
            prohib_words = [i.decode('euc-kr').rstrip() for i in f.readlines()]
            return prohib_words
    
    def check_if_text_has_prohibited_word(self, text):
        for word in self.prohibited_words:
            if word in text:
                print('SKIPPED! HAS PROHIBITED WORD: ' + word + '\n')
                return True
        return False
    
    def init_driver(self):
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
        self.options.add_argument('--start-maximized')

        self.driver = uc.Chrome(use_subprocess=True, options=self.options)
        self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(20)
    
    def focus_browser_window(self):
        try:
            bring_window_to_front(HWND_KEYWORDS)
        except:
            pyautogui.press("alt")
            bring_window_to_front(HWND_KEYWORDS)

    def start(self):
        self.init_driver()
        self.login_naverkin()
        time.sleep(10)
        self.save_cookies()
        self.obj.interests.init_interests(list(self.get_interests().keys()))
        self.set_view_type()
        self.prohibited_words = self.load_prohibited_words()
        links = self.get_valid_questions()
        for i in links:
            self.answer_question(i)
        self.obj.return_widgets_to_normal()
        print('DONE')

if __name__ == '__main__':
    z = NaverKinCrawler()
    z.start()
    
    time.sleep(100000)
        

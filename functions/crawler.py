import undetected_chromedriver as uc
import time
from selenium.webdriver import ChromeOptions
import pyperclip
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from chatgpt import generate_response

PROXY = "221.151.181.101:8000"
# COOKIES = [{'domain': '.kin.naver.com', 'httpOnly': False, 'name': 'kin_session', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '"pBiZ1rCCBqKma9vsKxMlKogrFqgqKxnmaqgsKAnmaqgsKAnmaqgsKAnwaqu="'}, {'domain': '.naver.com', 'httpOnly': False, 'name': 'NID_JKL', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'r8GToEyL4msYRPCPZUDHI2AXcn/eAbaLGGsrkb1ielQ='}, {'domain': 'kin.naver.com', 'httpOnly': False, 'name': 'JSESSIONID', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '91D5DACF42DACD7EE86CCE430B281955'}, {'domain': '.naver.com', 'httpOnly': False, 'name': 'NID_SES', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'AAABgeilibLUPhSDeAMEOlLilvE/M8yHNSeXwDbAuM2sigdv5zwtN5kWwLnsc+Tqujwnr54UF/yXEELAPGoh9k6/Bhh5ojMgPMhHIIMjXpE+gn79oOIo62BCs2KlkzJBAGcIKffBXiuotZu7fL7Fq1mB4CqYyFBeRK3ww72oSKiwj80Y6ZLcrC0QcZF4jmsVGkqjsWovHt6JnUps5kh5Ety4HSlYZyQ253eQXH5X7v7ualIrZxlKlufYRFwlVO8cub6GSqiAullufD2NA+Hw3iOBIDpe2ZpGDzgEKqGcCHmC9wfcsD1ch2svPwqrWZedAtjghaJ82rWBPeutP7LFK0SzF2Jc6Q/HtnScvL0/DoZ2ehwACukJ0epF0l0N+roQ8M7W1LOpKQfPPhlDtpj9IU8lOVneVquCRErM6BhSRY+7+ath7H7i5K1xn8iUCNjo0bZL6K1skbhU0q9VkszU/f/DBDq+98lpftcGGnyqmHO7FAhkBC8+o06ww7OwsyXzezRSwwi7UeahGIIf2kgRqmwpGww='}, {'domain': '.naver.com', 'httpOnly': True, 'name': 'NID_AUT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '827PHETY3ZjBpiVPwP7RQULE4VqcVGMsecfs3UzW1/8uy6N+IkIToRzMy7hwPn16'}, {'domain': '.naver.com', 'httpOnly': False, 'name': 'nid_inf', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '-1523225532'}, {'domain': '.naver.com', 'expiry': 1726627035, 'httpOnly': False, 'name': 'NNB', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'L732XD524TNGI'}]

class NaverKinCrawler():
    def __init__(self, obj=None):
        self.obj = obj
        self.agent = UserAgent()
        self.ua = self.agent.random
        self.options = ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument(f'--user-agent={self.ua}')
        # self.options.add_argument(f'--proxy-server={PROXY}')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--incognito')

        self.driver = uc.Chrome(use_subprocess=True, options=self.options)
        self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(20)

    def login_naverkin(self):
        with open('../creds.txt') as f:
            creds = [i.rstrip() for i in f.readlines()]
        self.driver.get(r'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fkin.naver.com%2F')
        try:
            with open('naverkin_cookies.json', 'r') as f:
                COOKIES = json.load(f)
            [self.driver.add_cookie(i) for i in COOKIES]
        except Exception as e:
            print(e)
        
        time.sleep(10)
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        print(user_agent)

        user_field = self.driver.find_element('xpath', '//*[@id="id"]')
        for i in creds[0]:
            user_field.send_keys(i)
            time.sleep(0.2)

        time.sleep(3)
        
        pyperclip.copy(creds[1])
        pwd_field = self.driver.find_element('xpath', '//*[@id="pw"]')
        for i in creds[1]:
            pwd_field.send_keys(i)
            time.sleep(0.2)

        time.sleep(2)
        login_btn = self.driver.find_element('xpath', '//*[@id="log.login"]')
        login_btn.click()
        time.sleep(3)
        try:
            pwd_field = self.driver.find_element('xpath', '//*[@id="pw"]')
            pwd_field.send_keys(creds[1])

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
        for c, i in enumerate(items):
            if len(i.find_all()) >= 1:
                for j in range(len(i.find_all())):
                    i.find_all()[j].decompose()
            interests[i.text] = '''[onclick="%s"]''' % i['onclick']
        print(interests)
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
                    question_links.append(i['href'].rstrip())
                    print(i.find('span', {'class': 'tit_txt'}).text)
        return question_links
    
    def answer_question(self, link):
        self.driver.get('https://kin.naver.com/' + link)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        question_content = soup.find('div', {'class': 'c-heading _questionContentsArea c-heading--default-old'}).find('div', {'class': 'c-heading__content'}).text

        response = generate_response(question_content)
        self.driver.find_element('xpath', "//*[contains(@class, 'se-ff-nanumgothic se-fs15')]")
        self.driver.execute_script('''document.querySelector('[class="se-ff-nanumgothic se-fs15 __se-node"]').innerHTML = arguments[0]''', response)
        # self.driver.execute_script("document.querySelector('#answerRegisterButton').click()")

    def save_cookies(self):
        with open('naverkin_cookies.json', 'w+') as f:
            json.dump(self.driver.get_cookies(), f)
        print("cookies saved")
    
    def start(self):
        self.login_naverkin()
        time.sleep(30)
        self.save_cookies()
        self.get_interests()
        self.set_view_type()
        links = self.get_valid_questions()
        for i in links:
            self.answer_question(i)

if __name__ == '__main__':
    z = NaverKinCrawler()
    z.start()
    time.sleep(100000)
        

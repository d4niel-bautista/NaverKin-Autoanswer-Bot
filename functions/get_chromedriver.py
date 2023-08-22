import subprocess
import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile

dirname = os.path.dirname(__file__)
chromedriver_folder = os.path.join(dirname, '..', 'latest_chromedriver')

def get_chrome_browser_version():
    version = subprocess.Popen('''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"''', stdout=subprocess.PIPE).communicate()[0].decode().strip()
    print('chrome browser version:', version)
    return version.split('.')[0]

def download_chromedriver():
    version = get_chrome_browser_version()
    soup = BeautifulSoup(requests.get("https://googlechromelabs.github.io/chrome-for-testing/").content, 'lxml')
    stable = soup.find('section', {'id':'stable'})
    latest_stable_version = stable.p.code.text

    if latest_stable_version.split('.')[0] == version:
        link = f'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{latest_stable_version}/win64/chromedriver-win64.zip'
        chromedriver_win64 = requests.get(link, allow_redirects=True)
        filename = link.split('/')[-1]
        zip_path = os.path.join(chromedriver_folder, filename)
        os.makedirs(chromedriver_folder, mode=0o755, exist_ok=True)
        with open(zip_path, 'wb') as f:
            f.write(chromedriver_win64.content)
    return extract_chromedriver_zipfile(zip_path, filename)

def extract_chromedriver_zipfile(zip_path, filename):
    with ZipFile(zip_path, 'r') as zf:
        zf.printdir()
        zf.extract(f"{filename.split('.')[0]}/chromedriver.exe", chromedriver_folder)
    os.remove(zip_path)
    chromedriver_path = os.path.join(chromedriver_folder, filename.split('.')[0], "chromedriver.exe")
    os.chmod(chromedriver_path, 0o755)
    return chromedriver_path
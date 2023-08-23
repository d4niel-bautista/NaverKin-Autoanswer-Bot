import subprocess
import requests
import os
from zipfile import ZipFile

dirname = os.path.dirname(__file__)
chromedriver_folder = os.path.join(dirname, '..', 'latest_chromedriver')

def get_chrome_browser_version():
    version = subprocess.Popen('''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"''', stdout=subprocess.PIPE).communicate()[0].decode().strip()
    print('chrome browser version:', version)
    return version.split('.')[0]

def download_chromedriver():
    milestone_version = get_chrome_browser_version()
    json_endpoints = requests.get("https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json").json()
    download_links = json_endpoints['milestones'][milestone_version]['downloads']['chromedriver']
    chromedriver_download_link = [i['url'] for i in download_links if i['platform'] == 'win64'][0]
    chromedriver_win64 = requests.get(chromedriver_download_link, allow_redirects=True)
    filename = chromedriver_download_link.split('/')[-1]
    zip_path = os.path.join(chromedriver_folder, filename)
    os.makedirs(chromedriver_folder, mode=0o755, exist_ok=True)
    with open(zip_path, 'wb') as f:
        f.write(chromedriver_win64.content)
    print(f'DOWNLOADED CHROMEDRIVER {milestone_version}')
    return extract_chromedriver_zipfile(zip_path, filename)

def extract_chromedriver_zipfile(zip_path, filename):
    with ZipFile(zip_path, 'r') as zf:
        zf.printdir()
        zf.extract(f"{filename.split('.')[0]}/chromedriver.exe", chromedriver_folder)
    os.remove(zip_path)
    chromedriver_path = os.path.join(chromedriver_folder, filename.split('.')[0], "chromedriver.exe")
    os.chmod(chromedriver_path, 0o755)
    print("EXTRACTED chromedriver.exe")
    return chromedriver_path
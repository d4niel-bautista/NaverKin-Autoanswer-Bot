import os
import json

dirname = os.path.dirname(__file__)
accounts_folder = os.path.join(dirname, '..', 'accounts')

if not os.path.isdir(accounts_folder):
    os.makedirs(accounts_folder, exist_ok=True)

def get_user_cookies(user):
    user_path = os.path.join(accounts_folder, user)
    if os.path.isfile(os.path.join(user_path, user + '_cookies.json')):
        with open(os.path.join(user_path, user + '_cookies.json'), 'r') as f:
            return json.load(f)
    return False

def get_user_creds(user):
    if os.path.isfile(os.path.join(accounts_folder, user, user + '_login.txt')):
        with open(os.path.join(accounts_folder, user, user + '_login.txt')) as f:
            creds = [i.rstrip() for i in f.readlines()]
            if len(creds) == 2:
                return creds
    return False

def save_user_creds(user, pwd):
    user_path = os.path.join(accounts_folder, user)
    if not os.path.isdir(user_path):
        os.makedirs(user_path, exist_ok = True)
    with open(os.path.join(user_path, user + '_login.txt'), 'w+') as f:
        f.writelines([i + '\n' for i in [user, pwd]])

def save_user_cookies(user, cookies):
    user_path = os.path.join(accounts_folder, user)
    with open(os.path.join(user_path, user + '_cookies.json'), 'w+') as f:
        json.dump(cookies, f)
    print(f"{user} cookies saved")

def get_current_user():
    current_user_path = os.path.join(accounts_folder, '..', 'creds.txt')
    if os.path.isfile(current_user_path):
        with open(current_user_path, 'r') as f:
            user = [i.rstrip() for i in f.readlines()]
            if len(user) == 2:
                return user[0]
    return False

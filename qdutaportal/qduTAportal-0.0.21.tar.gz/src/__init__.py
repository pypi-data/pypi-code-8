#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
from .portal import Portal

SCRIPT_NAME = sys.argv[0].split('/').pop()

Func_dict = {
    '-f': 'force_login',
    '-h': 'help',
    '-s': 'login',
    '-v': 'version',
}

def main():
    print("\n****************************************\n")
    print("* Welcome to QDU Tearching Area Portal *\n")
    print("*             -- powered by Cole Smith *\n")
    print("****************************************\n")

    if len(sys.argv) <= 1:
        menu()
        return

    option = sys.argv[1].strip()

    if option in Func_dict:
        eval(Func_dict.get(option))()
        return

    print('Invalid Options. -h for help.')

def menu():
    print('-h   Get help.')
    print('-f   Force relogin.')
    print('-s   Login normally.')
    print('-v   Get %s version' % SCRIPT_NAME)

def help():
    menu()

def get_user():
    username = None
    password = None
    homedir = os.path.expanduser('~')
    config_dir = homedir + '/.config'
    config_file = config_file + '/qduTAportal_conf.json'
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    if not os.path.isfile(config_file):
        print("First Use This Script!!!")
        username = raw_input("UserName: ")
        password = raw_input("PassWord: ")
        print("Store info in " + config_file)
        # if not os.path.exists('/usr/bin/userinfo.txt'):
        #     os.system('sudo touch /usr/bin/userinfo.txt && sudo chmod 766 /usr/bin/userinfo.txt')
        with open(config_file, 'w') as uif:
            data = json.dumps({
                'username': username,
                'password': password
                }, indent=4)
            uif.write(data)
    else:
        # print("Make sure you UserName & PassWord in file `userinfo.txt` is Right")
        with open(config_file, 'r') as uif:
            # username = uif.readline().strip()
            # password = uif.readline().strip()
            raw_data = uif.read()
            data = json.loads(raw_data)
            username = data.get('username').strip()
            password = data.get('password').strip()

    if username == "" or password == "":
        print("Username or Password cannot be empty.")
        print("Please Check Your Input or File " + config_file)
        username = raw_input("UserName: ")
        password = raw_input("PassWord: ")
        with open(config_file, 'w') as uif:
            data = json.dumps({
                'username': username,
                'password': password
                }, indent=4)
            uif.write(data)
            sys.exit()
    
    return (username, password)

def version():
    print('%s %s\n' % (SCRIPT_NAME, Portal._VERSION))

def login():
    username, password = get_user()

    print("Logining Now, Just Waiting a second ...\n")
    print("(Tips: If failed to login, please check your userinfo in: \n")
    print("\t " + config_file + "\n")

    client = Portal()
    client.re_login_by_time_out(username, password)
    #client.do_heart_beat()

def force_login():
    username, password = get_user()

    print("Logining Now, Just Waiting a second ...\n")
    print("(Tips: If failed to login, please check your userinfo in: \n")
    print("\t " + config_file + "\n")

    client = Portal()
    client.logout()
    client.re_login_by_time_out(username, password)
    #client.do_heart_beat()

if __name__ == '__main__':
    main()

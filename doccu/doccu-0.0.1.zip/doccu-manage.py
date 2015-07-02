import pickle
import sys
import subprocess
import requests
from os.path import expanduser
import os

try:
   input = raw_input
except NameError:
   pass

def generate_id(name,code):
    doccu_home = expanduser("~/.doccu")
    db = pickle.load(open(doccu_home + "/ids.dbs", "rb"))
    if code in db.values():
        print("Code not unique!")
        wait = input("Press enter to exit.")
        sys.exit()
    if name in db.keys():
        print("User already exists!")
        choice = input("Overwrite? Y/N")
        if choice == 'y':
            print("Overwriting...")
        elif choice == 'Y':
            print("Overwriting...")
        else:
            print("Not overwriting.")
            wait = input("Press enter to exit.")
            sys.exit()
    db[name] = code
    pickle.dump(db,open(doccu_home + "/ids.dbs","wb"))
    print("User written to database!")

def remove_id(name):
    doccu_home = expanduser("~/.doccu")
    db = pickle.load(open(doccu_home + "/ids.dbs", "rb"))
    del db[name]
    pickle.dump(db,open(doccu_home + "/ids.dbs","wb"))
    print("User removed from database!")

def update_js():
    doccu_static = expanduser("~/.doccu/static")
    url_request = requests.get('https://raw.githubusercontent.com/bpampuch/pdfmake/master/build/pdfmake.min.js', stream=True)
    with open(doccu_static + '/js/pdfmake.min.js','wb') as fileOpen:
        for chunk in url_request.iter_content(chunk_size=1024):
            if chunk:
                fileOpen.write(chunk)
                fileOpen.flush()
    url_request = requests.get('https://raw.githubusercontent.com/bpampuch/pdfmake/master/build/vfs_fonts.js', stream=True)
    with open(doccu_static + '/js/vfs_fonts.js','wb') as fileOpen:
        for chunk in url_request.iter_content(chunk_size=1024):
            if chunk:
                fileOpen.write(chunk)
                fileOpen.flush() 

def update_template(url, fileName):
    doccu_templates = expanduser("~/.doccu/templates")
    url_request = requests.get(url, stream=True)
    with open(doccu_templates + '/' + fileName, 'wb') as fileOpen:
        for chunk in url_request.iter_content(chunk_size=1024):
            if chunk:
                fileOpen.write(chunk)
                fileOpen.flush()

def update_doccu_server():
    doccu_home = expanduser("~/.doccu")
    url_request = requests.get('https://raw.githubusercontent.com/shakna-israel/doccu-server/master/doccu-server.py', stream=True)
    with open(doccu_home + '/doccu-server.py', 'wb') as fileOpen:
        for chunk in url_request.iter_content(chunk_size=1024):
            if chunk:
                fileOpen.write(chunk)
                fileOpen.flush()

def update_all_templates():
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/index.html','index.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/styles.html','styles.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/sidebar.html','sidebar.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/new_document_submitted.html','new_document_submitted.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/new_document_denied.html','new_document_denied.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/new_document.html','new_document.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/header.html','header.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/edit_document.html','edit_document.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/document.html','document.html')
    update_template('https://raw.githubusercontent.com/shakna-israel/doccu-templates/master/category.html','category.html')

def gen_folder_struct():
    doccu_home = expanduser("~/.doccu")
    doccu_docs = expanduser("~/.doccu/documents")
    doccu_static = expanduser("~/.doccu/static")
    doccu_js = expanduser("~/.doccu/static/js")
    doccu_templates = expanduser("~/.doccu/templates")
    if os.path.isdir(doccu_home):
        if os.path.isdir(doccu_docs):
            if os.path.isdir(doccu_static):
                if os.path.isdir(doccu_js):
                    if os.path.isdir(doccu_templates):
                        return True
                    else:
                        os.makedirs(doccu_templates)
                else:
                    os.makedirs(doccu_js)
                    os.makedirs(doccu_templates)
            else:
                os.makedirs(doccu_static)
                os.makedirs(doccu_js)
                os.makedirs(doccu_templates)
        else:
            os.makedirs(doccu_docs)
            os.makedirs(doccu_static)
            os.makedirs(js)
            os.makedirs(doccu_templates)
    else:
        os.makedirs(doccu_home)
        os.makedirs(doccu_docs)
        os.makedirs(doccu_static)
        os.makedirs(doccu_js)
        os.makedirs(doccu_templates)

def main():
    gen_folder_struct()
    doccu_home = expanduser('~/.doccu')
    choice = input("Enter 1 to ADD a user\n2 to REMOVE a User\n3 to START the server\n4 to updated browser-based dependencies\n5 to updateserver-based dependencies:")
    if str(choice) == '1':
        unique_name = input("Enter a users UNIQUE name, e.g. Trevor Clough: ")
        unique_name = unique_name.strip()
        unique_name = unique_name.lower()
        unique_code = input("Enter a users UNIQUE code, e.g. 00226677 ")
        unique_code = unique_code.strip()
        generate_id(unique_name,unique_code)
        print("Done!")
        wait = input("Press enter to try exit.")
        sys.exit()
    elif str(choice) == '2':
        unique_name = input("Enter the user's UNIQUE name, e.g. Trevor Clough: ")
        unique_name = unique_name.strip()
        remove_id(unique_name)
        print("Done!")
        wait = input("Press enter to try exit.")
        sys.exit()
    elif str(choice) == '3':
        try:
            subprocess.call(["python", doccu_home + "/doccu-server.py"])
        except SystemExit:
            try:
                subprocess.call(["python", doccu_home + "/doccu-server.py"])
            except SystemExit:
                subprocess.call(["python", doccu_home + "/doccu-server.py"])
            except KeyboardInterrupt:
                sys.exit()
        except KeyboardInterrupt:
            sys.exit()
    elif str(choice) == '4':
        print("Updating javascript dependencies...")
        update_js()
        print("Updated!")
    elif str(choice) == '5':
        print("Updating templates...")
        update_all_templates()
        print("Updated!")
    elif str(choice) == '6':
        print("Updating server...")
        update_doccu_server()
        print("Updated!")
    else:
        choice = None
        main()

if __name__ == "__main__":
    main()

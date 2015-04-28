_date = '20150425'
"""This is a command-line address-book program using to browse, add, modify, delete or search 
for your contacts such as friends, family and colleagues and their information 
such as email address and/or phone number. Details can stored for later retrieval."""

#entry = dict()
import pickle

def string_dict(strs,dics):
	text = strs.strip().split(',')
	dics['Name'] = text[0]
	dics['Number'] = text[1]
	dics['Email'] = text[2]
	dics['Group'] = text[3]


def add(filename):
	print("-----------------------Add an entry-------------------------")
	add_entry = input('Entry include name,phone number, email-address, group. split in ","\n****>')
	print(add_entry,file=filename)

#判断输入的数据是否为4项，否则报错，退出
#输入的数据还得按顺序名字，电话号码，邮件，分组


def browse(filename):
	print("----------------------The address book----------------------")
	for each_line in filename:
		print(each_line)


def delete(filename):
	temp1 = []
	flag = 0
	print("---------------------Delete an entry------------------------")
	delete_entry = input('Please input the name you want to delete.\n*****>')
	for each_line in filename:
		string_dict(each_line,entry)
		if entry['Name'] == delete_entry:
			print('Entry Deleted')
			flag = 1
		else:
			temp1.append(each_line)
	if flag == 0:
		print('Cannot find the entry')	
	filename.seek(0)
	#记得将文件指针指向文件头，并清空文件内容，
	filename.truncate()
	for t in temp1:
		print(t,file=filename,end='')



def modify(filename):
	temp2 = []
	flag = 0
	print("---------------------Modify an entry------------------------")
	modify_name = input('Please input the name you want to modify.\n*****>')
	modify_new = input('Please input the new information.\n*****>')+'\n'
	text = modify_new.strip().split(',')
	for each_line in filename:
		string_dict(each_line,entry)
		if entry['Name'] == modify_name:
			temp2.append(modify_new)
			print('Entry Modified')
			flag = 1
		else:
			temp2.append(each_line)
	if flag ==0:
		print('Cannot find the entry')
	filename.seek(0)
	for t in temp2:
		print(t,file=filename,end='')


def search(filename):
	flag = 0
	print("---------------------Search an entry------------------------")
	search_entry = input('Please input the name you want to search.\n*****>')
	for each_line in filename:
		string_dict(each_line,entry)
		if entry['Name']== search_entry:
			print(each_line,end='')
			flag = 1
	if flag == 0:
		print('Cannot find the entry')


	

print('''--------------------------------------------------------------------
This is a address-book program, you can choose the following instruct
  a for add
  b for browse
  d for delete
  m for modify
  s for search
  q for quit
the address-book include name, phone number, email-address, group''')
choice = input('choice****>')

try:
	while choice!='q':
		with open('abook.txt','a') as file_a, open('abook.txt','r') as file_b_s,open('abook.txt','r+') as file_d_m:		
			if choice == 'a':	
				add(file_a)
			elif choice == 'b':
				browse(file_b_s)
			elif choice == 'd':
				delete(file_d_m)
			elif choice == 'm':
				modify(file_d_m)
			elif choice == 's':
				search(file_b_s)
			else:
				print('Input error, please try again. :-)')	
			choice = input('***************choice****>')
		
except IOError as err1:
	print('i want to test22222222')
	print('File open error: ' + str(err1))























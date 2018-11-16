#coding=utf-8
import subprocess
import os
import tkinter.messagebox as tm

###
# Python checker and Package installer
output = subprocess.check_output("python --version", shell=True)
if "Python" not in str(output): 
	tm.showerror(title="Error",
                 message="Python 未安裝或安裝失敗 請重新安裝")
else:
	os.system("pip install selenium")
	os.system("pip install requests")
	os.system("pip install pyinstaller")
	os.system("pip install selenium-requests")
	
import tkinter as tk
from tkinter import ttk
import traceback
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import webbrowser
import re
import codecs
import seleniumrequests

###
# Main GUInterface
root=tk.Tk()
root.title("懶人打卡 讓你青春不卡卡")
root.maxsize(1000,600)
root.geometry("500x550")
root.configure(background='gray')
### Another paramteres
# root.resizable(0, 0) #Don't allow resizing in the x or y direction
# root.pack(fill="both", expand=True)
# root.pack()
# ================================================================ #

###
# Passing Exception to except block:
class EmptyError(Exception):
	pass
class LoginError(Exception):
	pass
class DriverError(Exception):
	pass

###
# CMD work for Punch
# No use in this program
# Improve the work with background work in future
def cmdPun():
	session = requests.Session()
	login_params1 = {'Ecom_User_ID':'KF05588','Ecom_Password':'77040828','option':'credential','target':'https://portal.nchu.edu.tw/portal'}
	result = session.post("https://nchu-am.nchu.edu.tw/nidp/idff/sso?sid=0",data=login_params1)

	ans = session.get("https://nchu-am.nchu.edu.tw/nidp/idff/sso?sid=0")
	ans = session.get("https://nchu-am.nchu.edu.tw/portal/login")

	login_params2 = {'j_username':'KF05588','j_password':'77040828'}
	result = session.post("https://nchu-am.nchu.edu.tw/portal/j_spring_security_check",data=login_params2)

	ans = session.get("https://nchu-am.nchu.edu.tw/PsnWeb/IndexTop.jsp?url=/PsnWeb/AbntPunch.jsp")

	login_params3 = {'txtLoginID':'KF05588','url':'/PsnWeb/AbntPunch.jsp','txtLoginPWD':'L123917704','button':'送出'}
	result = session.post("https://nchu-am.nchu.edu.tw/PsnWeb/abntlogin_chk.jsp",data=login_params3)

	ans = session.get("https://nchu-am.nchu.edu.tw/PsnWeb/AbntSystem.jsp?url=/PsnWeb/AbntPunch.jsp")
	ans = session.get("https://nchu-am.nchu.edu.tw/PsnWeb/AbntPunch.jsp")

	punch_params = {'v_empl':'KF05588','v_pass':'L123917704','v_punch':'1'}
	result = session.post("https://nchu-am.nchu.edu.tw/PsnWeb/AbntPunchE.jsp",data=punch_params)
	print("打卡完成 請檢查是否正確打上班卡")
	root.quit()

###
# Browser work for Punch
# UserID: Employee ID
# PassID: Self-defined password
# pathID: Chrome-Driver location path
def work():
	try:
		user = account.get()
		pass_v = password.get()
		path = chromePath.get()
		if (user == '') or (pass_v == ''):
			raise EmptyError # define with class and jump to except block
		elif (path == ''):
			raise DriverError
		browser = webdriver.Chrome(path)
		browser.get('https://nchu-am.nchu.edu.tw/nidp/idff/sso?id=15&sid=1&option=credential&sid=1')
		time.sleep(1) # Time for browser loading
		userID = browser.find_element_by_xpath(".//*[@id='textfield']")
		passID = browser.find_element_by_xpath(".//*[@id='textfield2']")
		userID.send_keys(user)
		passID.send_keys(pass_v)
		browser.find_element_by_link_text('登入').click()
		time.sleep(1) # Time for browser loading
		browser.get('https://portal.nchu.edu.tw/portal/')
		pattern = "系統公告及相關資訊"
		if pattern in str(browser.page_source):
			print("<Log> Login Success")
		else:
			raise LoginError
			return # function return : program terminated
		
		### No-use in this function
		# requests.Session() : keep session with per-request
		#session = requests.Session()
		# result = session.get("https://psf2.nchu.edu.tw/PsnWeb/AbntSystem.jsp?url=/PsnWeb/AbntPunch.jsp")

		browser.get('https://psf2.nchu.edu.tw/PsnWeb/AbntSystem.jsp?url=/PsnWeb/AbntPunch.jsp')
		browser.find_element_by_link_text('線上簽到退').click()
		###
		# 這邊卡超久 一直沒注意到form被包在frame裡面 結果一直找不到input type跟value 
		# 是剛好巧合吧?
		# switch 之後才能找到表單裡的input 繼而submit表單做打卡
		browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
		browser.find_element_by_name('v_punch').submit()
		
		###
		# 從這一大串就知道我挖了多久的坑 才找到原來是在frame裡面 傻眼=3=
		# 為此留下此坑的紀錄 感謝我的時間小弟 犧牲了好多你才有今天的打卡程式
		#punch_params = {'v_empl':'KF05588','v_pass':'L123917704','v_punch':'2'}
		#result = session.post("https://nchu-am.nchu.edu.tw/PsnWeb/AbntPunchE.jsp",data=punch_params)
		#print(result)
		# browser.find_element_by_xpath("//input[@type='submit' and @value=' 刷 卡  ']").click()
		# browser.find_element_by_link_text('刷 卡').click()
		# browser.find_element_by_name('v_punch').submit()
		# chromedriv = seleniumrequests.Chrome()
		# time.sleep(2)
		# response = chromedriv.request('POST', 'https://nchu-am.nchu.edu.tw/PsnWeb/AbntPunchE.jsp', data={'v_empl':'KF05588','v_pass':'L123917704','v_punch':'2'})
		# print(response)

		tm.showinfo(title="Info",
                 message="刷卡完畢!",
                 )
# End of Program unit test
		time.sleep(2)
	except EmptyError: # Pass received
		tm.showerror(title="Error",
                 message="請正確輸入帳號密碼")
	except DriverError:
		tm.showerror(title="Error",
                 message="請填入Chrome Driver位置\n如需協助請呼叫電話旁邊那位")
	except LoginError:
		tm.showerror(title="Error",
                 message="登入失敗 請重新輸入帳號密碼並重試")
	except:
		tm.showerror(title="Error",
                 message="Unknown error has occurred",
                 detail=traceback.format_exc())
	finally:
		browser.quit()

###
# button function (WriteFile & CloseRoot)
def cmdButton():
	source_code ='''#coding=utf-8
import tkinter as tk
from tkinter import ttk
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import webbrowser
import re
import codecs
import seleniumrequests
import subprocess
import os
import tkinter.messagebox as tm

class EmptyError(Exception):
	pass
class LoginError(Exception):
	pass
class DriverError(Exception):
	pass

with open('Account.log', 'r') as user:
	account = user.read().split(',')
	userID = account[0]
	passID = account[1]
	pathID = account[2]
try:
	# Version 2 : add timer to control Punch timing and not repeat the same time 
	# Author: PPPy
	buffer = random.randint(30,180)
	time.sleep(buffer)
	user = userID
	pass_v = passID
	path = pathID
	if (user == '') or (pass_v == ''):
		raise EmptyError # define with class and jump to except block
	elif (path == ''):
		raise DriverError
	browser = webdriver.Chrome(path)
	browser.get('https://nchu-am.nchu.edu.tw/nidp/idff/sso?id=15&sid=1&option=credential&sid=1')
	time.sleep(1) # Time for browser loading
	userID = browser.find_element_by_xpath(".//*[@id='textfield']")
	passID = browser.find_element_by_xpath(".//*[@id='textfield2']")
	userID.send_keys(user)
	passID.send_keys(pass_v)
	browser.find_element_by_link_text('登入').click()
	time.sleep(1) # Time for browser loading
	browser.get('https://portal.nchu.edu.tw/portal/')
	pattern = "系統公告及相關資訊"
	if pattern in str(browser.page_source):
		print("<Log> Login Success")
	else:
		raise LoginError

	browser.get('https://psf2.nchu.edu.tw/PsnWeb/AbntSystem.jsp?url=/PsnWeb/AbntPunch.jsp')
	browser.find_element_by_link_text('線上簽到退').click()

	browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
	browser.find_element_by_name('v_punch').submit()
		
	tm.showinfo(title="Info",
                message="刷卡完畢!",
                )
# End of Program unit test
	time.sleep(2)
except EmptyError: # Pass received
	tm.showerror(title="Error",message="帳號密碼讀取失敗\\n請重新開啟奇軒Go設定")
except DriverError:
	tm.showerror(title="Error",message="Chrome Drive讀取失敗\\n請重新開啟奇軒Go設定")
except LoginError:
	tm.showerror(title="Error",message="登入失敗\\n請重新開啟奇軒Go設定帳號密碼")
except:
	tm.showerror(title="Error",message="Unknown error has occurred",detail=traceback.format_exc())
finally:
	browser.quit()
'''
	resultPath = ''
	chromePathStr = chromePath.get().split('\\')
	for x in range(0,len(chromePathStr)):
		if (x==(len(chromePathStr)-1)):
			resultPath = resultPath + str(chromePathStr[x])
		else:
			resultPath = resultPath + str(chromePathStr[x]) + '\\\\'
	# write to file
	userInfo = account.get()+','+password.get()+','+resultPath

	###
	# WriteFile has two method
	# in this case : UTF-8 decode error 
	# solution : import codecs and convert to utf-8 encoding
	## Method 1 : basic
	# with open('Punch.py', 'w+') as source:
	# 	source.write(source_code)
	## Method 2 : advanced for encoding
	file = codecs.open("Punch.py", "w+", "utf-8")
	file.write(source_code)
	file.close()
	print("指令碼寫檔完成")

	with open('Account.log', 'w+') as user:
		user.write(userInfo)
		print("程式記錄檔完成")
	###
	# Compile Punch.py -> executable in dist directory
	# os.system("pyinstaller -F .\\Punch.py")
	tm.showinfo(title="Info",
                 message="指令碼產生完畢!\n請依照指示新增至Windows排程",
                 )
	webbrowser.open_new("http://www.py.idv.tw/files/Windows.html")
	root.quit()

# Hyperlink with event callback
def callback(event):
	webbrowser.open_new(event.widget.cget("text"))

### Main GUI widget
# Powered Banner
label2=tk.Label(master=root, text="找飯店 Trivago\n找懶人 奇軒Go\n\n中興大學打卡專用\n", bg='gray', fg='cyan')
label2.config(font=("標楷體", 15))
label2.pack()
# UserID
label1=tk.Label(master=root, text="登入帳號:", bg='gray')
label1.config(font=("", 12))
label1.pack()
account = tk.StringVar()
Enput1=tk.Entry(master=root, textvariable=account)
Enput1.config(width=25)
Enput1.pack()
# PassID
label2=tk.Label(master=root, text="登入密碼:", bg='gray')
label2.config(font=("", 12))
label2.pack()
password = tk.StringVar()
Enput2=tk.Entry(master=root, show="*", textvariable=password)
Enput2.config(width=25)
Enput2.pack()
# Path
label9=tk.Label(master=root, text="Chrome Driver 路徑:", bg='gray')
label9.config(font=("", 12))
label9.pack()
chromePath = tk.StringVar()
Enput3=tk.Entry(master=root, textvariable=chromePath)
Enput3.config(width=25)
Enput3.pack()
###
# Factory Mode
# this block take with callback event function
label5=tk.Label(master=root, text="\n\n***** 套件安裝需求 *****", bg='gray', fg='black')
label5.config(font=("", 13))
label5.pack()
label5=tk.Label(master=root, text=r"https://www.python.org/downloads/", bg='gray', fg='blue')
label5.config(font=("", 13))
label5.pack()
label5.bind("<Button-1>", callback)
label5=tk.Label(master=root, text=r"http://chromedriver.chromium.org/downloads", bg='gray', fg='blue')
label5.config(font=("", 13))
label5.pack()
label5.bind("<Button-1>", callback)
#
labelq=tk.Label(master=root, text="\n", bg='gray')
labelq.pack()
###
# Submit Checker
button1=ttk.Button(master=root, text="測試登入與打卡", command=work)
button1.pack()
###
# Packer implementation
button2=ttk.Button(master=root, text="產生打卡執行檔", command=cmdButton)
button2.pack()
# User document
label3=tk.Label(master=root, text="===== 使用前請先詳閱說明書 =====\n\n帳號: 員工編號\n密碼: (同登入口密碼)\n先經過\"測試登入與打卡\"成功後在按下產生執行檔\n並將執行檔掛載進Windows排程器\n有使用問題請洽電話旁邊那位", bg='gray', fg='yellow')
label3.config(font=("", 13))
label3.pack()
###
# Banner
# \n\n\t\tPowered by 奇軒
label4=tk.Label(master=root, text="\n\n\t\t\tVersion 1.0 -- Powered by 奇軒", bg='gray', fg='pink')
label4.config(font=("標楷體", 13))
label4.pack()
###
# Window Show
root.mainloop()

###
# [Entry] Main Function
# if __name__ == '__main__':
	###
	# get output from os_system(shell)
	# output = subprocess.check_output("python --version", shell=True)
	# if "Python" not in str(output): 
	# 	tm.showerror(title="Error",
 #                 message="Python 未安裝或安裝失敗 請重新安裝")
	# else:
	# 	os.system("pip install selenium")
	# 	os.system("pip install requests")
	# 	os.system("pip install pyinstaller")
	# 	os.system("pyinstaller -F .\\Punch.py")
	# tm.showinfo(title="Info",
 #                 message="執行檔產生完畢!\n請依照指示新增至Windows排程",
 #                 )
	# root.quit()

### MessageDialog補充
#,detail=traceback.format_exc()

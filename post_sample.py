import requests
import time

# Customized Headers from Web traffic packet
##
### Value fixed by empty, need replace with sending parameters
headers = {
	'Host':'',
	'Connection':'close',
	'Content-Length':'',
	'Cache-Control':'max-age=0',
	'Origin':'',
	'Upgrade-Insecure-Requests':'1',
	'Content-Type':'application/x-www-form-urlencoded',
	'User-Agent':'',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Referer':'',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.9',
	'Cookie':''
}

#### fixed Keys and values

# post_parm = {
# 	'BASE_MANAGER':'',
# 	'OFF_PUN':'0',
# 	'Pun_Date':'1070815',
# 	'Pun_Hour':'08',
# 	'Pun_Min':'00',
# 	'Apply':'1',
# 	'Reason':'',
# 	'Reason':'9',
# 	'PUN_ATTACH':''
# }

#### Loop for send request with parameters & headers
while True:
	for x in range(3,8):
		dater = '107090' + str(x)
		post_parm = {
			'BASE_MANAGER':'',
			'OFF_PUN':'0',
			'Pun_Date':'1070815',
			'Pun_Hour':'08',
			'Pun_Min':'00',
			'Apply':'1',
			'Reason':'',
			'Reason':'9',
			'PUN_ATTACH':''
		}
		r = requests.post('http://www.py.idv.tw', headers= headers, data = post_parm)
		print(r.status_code)
		time.sleep(1)

	for x in range(3,8):
		dater = '107090' + str(x)
		post_parm = {
			'BASE_MANAGER':'',
			'OFF_PUN':'0',
			'Pun_Date':'1070815',
			'Pun_Hour':'08',
			'Pun_Min':'00',
			'Apply':'2', # to identify user "go" or "leave"
			'Reason':'',
			'Reason':'9',
			'PUN_ATTACH':''
		}
		r = requests.post('http://www.py.idv.tw', headers= headers, data = post_parm)
		print(r.status_code)
		time.sleep(1)
	if dater == '1070907':
		break
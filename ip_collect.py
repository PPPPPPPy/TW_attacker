import re

with open("plain text - preprocesshurricane.txt",'a') as outfile ,open('0723-27.txt', 'r') as infile:
	outfile.seek(0)
	outfile.flush()
        for tweet in infile.readlines():
			temp=tweet.split(',')
			y=str(temp[0])
			print(y+'\n')
			#x= re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", y)
			#x = re.match("</[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/>", y)
			#[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$
			#print x
			outfile.write(y+'\n')
			#outfile.write('\n')

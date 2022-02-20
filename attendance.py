from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from mss import mss
import os
import time
import datetime
import getpass

petrol = 'https://lms.iitjammu.ac.in/course/view.php?id=272'
eco = 'https://lms.iitjammu.ac.in/course/view.php?id=329'
ml = 'https://lms.iitjammu.ac.in/course/view.php?id=281'
biosensors = 'https://lms.iitjammu.ac.in/course/view.php?id=235'
reactors = 'https://lms.iitjammu.ac.in/course/view.php?id=268'
daa = 'https://lms.iitjammu.ac.in/course/view.php?id=285'
empty = True

l = [[petrol, empty, eco, ml, biosensors], [reactors, petrol, empty, biosensors], [daa, reactors, empty, petrol, empty, biosensors], [eco, daa, reactors, empty, ml], [empty, eco, daa, ml, reactors]]
t = [[90, 160, 90, 90, 2], [90, 90, 250, 1.5], [90, 90, 60, 90, 90, ], [90, 90, 60, 1.5], [90, 150, 90, 90, 1.5]]

weekday = datetime.datetime.today().weekday()

if(weekday == 6 or weekday==5):
	print("No classes today, have some rest xD")
	time.sleep(4)
else:
	now = datetime.datetime.now()
	start = datetime.datetime.combine(datetime.date.today(), datetime.time(9, 2))
	diff = (start-now).total_seconds()/60.0
	cnt = 0
	for i in range (0, len(t[weekday])):
		if(diff > 0):
			break
		elif(diff > -80):
			t[weekday][i] = t[weekday][i] + diff
			diff = 0
			break
		else:
			diff = diff + t[weekday][i]
			cnt = cnt + 1 
	init_sleep = diff
	print("Sleeping for initial ", init_sleep, " minutes")
	time.sleep(60*init_sleep)

	for i in range (0, len(l[weekday])):
		if(cnt != 0):
			cnt = cnt - 1
			continue
		chrome_options = Options()
		chrome_options.add_argument("--disable-infobars")
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument("user-data-dir=C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Google\\Chrome\\User Data")
		driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
		if(l[weekday][i]!=True):
			driver.get(l[weekday][i])
			if("https://lms.iitjammu.ac.in/login/index.php" in driver.current_url):
				driver.find_element_by_xpath('//*[@id="username"]').send_keys(os.environ.get("LMS_USER"))
				time.sleep(0.2)
				driver.find_element_by_xpath('//*[@id="password"]').send_keys(os.environ.get("LMS_PASS"))
				time.sleep(0.2)
				driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
			driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/section[2]/aside/section/div/div/div[1]/p/a').click()
		time.sleep(0.4*t[weekday][i])
		with mss() as sct:
			sct.shot(output="class"+str(i+1)+".png")
		print("Screenshot saved.....")
		time.sleep(0.1*t[weekday][i])
		print("Exiting Chrome.....")
		driver.quit()
		print("Sleeping for ",t[weekday][i]//60, " hour/s and ", t[weekday][i]%60," minutes")
		time.sleep(59.5*t[weekday][i])
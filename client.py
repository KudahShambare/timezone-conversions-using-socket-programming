##Please read readme.md before you run the code
#4075731

import socket
import pandas
import json
import random
from faker import Faker
from datetime import datetime


clientSocket = socket.socket()

#connect to server

clientSocket.connect(("localhost",20232))

#import data from the excel file and convert it to json

excelData = pandas.read_excel("data.xlsx").to_json(orient='records');

#convert the json data to python list 

excelData=json.loads(excelData)

#remove the headings row

excelData.pop(0)

#single student data
counter=0;
for student in excelData:
	if(student["Student No."]!="4075731"):
		counter+=1
	
	else:
		myData=excelData[counter]

#PUT ALL CITIES TOGETHER
myCities=[]

myCities.append(myData["Cities (20 in a row)"])

unNamedRange = range(3,22)

for num in unNamedRange:
	myCities.append(myData["Unnamed: "+str(num)])

#10 Additional Cities

additionalCities = ["Harare","Nairobi","New York","Florida","Helsinki","Tokyo","Beijing","London","Cairo","Madrid"]	

for add_city in additionalCities:
	myCities.append(add_city)

####################################################################################################

#create TXT to store schedules

file = open("schedules.txt","w")


for city in myCities:

	#meeting platforms

	platforms = ["Zoom","Google Meets","Skype","Microsoft Teams"]
	topics = ["Cloud Computing","DevOps","Socket Programming","Computer Networks","Cyber Security","IoT"]
	randomTopic = random.choice(topics)
	randomPlatform = random.choice(platforms)

	#create schedules using 30 city datas

	# Generate fake dates 

	fake = Faker()
	startDate = datetime.strptime("2023/03/07","%Y/%m/%d")
	endDate = datetime.strptime("2023/12/31","%Y/%m/%d")
	randomDate = fake.date_between(startDate,endDate)

	# Generate random time

	hourRange = list(range(0,23))
	minuteRange = list(range(0,59))

	randomHour = random.choice(hourRange)

	if (randomHour<10):
		randomHour = "0"+str(randomHour)

	randomMinute = random.choice(minuteRange)

	if(randomMinute<10):
		randomMinute = "0"+str(randomMinute)

	randomTime = str(randomHour) + ":" + str(randomMinute)
			
	schedule = str(randomDate)+ "," + city + "," + randomTime + "," + randomTopic + "," + randomPlatform

	file.write(schedule+"   ####   ")
#close the file
file.close()

##################################################################################################################

#read the created file and send the date and time to South African Time

#create a string that is gouing to combine all the file lines into 1 string seperated by a delimeter ####
readFile = open("schedules.txt","r")
lines = readFile.readlines()
readFile.close()

toSendToServer= "".join(lines)


clientSocket.send(bytes(toSendToServer,"utf-8"))


#Data from server

fromServer = clientSocket.recv(1024).decode()

print(fromServer)




	



	  
	
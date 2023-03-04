##Please read readme.md before you run the code
#4075731

# import libraries

import requests
import socket
from datetime import *



serverSocket = socket.socket()
print('Server ready to connect with clients')

# port number and IP binding

port = 20232

serverSocket.bind(('localhost', port))

# max number of clients to connect to this server

serverSocket.listen(4)

#/**********************************************************************************************************/

# API that matches a city name to its timezone
apiUrl = 'https://fair-blue-scorpion-hat.cyclic.app/'

	 # Timezones API

apiKey = '368db72f727b4a1895af3250005b8895'


########################################################################################################

# Prof Bagula's timezone

bagulaCity = 'Cape Town'
capeZone = apiUrl + bagulaCity
bagulaTimeZone = requests.get(capeZone)
bagulaTimeZone = bagulaTimeZone.text

# fetch Prof Bagula's TIMEZONE Details

bagulaZoneDetails = requests.get('https://api.ipgeolocation.io/timezone?apiKey=' + apiKey + '&tz=' + bagulaTimeZone)
bagulaZoneDetails = bagulaZoneDetails.json()

bagulaTimeOffset = bagulaZoneDetails['timezone_offset']


# time difference object

def timeZoneDifferences(city):

	cityZone = requests.get(apiUrl + city)
	cityZone = cityZone.text
	cityZoneDetails = requests.get('https://api.ipgeolocation.io/timezone?apiKey=' + apiKey + '&tz=' + cityZone)
	cityZoneDetails = cityZoneDetails.json()

	if 'timezone_offset' in cityZoneDetails:

		cityTimeOffset = cityZoneDetails['timezone_offset']
		timeDiff = bagulaTimeOffset - cityTimeOffset
		cityObject = {'City': city, 'Difference': timeDiff}

#Account for City errora in the excel file
	else:
		cityObject = {'City':city,'Difference':9999}


	return cityObject	
	

while True:

	clientSocket, clientAddress = serverSocket.accept()

	print("Server connected with client: ",clientAddress)

	#read data from client

	clientData = clientSocket.recv(4096).decode()
	clientList = clientData.split("   ####   ")
	clientList.pop()

	#file to send to client
	convertedTimes = open("converted.txt","w")

	#iterate clientList to convert  times  to SAST
	for city in clientList:
		cityArr = city.split(",")
		cityName = cityArr[1]
		meetingDate = cityArr[0]
		meetingTime = cityArr[2]

		#replace - with / in date for manipulation purposes
		meetingDateArr=meetingDate.split("-")
		meetingDate="/".join(meetingDateArr)

		dateTimeString = meetingDate + " " + meetingTime

		cityDateAndTime = datetime.strptime(dateTimeString,"%Y/%m/%d %H:%M")
		

		#time differences
		cityTimeDiff = timeZoneDifferences(cityName)
		
		#work with correct cities only 
		
		if (cityTimeDiff["Difference"] != 9999):
			sastDateAndTime = cityDateAndTime + timedelta(hours=cityTimeDiff["Difference"])
			sastDateAndTime = str(sastDateAndTime)
			sastDateAndTimeArr = sastDateAndTime.split(" ")
			
			cityArr[0] = sastDateAndTimeArr[0]
			cityArr[2]= sastDateAndTimeArr[1]

		# cities with errors

		else:
			cityArr.append("The time was not converted to SAST because of an error in the input.")

		cityArr= " ".join(cityArr)
		
		convertedTimes.write(cityArr+"\n")

	convertedTimes.close()


	message = "All the time conversions to SAST have been completed. Please check the output file named <<converted.txt>> for the results. The results are in the same order as the input from the <<schedules.txt>>"

	clientSocket.send(bytes(message,"utf-8"))

	clientSocket.close()








import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import ast


headers = {
    # Request headers
    'atr-environment-id': 'atrprod02us',
    'atr-partner-id': '0842d87e-c606-477d-9f01-271d4bded17e',
    'atr-request-source': 'benjamin',
    'atr-subscription-key': 'ec6e0db6e4ea42dab1e9ea347fc1c104',
}


exportData={
    "result": [],
    "count": 0
}
siteID = "810"
#startDateString = "2018-09-25T01:00:00"
#endDateString = "2018-09-25T02:50:00"
requestType = "GET"
dateWindowStrings = ["2017-09-01T00:01:00Z&endDate=2017-09-01T23:59:00",
					"2017-09-02T00:01:00Z&endDate=2017-09-02T23:59:00", 
                    "2017-09-03T00:01:00Z&endDate=2017-09-03T23:59:00",
					"2017-09-04T00:01:00Z&endDate=2017-09-04T23:59:00", 
                    "2017-09-05T00:01:00Z&endDate=2017-09-05T23:59:00",
					"2017-09-06T00:01:00Z&endDate=2017-09-06T23:59:00", 
                    "2017-09-07T00:01:00Z&endDate=2017-09-07T23:59:00",
					"2017-09-08T00:01:00Z&endDate=2017-09-08T23:59:00", 
                    "2017-09-09T00:01:00Z&endDate=2017-09-09T23:59:00",
					"2017-09-10T00:01:00Z&endDate=2017-09-10T23:59:00", 
                    "2017-09-11T00:01:00Z&endDate=2017-09-11T23:59:00",
					"2017-09-12T00:01:00Z&endDate=2017-09-12T23:59:00", 
                    "2017-09-13T00:01:00Z&endDate=2017-09-13T23:59:00",
					"2017-09-14T00:01:00Z&endDate=2017-09-14T23:59:00", 
                    "2017-09-15T00:01:00Z&endDate=2017-09-15T23:59:00",
					"2017-09-16T00:01:00Z&endDate=2017-09-16T23:59:00", 
                    "2017-09-17T00:01:00Z&endDate=2017-09-17T23:59:00",
					"2017-09-18T00:01:00Z&endDate=2017-09-18T23:59:00",
					"2017-09-19T00:01:00Z&endDate=2017-09-19T23:59:00",
					"2017-09-20T00:01:00Z&endDate=2017-09-20T23:59:00",
					"2017-09-21T00:01:00Z&endDate=2017-09-21T23:59:00"]#,
					#"2018-09-22T00:01:00Z&endDate=2018-09-22T23:59:00",
					#"2018-09-23T00:01:00Z&endDate=2018-09-238T23:59:00",
					#"2018-09-24T00:01:00Z&endDate=2018-09-24T23:59:00",
                    #"2018-09-25T00:01:00Z&endDate=2018-09-25T23:59:00", 
                    #"2018-09-26T00:01:00Z&endDate=2018-09-26T23:59:00",
					#"2018-09-27T00:01:00Z&endDate=2018-09-27T23:59:00",
					#"2018-09-28T00:01:00Z&endDate=2018-09-28T23:59:00", 
                    #"2018-09-29T00:01:00Z&endDate=2018-09-29T23:59:00",
					#"2018-09-30T00:01:00Z&endDate=2018-09-30T23:59:00"
                    #]

for t in dateWindowStrings:
	requestString = "/api/v2/insights/positions/site-id/" + siteID + "?startDate=" + t + "Z&"
	#requestString = "/api/v2/insights/positions/site-id/810?startDate=2018-09-25T01:00:00Z&endDate=2018-09-25T02:00:00Z&"
	#print(type(requestString))

	try:
		conn = http.client.HTTPSConnection('api.us.atrius-iot.io')
		#conn.request("GET", "/api/v2/insights/positions/site-id/810?startDate=2018-09-25T01:00:00Z&endDate=2018-09-25T02:50:00Z&", "{body}", headers)
		conn.request(requestType, requestString, "{body}", headers)
		response = conn.getresponse()
		data = response.read() #bytes object
		print("the window " + t + " is done")
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
		
	dataString = str(data)[2:-1]	#convert it to a string and remove the b' to make it formattable to json
	
	#print(dataString)
	#locations = dataString
	#print(locations)
	#locationFile=open("testfile.json","w+")
	#locationFile.write(locations)
	#locationFile.close()

	locationJSON = json.loads(dataString)
	exportData["result"].append(locationJSON["result"])

#print(exportData)
stringToFile = str(exportData).replace("\'", "\"")# turn single quotes to double quotes so the json will be valid
locationFile=open("T0862August2017.json","w+")
locationFile.write(stringToFile)
locationFile.close()
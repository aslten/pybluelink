#!/usr/bin/python3

import os
import subprocess
import time

CONNECTION_TIMEOUT = 20

class bluelinkConnection():
    def __init__(self, user, password, pin, carVIN, path):
        self.user = user
        self.pw = password
        self.pin = pin
        self.carVIN = carVIN
        self.path = path
            
    def getStatus(self):
        print('Fetching bluelink status information')
        response = self.bluelinkCommunication('status.js')
 
        carStatus = {'validData': False, 'status': {}} 

        if response != None:
            carStatus['status'] = self.parseResponse(response)
            if carStatus['status'] != {}:
                carStatus['validData'] = True
                
        return carStatus

    def parseResponse(self, theResponse):
        statusDict = {}
        statusDict['battery12V'] = self.getItem(theResponse, 'batSoc',',', 'floatType')
        statusDict['soc'] = self.getItem(theResponse, 'batteryStatus',',', 'floatType')
        statusDict['locked'] = self.getItem(theResponse, 'doorLock',',', 'boolType')
        statusDict['airCtrlOn'] = self.getItem(theResponse, 'airCtrlOn',',', 'boolType')
        return statusDict
        
        
    def getItem(self, response, theItem, endCharacter, itemType):
        tempString = response.split(theItem+':')
        if len(tempString) > 1:
            tempString2 = tempString[1].split(endCharacter)

            if len(tempString2) >1:
                if itemType == 'floatType':
                    return float(tempString2[0].strip())
                elif itemType == 'boolType':
                    if tempString2[0].strip() == 'true':
                        return True
                    else:
                        return False
                else:
                    return tempString2[0]
            else:
                return None
        else:
            return None

    def startCharge(self):
        self.bluelinkCommunication('startCharge.js')
    def stopCharge(self):
        self.bluelinkCommunication('stopCharge.js')

    def startPreheatWithoutDefrost(self):
        self.bluelinkCommunication('startPreheat.js')

    def startPreheatDefrost(self):
        self.bluelinkCommunication('startPreheatDefrost.js')

    def startPrecool(self):
        self.bluelinkCommunication('startPrecool.js')

    def stopPreheat(self):
        self.bluelinkCommunication('stopPreheat.js')

    def bluelinkCommunication(self, command):
        print("Connection over bluelink")
        # Perform 3 tries before giving up
        count = 0
        theCommand = ['node', (self.path + command), self.user, self.pw, self.pin, self.carVIN]
        
        success = False
        response = None

        #return response
        
        for count in range(3):
            try:
                rawResponse = subprocess.run(theCommand, capture_output=True, timeout=CONNECTION_TIMEOUT)
                print(rawResponse)
            except:
                print('Error when trying to read Bluelink')
            else:
                response = str(rawResponse)

                if response.find('UnhandledPromiseRejectionWarning') != -1:
                    print('Bluelink: Error when trying to read Bluelink: UnhandledPromiseRejectionWarning')
                    response = None
                elif len(response) == 0:
                    print('Bluelink: Received empty status')
                    response = None
                else:
                    success = True
                    break
            if count < 3 and success == False:
                time.sleep(10)
        return response
        

if __name__ == '__main__':
    #bl.startCharge()
    print(bl.getStatus())
    #bl.startPreheatWithoutDefrost()
    #bl.stopPreheat()


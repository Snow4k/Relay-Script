# Author Devin Buckles
# Company - Security Central Protection
# Version 1.0

from flask import Flask, make_response
from flask_restful import Resource, Api
import yaml
import os
import time
import serial


app = Flask(__name__)
api = Api(app)
#Declare these variables for later
host = str()
port = int()
version = float()
inputs = dict()

#This pulls the latest release from github and replaces it in whatever directery its in.  
def checkForUpdates():
    pass

#Code for the endpoints in question 
class Endpoints():
    class ImmixReading(Resource):
        def get(self):
            return 200


    class RelayTrigger(Resource):
        def post(self, RelayNumber, Command):
            RelayNumber = int(RelayNumber)  
            Command = str(Command)

            try:
                #Grab the relay details accordingly
                relay = serial.Serial(
                    str(inputs[RelayNumber]['Port']), 
                    int(inputs[RelayNumber]['Baud']), 
                    int(inputs[RelayNumber]['DataBits']), 
                    serial.PARITY_NONE, 
                    float(inputs[RelayNumber]['Stop'])
                    )
                

                if Command == "on":
                    relay.write(bytes(inputs[RelayNumber]['OnCommand'], "ascii"))
                elif Command == "off":
                    relay.write(bytes(inputs[RelayNumber]['OffCommand'], "ascii"))

                resp = make_response("Success", 200)
                return resp
            except IndexError:
                print("That Input number is not valid")
                resp = make_response("Input Not Found", 401)
                return resp
            except:
                resp = make_response("Internal Error", 500)
                return resp
      
#Add API Endpoints. More can be added later
api.add_resource(Endpoints.ImmixReading, '/')
api.add_resource(Endpoints.RelayTrigger, '/relay/<RelayNumber>/<Command>')

def main():

    #Check for updates
    checkForUpdates()

    #Parse configertion File
    with open('config.yml', 'r') as file:
        setting = yaml.safe_load(file)
    
        #Parse the main settings
        host = setting['host']
        port = setting['port']
        version = setting['version']
        print(f"This is version: {version}")
      
        #Parse each input
        for inputNum in setting['serials']:
            inputs[inputNum] = setting['serials'][inputNum]
                   
    #Run API 
    app.run(debug=True, port=port, host=host)


#Run main above
main()
import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as sqldb
import requests


def connectToSQLDB():
    return sqldb.connect(user='root', password='password', database='team22demand', port=6022)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '1.0'

    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    def do_POST(self):
        path = self.path
        print(path)
        responseDict = {'Success': False, 'Vehicle Info': None}

        if '/orderHandler' in path:
            dictionary = self.getPOSTBody()
            # To access a specific key from the dictionary:
            print(dictionary)
            username = dictionary['username']
            sType = dictionary['serviceType']
            destination = dictionary['destination']

            print(username)
            print(sType)
            print(destination)

            sqlConnection = connectToSQLDB()
            cursor = sqlConnection.cursor()
            cursor.execute('SELECT custid FROM customers WHERE username = %s', (username,))
            custid = cursor.fetchone()[0]
            print(custid)
            if custid is not None:
                print(custid)
                cursor.execute('INSERT INTO orders (custid, type, destination) VALUES (%s, %s, %s)',
                               (custid, sType, destination))
                sqlConnection.commit()

                # Make API call to vehicleRequest, POSTing our order dictionary. Our API will need partial order
                # dictionary information.
                # response = requests.post('https://supply.team22.softwareengineeringii.com/vehicleRequest', dictionary)
                # status = response.status_code
                status = 200
                # if status == 200:
                #     responseDict['Vehicle Info'] = response.json()
            else:
                status = 400
        else:
            status = 404

        print(status)
        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseDict)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)

    def do_GET(self):
        print("got")
        self.send_response(200)
        self.end_headers()
        self.wfile.write("response body \r\n")

def main():
    # Define the port your server will run on:
    # Using 4001 as an example! Yours may run on another port!
    # Consult with Devops Coordinator to find out which port
    # your server should be running on!
    port = 4003
    # Create an http server using the class and port you defined
    httpServer = http.server.HTTPServer(('', port), SimpleHTTPRequestHandler)
    print("Running on port", port)
    # this next call is blocking! So consult with Devops Coordinator for
    # instructions on how to run without blocking other commands frombeing
    # executed in your terminal!
    httpServer.serve_forever()

if __name__ == "__main__":
    main()
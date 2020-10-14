# pip3 install -r requirements.txt
# dmesg | grep tty (lookout for ttyUSB0)
# mv env.example .env

import serial
import time

# MySql
import mysql.connector

# Get Host Name
import socket


def connectDB:
	try:
     	connection = None
     	if(os.getenv("db_password")):
            connection = mysql.connector.connect(
            user=os.getenv("db_user"),
            host=os.getenv("db_ip"),
            database=os.getenv("db_database"),
            charset='utf8',
            port='3306')
        else:
            connection = mysql.connector.connect(
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            host=os.getenv("db_ip"),
            database=os.getenv("db_database"),
            charset='utf8',
            port='3306')

deviceID = socket.gethostname()
z1baudrate = 9600
z1port = '/dev/ttyUSB0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2  # set read timeout
# print z1serial  # debug serial.
print (z1serial.is_open)  # True for opened
if (z1serial.is_open):
    connectDB()
    while True:
        size = z1serial.inWaiting()
        if size:
            data = z1serial.read(size)
            data = data.decode('utf-8')
            sql="INSERT INTO `raspi_listener` (`deviceID`, `garment_code`) VALUES ({}, {}, );".format(deviceID, data);
            #print(sql)
            mycursor = connection.cursor()
            mycursor.execute(sql)
            print (data)
        else:
            print ('no data')
        time.sleep(1)
else:
    print ('z1serial not open')
# z1serial.close()  # close z1serial if z1serial is open.





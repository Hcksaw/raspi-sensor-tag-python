from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
import time
import binascii
import os
import struct
from time import sleep
from datetime import datetime
import MySQLdb

def connectDevice(macAddress):
	device = btle.Peripheral(macAddress)
	return device

def connectService(device, sensorUUID):
	sensor = btle.UUID(sensorUUID)
	service = device.getServiceByUUID(sensor)
	return service

def getDataAccel(device):
	accelService = connectService(dev, "f000AA80-0451-4000-b000-000000000000")
	for ch in accelService.getCharacteristics():
		print str(ch)
	accelConfigUUID = "f000AA82-0451-4000-b000-000000000000"
	accelSensorConfig = accelService.getCharacteristics(accelConfigUUID)[0]
	accelSensorConfig.write(struct.pack("<H", 7 << 3))
	time.sleep(1)

	accelDataUUID = "f000AA81-0451-4000-b000-000000000000"
	accelData = accelService.getCharacteristics(accelDataUUID)[0]
	db = MySQLdb.connect("localhost", "hacksaw", "logfile12", "SensorData")
	curs=db.cursor() 

	while 1:
		val = accelData.read()
	 	print "accel raw value", struct.unpack("<hhhhhhhhh", val)[3:6]
		one = struct.unpack("<hhhhhhhhh", val)[3:4][0]
		two = struct.unpack("<hhhhhhhhh", val)[4:5][0]
		three = struct.unpack("<hhhhhhhhh", val)[5:6][0]
		
		try:
			curs.execute("INSERT INTO accelData values (%s, %s, %s, CURRENT_DATE(), NOW(), NULL, NULL)", (one, two, three))    		
			db.commit()
			print "record"
	 	time.sleep(1)



scanner = Scanner()
devices = scanner.scan(5.0)

sensors = []
for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if "SensorTag" in value:
            print "Sensor Found"
            sensors.append(dev.addr)
            print dev.addr

if len(sensors) > 0:
	print "conecting... to %s", sensors[0]
	# dev = btle.Peripheral(sensors[0])
	dev = connectDevice(sensors[0])
	print "Services.."
	for svc in dev.services:
		print str(svc)

	lightService = connectService(dev, "f000aa70-0451-4000-b000-000000000000")
	for ch in lightService.getCharacteristics():
		print str(ch)

	uuidConfig = btle.UUID("f000aa72-0451-4000-b000-000000000000")
	lightSensorConfig = lightService.getCharacteristics(uuidConfig)[0]

	lightSensorConfig.write(bytes("\x01"))

	time.sleep(1.0)

	uuidValue = btle.UUID("f000aa71-0451-4000-b000-000000000000")
	lightSensorValue = lightService.getCharacteristics(uuidValue)[0]

	getDataAccel(dev)

	# while 1:
	# 	val = lightSensorValue.read()
	# 	print "Light sensor raw value", binascii.b2a_hex(val)
	# 	time.sleep(1)

	

	# tempSensor = btle.UUID("f000aa00-0451-4000-b000-000000000000")
	# tempService = dev.getServiceByUUID(tempSensor)
	# for ch in tempService.getCharacteristics():
	# 	print str(ch)

	## batterySensor = btle.UUID("Battery Service")
	## batteryService = dev.getServiceByUUID(batterySensor)
	##for ch in batteryService.getCharacteristics():
	##    print str(ch)
else:
    print "No Sensor Found"

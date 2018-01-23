from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
import time
import binascii
import os
from time import sleep
from datetime import datetime

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
	dev = btle.Peripheral(sensors[0])

	print "Services.."
    for svc in dev.services:
        print str(svc)
	lightSensor = btle.UUID("f000aa70-0451-4000-b000-000000000000")
	lightService = dev.getServiceByUUID(lightSensor)
	for ch in lightService.getCharacteristics():
            print str(ch)

	uuidConfig = btle.UUID("f000aa72-0451-4000-b000-000000000000")
	lightSensorConfig = lightService.getCharacteristics(uuidConfig)[0]

	lightSensorConfig.write(bytes("\x01"))

	time.sleep(1.0)

	uuidValue = btle.UUID("f000aa71-0451-4000-b000-000000000000")
	lightSensorValue = lightService.getCharacteristics(uuidValue)[0]

	val = lightSensorValue.read()
	print "Light sensor raw value", binascii.b2a_hex(val)

	tempSensor = btle.UUID("f000aa00-0451-4000-b000-000000000000")
	tempService = dev.getServiceByUUID(tempSensor)
	for ch in tempService.getCharacteristics():
            print str(ch)

	## batterySensor = btle.UUID("Battery Service")
	## batteryService = dev.getServiceByUUID(batterySensor)
	##for ch in batteryService.getCharacteristics():
	##    print str(ch)
else:
    print "No Sensor Found"

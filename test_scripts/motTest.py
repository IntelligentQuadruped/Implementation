# testing the motors
import RPi.GPIO as GPIO
import time

def switchValue(thisValue):
	if thisValue == GPIO.HIGH:
		return GPIO.LOW
	if thisValue == GPIO.LOW:
		return GPIO.HIGH
	print("Error on value", str(thisValue))
	return " "

# Paramaters:
numCycles = 2
runDebug = False
debugCode = 'esd'

# Defining the pins
step = 14
direction = 15
enable = 17

# pin setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(step, GPIO.OUT)
GPIO.setup(direction, GPIO.OUT)
GPIO.setup(enable, GPIO.OUT)

print("Starting Test Now")

GPIO.output(enable,GPIO.LOW)
time.sleep(2)
direct = GPIO.LOW
count = 0
rotations = 0

switching = GPIO.LOW

if runDebug:
	if 'e' in debugCode.lower():
		print("Testing Enable")
		print("Setting Enable to High")
		GPIO.output(enable,GPIO.HIGH)
		time.sleep(10)
		print("Setting Enable to Low")
		GPIO.output(enable,GPIO.LOW)
		time.sleep(10)

	if 's' in debugCode.lower():
		print("Testing step")
		print("Setting Step to LOW")
		GPIO.output(step, GPIO.LOW)
		time.sleep(10)
		print("Setting Step to HIGH")
		GPIO.output(step, GPIO.HIGH)
		time.sleep(10)


	if 'd' in debugCode.lower():
		print("Testing Direction")
		print("Setting Direction to LOW")
		GPIO.output(direction, GPIO.LOW)
		time.sleep(10)
		print("Setting Direction to HIGH")
		GPIO.output(direction, GPIO.HIGH)
		time.sleep(10)
try:
	GPIO.output(direction,GPIO.LOW)
	for i in range(0, 50):
		# GPIO.output(direction,switchValue(switching))
		GPIO.output(direction,GPIO.HIGH)
		time.sleep(.01)
		GPIO.output(step,GPIO.HIGH)
		time.sleep(.02)
		GPIO.output(step,GPIO.HIGH)
		time.sleep(.02)
		# if count > 100:
		# 	direct = switchValue(direct)
		# 	count = 0
		# 	rotations += 1
		# 	print("switching direction")
		# 	GPIO.output(direction,direct)
		# if rotations >= numCycles:
		# 	break
		# count += 1
	# 	directiono = count % 2
	# 	stepo = count
	# 	print("count = %.f, direction = %.f, step = %.d" % (count, directiono, stepo))

	# 	GPIO.output(direction, directiono)
	# 	GPIO.output(step, stepo)
	# 	time.sleep(0.5)
	# 	count += 1
except KeyboardInterrupt:
	# GPIO.output(enable,GPIO.HIGH)
	GPIO.cleanup()
	print("Test ended prematurely and enable set to HIGH")


# GPIO.output(enable,GPIO.HIGH)
GPIO.cleanup()
print("Test Completed, enable set to HIGH")

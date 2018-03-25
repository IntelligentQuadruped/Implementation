import time

import logging

try:
    import RPi.GPIO as GPIO
except:
    logging.warning("head.py: Could not import RPi module.")


class Head(object):

	def __init__(self):
		# Constants
		self.CONVERSION_FACTOR_TURN = 2.22 #steps per degree
		self.CONVERSION_FACTOR_TILT = 10.0 #steps per degree
		self.connect_head = False

		# Setting time to pause between steps of stepper motor
		self.MOTOR_DELAY = 0.01 #sec

        # setup pins for rotation
		self.STEP_PIN_TURN = 2
		self.STEP_PIN_TILT = 14
		self.DIRECTION_PIN_TURN = 3
		self.DIRECTION_PIN_TILT = 15
		self.ENABLE_PIN_TURN = 4
		self.ENABLE_PIN_TILT = 17

        # starting head position
		self.turn_angle = 0 #deg
		self.tilt_angle = 0 #deg
		self.turn_steps = 0 # count of steps from neutral
		self.tilt_steps = 0 # count of steps from neutral


	def connect(self):
		try:
            # Head control via pin communicatoin
			GPIO.setmode(GPIO.BCM)
            ## motor 1: turning
			GPIO.setup(self.STEP_PIN_TURN, GPIO.OUT)
			GPIO.setup(self.DIRECTION_PIN_TURN, GPIO.OUT)
			GPIO.setup(self.ENABLE_PIN_TURN, GPIO.OUT)
            ## motor 2: tilting
			GPIO.setup(self.STEP_PIN_TILT, GPIO.OUT)
			GPIO.setup(self.DIRECTION_PIN_TILT, GPIO.OUT)
			GPIO.setup(self.ENABLE_PIN_TILT, GPIO.OUT)

            ## connecting to motors
			GPIO.output(self.ENABLE_PIN_TURN,GPIO.LOW)
			GPIO.output(self.ENABLE_PIN_TILT,GPIO.LOW)
			self.connected = True # stores which components are connected.
			logging.info("head.py: Head Component is connected.")
		except:
			self.connected = False
			logging.warning("head.py: Head Component could not be connected.")


	def disconnect(self):
		if self.connect_head:
			GPIO.cleanup()
		logging.info("head.py: Disconected head component successfully.")

	def resetHeadPosition(self):
		"""
		Resets head to move to 0 deg turn and 0 deg tilt.
		--- Under development ---
		How do we know the position when we first run the 
		script?
		----------------------------------------------
		"""
		return

	def __deg2step(self, degrees, CONVERSION_FACTOR):
		"""
		Converts number of degrees to number of steps and step direction.
		--- Under development ---
		Add conversion factor: emperically determined.
		Check: Direction assumption
		----------------------------------------------
		"""
        # assuming that LOW goes left and HIGH turns right
		direction = GPIO.LOW if degrees <= 0 else GPIO.HIGH
		steps = round(CONVERSION_FACTOR*degrees,0) # rounding to next integer
		steps = abs(int(steps))                    # convert to positive int type
		return (direction,steps)


	def look(self, **kwargs):
		""" 
		--- Under development ---
		Add max degree safety feature
		-----------------------------
		Controls the field of vision by rotating head. 
		Takes arguments as follows:
		keyword:    [int] value
		tilt:       [deg]  -45 to 45 
		turn:       [deg] -160 to 160
		"""
		if self.connect_head is False:
			logging.warning("head.py: Method look(): Cannot execute command. Head disconneted.")
			return
    
		steps_turn = 0
		direct_turn = None

		steps_tilt = 0
		direct_tilt = None

		for key in kwargs:
			if key == 'turn':
				if abs(kwargs[key]) > 160:
					logging.warning("head.py: >>> Degrees of head rotation out of bounds.")
					logging.warning("head.py: >>> Valid interval: [-160, 160]")
					return
				degrees = kwargs[key] - self.turn_angle
				direct_turn, steps_turn = self.__deg2step(degrees, self.CONVERSION_FACTOR_TURN)
				self.turn_steps = self.turn_steps + (-1*steps_turn) \
								if degrees < 0 else self.turn_steps + steps_turn
				self.turn_angle = self.turn_steps / self.CONVERSION_FACTOR_TURN
			elif key == 'tilt':
				if abs(kwargs[key]) > 45:
					logging.warning("head.py: Degrees of head rotation out of bounds.")
					logging.warning("head.py: >>> Valid interval: [-45, 45]")
					return
				degrees = kwargs[key] - self.tilt_angle
				direct_tilt, steps_tilt = self.__deg2step(degrees, self.CONVERSION_FACTOR_TILT)
				self.tilt_steps = self.tilt_steps + (-1*steps_tilt) \
								if degrees < 0 else self.tilt_steps + steps_tilt
				self.tilt_angle = self.tilt_steps / self.CONVERSION_FACTOR_TILT   
			else:
				logging.warning("head.py: Invalid command input to look().")

        # Choosing max steps value
		steps = steps_turn if steps_turn > steps_tilt else steps_tilt

        # Setting direction
		GPIO.output(self.DIRECTION_PIN_TURN,direct_turn)
		GPIO.output(self.DIRECTION_PIN_TILT,direct_tilt)

		logging.info("head.py: Look command sent: turn={}, tilt={}".format(direct_turn,direct_tilt))

        # Sending signal to motors
		for i in range(steps):
			if i < steps_turn:
				GPIO.output(self.STEP_PIN_TURN,GPIO.LOW)
			if i < steps_tilt:
				GPIO.output(self.STEP_PIN_TILT,GPIO.LOW)
			time.sleep(self.MOTOR_DELAY)
			if i < steps_turn:
				GPIO.output(self.STEP_PIN_TURN,GPIO.HIGH)
			if i < steps_tilt:
				GPIO.output(self.STEP_PIN_TILT,GPIO.HIGH)
			time.sleep(self.MOTOR_DELAY)
		logging.info("head.py: Head arrived at target position.")
		return


















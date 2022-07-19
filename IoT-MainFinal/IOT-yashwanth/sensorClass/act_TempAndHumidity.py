import numpy as np
import matplotlib.pyplot as plt


class temperatureAction:
	OFF = "OFF"
	ON =  "ON"

	def __init__(self, instanceID):
		self.status = self.ON 
		self.instanceID = instanceID
		self.setpoint = 25

	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.status 

	def updateValue(self, dataReceived):

		dataReceived = [*dataReceived.values()]
		avgValue = sum(dataReceived)/float(len(dataReceived))
		if avgValue > self.setpoint:
			self.changeState(self.ON)
		else :
			self.changeState(self.OFF)

	def getInstanceID(self):
		return self.instanceID

class humidityAction:
	OFF = "OFF"
	ON =  "ON"

	def __init__(self, instanceID):
		self.status = self.ON 
		self.instanceID = instanceID
		self.setpoint = 55


	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.status 

	def updateValue(self, dataReceived):
		dataReceived = [*dataReceived.values()]
		avgValue = sum(dataReceived)/float(len(dataReceived))
		if avgValue > self.setpoint:
			self.changeState(self.ON)
		else :
			self.changeState(self.OFF)

	def getInstanceID(self):
		return self.instanceID
		

class dustAction:
	OFF = "OFF"
	ON =  "ON"

	def __init__(self, instanceID):
		self.status = self.ON
		#self.status = self.OFF 
		self.instanceID = instanceID
		self.setpoint = 5


	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.status 

	def updateValue(self, dataReceived):
		dataReceived = [*dataReceived.values()]
		avgValue = sum(dataReceived)/float(len(dataReceived))
		print("Dust:", avgValue)
		if avgValue > self.setpoint:
			self.changeState(self.ON)
		else :
			self.changeState(self.OFF)

	def getInstanceID(self):
		return self.instanceID


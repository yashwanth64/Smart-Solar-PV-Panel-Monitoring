import numpy as np
import matplotlib.pyplot as plt
import math

# index 0 row: for Temperature
TEMP_ROOM = 0
HUMIDITY_RH = TEMP_ROOM + 1
DUST_RD = HUMIDITY_RH + 1


MEAN_INDEX = 0
VAR_INDEX = MEAN_INDEX + 1
RATE_INDEX = VAR_INDEX + 1


# mean, variance
const__SensorType_Data__ = []
const__SensorType_Data__.append(
    [24.5, 1.5, 0.5]
)  # Room Temp: mean 22.5 C, var =4.5 C min 68 F, max 77 F
const__SensorType_Data__.append([55.0, 5, 2])  # RH
const__SensorType_Data__.append([5,1,1]) #Dust

class TemperatureSensor:
    """docstring for HumiditySensor"""

    sensorType = "Temperature"
    unit = "celcius"

    def _pvt_CheckRange(self, value):

        value = min(value, self.maxVal)
        value = max(value, self.minVal)

        return value

    def __init__(self, instanceID):

        self.instanceID = instanceID

        self.mean = const__SensorType_Data__[TEMP_ROOM][MEAN_INDEX]
        self.variance = const__SensorType_Data__[TEMP_ROOM][VAR_INDEX]
        self.rate = const__SensorType_Data__[TEMP_ROOM][RATE_INDEX]

        self.maxVal = self.mean + self.variance
        self.minVal = self.mean - self.variance

        self.value = np.random.uniform(self.minVal, self.maxVal)

    def sense(self):

        self.value += (
            self.rate
            * self.variance
            * math.sin(np.random.uniform(-math.pi / 2, math.pi / 2))
        )
        self.value = self._pvt_CheckRange(self.value)
        return self.value

    # Provide instance ID of the sensor being read.
    def getInstanceID(self):
        return self.instanceID

class HumiditySensor:
    """docstring for HumiditySensor"""

    sensorType = "humidity"
    unit = "Percentage_RH"

    def _pvt_CheckRange(self, value):

        value = min(value, self.maxVal)
        value = max(value, self.minVal)

        return value

    def __init__(self, instanceID):

        self.instanceID = instanceID

        self.mean = const__SensorType_Data__[HUMIDITY_RH][MEAN_INDEX]
        self.variance = const__SensorType_Data__[HUMIDITY_RH][VAR_INDEX]
        self.rate = const__SensorType_Data__[HUMIDITY_RH][RATE_INDEX]

        self.maxVal = self.mean + self.variance
        self.minVal = self.mean - self.variance

        self.value = np.random.uniform(self.minVal, self.maxVal)

    def sense(self):

        self.value += (
            self.rate
            * self.variance
            * math.sin(np.random.uniform(-math.pi / 2, math.pi / 2))
        )
        self.value = self._pvt_CheckRange(self.value)
        return self.value

    # Provide instance ID of the sensor being read.
    def getInstanceID(self):
        return self.instanceID


class DustSensor:
    """docstring for DustSensor"""

    sensorType = "dust"
    unit = "Percentage_RD"

    def _pvt_CheckRange(self, value):

        value = min(value, self.maxVal)
        value = max(value, self.minVal)

        return value

    def __init__(self, instanceID):

        self.instanceID = instanceID

        self.mean = const__SensorType_Data__[DUST_RD][MEAN_INDEX]
        self.variance = const__SensorType_Data__[DUST_RD][VAR_INDEX]
        self.rate = const__SensorType_Data__[DUST_RD][RATE_INDEX]

        self.maxVal = self.mean + self.variance
        self.minVal = self.mean - self.variance

        self.value = np.random.uniform(self.minVal, self.maxVal)

    def sense(self):

        self.value += (
            self.rate
            * self.variance
            * math.sin(np.random.uniform(-math.pi / 2, math.pi / 2))
        )
        self.value = self._pvt_CheckRange(self.value)
        return self.value

    # Provide instance ID of the sensor being read.
    def getInstanceID(self):
        return self.instanceID

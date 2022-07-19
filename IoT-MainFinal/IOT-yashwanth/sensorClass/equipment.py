import numpy as np
import math
import random


class testBench:
    """docstring for testBench"""

    VOLT_VAR = 0.3  # Pass is 0.1
    CURR_VAR = 0.08  # Pass is 0.05

    MEAN_VOLT = 15

    MEAN_CURR = 20  # 20mA

    def __init__(self, instanceID):
        self.instanceID = instanceID
        self.toBeCalibDate = "21/07/2021"  # in DD-MM-YYYY format

    def getInstanceID(self):
        return self.instanceID

    def getVoltage(self):

        mean = self.MEAN_VOLT

        variance = random.choices(
            [self.VOLT_VAR - 0.03, self.VOLT_VAR - 0.01, self.VOLT_VAR],
            weights=[0.33, 0.33, 0.33],
            k=1,
        )

        return (np.random.normal(mean, variance)).item()

    def getCurrent(self):

        mean = self.MEAN_CURR

        variance = random.choices(
            [self.CURR_VAR - 0.03, self.CURR_VAR - 0.01, self.CURR_VAR],
            weights=[0.98, 0.019, 0.001],
            k=1,
        )
        return (np.random.normal(mean, variance)).item()

    def getToBeCalibDate(self):
        return self.toBeCalibDate

    def doSelfCheck(self):

        error = 0.000000001
        result = ""

        # check max range of voltage channel
        value = self.getVoltage()
        if (self.VOLT_VAR - error) > abs(value - self.MEAN_VOLT):
            result += "P"
        else:
            result += "F"

        # check max value of current channel
        value = self.getCurrent()
        if (self.CURR_VAR - error) > abs(value - self.MEAN_CURR):
            result += "P"
        else:
            result += "F"

        return result
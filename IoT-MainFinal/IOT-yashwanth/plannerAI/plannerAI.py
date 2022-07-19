#from sensorClass.client_broker_data import *
import csv
import pandas as pd
import datetime
import requests
import ast


plannerNewInitState = {}
file = '/home/prasad/NotMine/Yashwanth/IOT-main/IOT-yashwanth/dataBase/room01DB.csv'

objectList = []


updatedInitStateList = []

abvDictObect = {'HS': 'humitdity',
                'DS': 'dust',
                'RT': 'temperature',
                'ST': 'solderingTemp',
                'OS': 'oscilloscope',
                'TB': 'testbentch',
                'CB': 'convyor',
                'RA': 'temperatureActuator',
                'HA': 'humidityAcutator',
                'DA': 'dustActuator',
                'IR': 'InfraRed',
                'ES': 'esdProtection',
                'PS': 'pressure',
                'PL': 'logistics',
                'PM': 'maintainence',
                'PQ': 'quality',
                }


def isHigh(newVal, threshold):

    if newVal > threshold:
        return True
    else:
        return False


def isOn(sensorData):

    if sensorData == 'ON':
        return True
    else:
        return False


def aiPlanner(data, topic):
    #data.pop(["date", ])

    if 'actuator' in topic:
        print("Actuator", topic, data)
        for item in data:
            value = data[item]
            plannerNewInitState['isOn ' + item] = isOn(value)
            #print(plannerNewInitState['isOn ' + item])
            #updateListOfPeople(item, listOfPerson[2])

    elif 'sensor' in topic:
        #df = pd.read_csv (file,header = 0, index_col=[0])
        for item in data:
            value = data[item]
            print("AIPlanner:", value, topic)
            try:
                if 'temperature' in topic:

                    plannerNewInitState['isHigh '+item] = isHigh(value, 25.0)

                elif 'dust' in topic:

                    plannerNewInitState['isHigh '+item] = isHigh(value, 5.0)

                
            except Exception as e:
                #plannerNewInitState[item] = True
                print("-----error in creating init state-----------")
                print(item)
                print(topic)
                print(e)
                print("-----error in creating init state-----------")

    else:
        pass

    # get state info about pepople to be informed.

    # print(plannerNewInitState)
    # print(dictAllTypesPeople)


def getObjectType(string):

    resultString = abvDictObect[string[1:3]]

    return resultString


def updateInitState(stateDict_TF):

    initStateString = ''
    # make list of true only elements
    for item in stateDict_TF:
        if stateDict_TF[item] == True:

            # updatedInitStateList.append(item)
            initStateString += '\t\t(' + item + ')\n'

    return initStateString


def defineProblemFile():

    objectString = ''
    goalString = ''

    for item in objectList:

        if item[1:3] == "HS" or item[1:3] == "TB":
            continue
        typeObject = getObjectType(item)
        objectString += '\t\t ' + item + ' - ' + typeObject + '\n'

        goal = getGoalForObeject(item, typeObject)
        if goal != None:
            goalString += goal + '\n'

    initState = {**plannerNewInitState}
    stateString = updateInitState(initState)

    generateProblemFile(objectString, stateString, goalString)


def updateObjects(idList):
    # to be called if new thing is added to the network

    try:
        for item in ["date", "time"]:
            idList.remove(item)
    except ValueError:
        pass

    objectList.extend(idList)


def getGoalForObeject(id, ofType):

    if ofType == abvDictObect['RT'] or ofType == abvDictObect['DS']:

        goalstring = '\t\t\t(or\n\t\t\t\t(and (isHigh roomTemp1) (not(isOn tempAct1)) )\n\t\t\t\t(and (not(isHigh roomTemp1)) (isOn tempAct1) ) \n\t\t\t) ;or roomTemp1 tempAct1\n'
        goalstring = goalstring.replace('roomTemp1', id)
        # actuator id
        actID = 'A' + id[1] + 'A' + id[3:]
        goalstring = goalstring.replace('tempAct1', actID)

    else:
        goalstring = None

    return goalstring


def generateProblemFile(objectTypes, init, goal):
    with open('/home/prasad/NotMine/Yashwanth/IOT-main/IOT-yashwanth/plannerAI/problem_template_empty.txt') as f:
        newText = f.read()

        newText = newText.replace('OBJECTS_HERE', objectTypes)
        newText = newText.replace('STATE_HERE', init)
        newText = newText.replace('GOAL_HERE', goal)

    with open('/home/prasad/NotMine/Yashwanth/IOT-main/IOT-yashwanth/plannerAI/Problem_generated.pddl', "w") as f:
        f.truncate()
        f.write(newText)

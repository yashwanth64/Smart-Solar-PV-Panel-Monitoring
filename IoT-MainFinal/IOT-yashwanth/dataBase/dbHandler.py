import csv
import pandas as pd
import datetime
from plannerAI.plannerAI import *

masterFILE = "masteDB.csv"
path = "dataBase/"


def createDB(fileName):

    if not (".csv" in fileName):
        fileName += ".csv"

    if not (path in fileName):
        fileName = path + fileName

    print("----Creating " + fileName + "-----------------")
    df = pd.DataFrame()
    df.to_csv(fileName)
    print("----Created " + fileName + "-----------------")


def handleData(data):

    # 1.Ensure all data being sent to server is of dict type with instanceID as key

    data.update({"date": datetime.datetime.now().date()})
    data.update({"time": datetime.datetime.now().time()})
    # 2. Get list of keys/Instance ID
    tempKeyList = list(data.keys())

    # Find room Number/ line number from InstancID
    roomNumber = "room" + tempKeyList[0][3:5]

    # 3. Check in masta DB whether this room number is present in it or not, if not add to it.
    df = pd.read_csv(path + masterFILE, header=0, index_col=[0])

    if not (roomNumber in df.columns):
        df[roomNumber] = tempKeyList
        updateObjects(tempKeyList.copy())

    # tempKeyList = list(tempKeyList.extend([timeStamp]))
    for item in tempKeyList:
        if not (item in list(df[roomNumber])):
            df = df.append({roomNumber: item}, ignore_index=True)
            updateObjects([item])

    # print(df)

    df.to_csv(path + masterFILE)

    # print("---------Master done----")

    # now masterDB has list of instances for room 'n'
    # read the room db file

    newFileName = path + roomNumber + "DB" + ".csv"
    try:
        df = pd.read_csv(newFileName, header=0, index_col=[0])
    except:
        createDB(roomNumber + "DB")
        df = pd.read_csv(newFileName, header=0, index_col=[0])

    df = df.append(data, ignore_index=True)

    # print("all done")
    # print(df)
    df.to_csv(newFileName)


createDB(masterFILE)

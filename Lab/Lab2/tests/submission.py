## import modules here 
import pandas as pd
import numpy as np
import helper


################### Question 1 ###################

def buc_rec_optimized(df):  # do not change the heading of the function
    if df.shape[0] == 1:
        header = list(df)
        dfOutput = pd.DataFrame(columns=header)
        buc_one_dim(df, dfOutput)
    else:
        header = list(df)
        dfOutput = pd.DataFrame(columns=header)
        buc_muti_dim(df, [], dfOutput)
    return dfOutput


def buc_one_dim(df, dfOutput):
    mValue = list(df.loc[0])[-1]
    originalList = [list(df.loc[0])[:-1]]
    rowList = [list(df.loc[0])[:-1]]
    while len(originalList) != 0:
        tempList = originalList.pop(0)
        for index in range(len(tempList)):
            if tempList[index] != 'ALL':
                tempList_ = list_copy(tempList)
                tempList_[index] = 'ALL'
                originalList.append(tempList_)
                if tempList_ not in rowList:
                    rowList.append(tempList_)

    for row in rowList:
        row.append(mValue)
        dfOutput.loc[len(dfOutput)] = row


def list_copy(list):
    newList = []
    for i in list:
        newList.append(i)
    return newList


def buc_muti_dim(df, preDimValue, dfOutput):
    if df.shape[1] == 1:
        _preDimValue = list_copy(preDimValue)
        _preDimValue.append(sum(helper.project_data(df, 0)))
        dfOutput.loc[len(dfOutput)] = _preDimValue

    else:
        print("--------\n")
        dim1Value = set(helper.project_data(df, 0).values)
        _preDimvalue = list_copy(preDimValue)
        for value in dim1Value:
            slicedDimData = helper.slice_data_dim0(df, value)
            dimValue = list_copy(_preDimvalue)
            dimValue.append(value)
            print(dimValue)
            buc_muti_dim(slicedDimData, dimValue, dfOutput)

        removedData = helper.remove_first_dim(df)
        preDimValue_ = list_copy(_preDimvalue)
        preDimValue_.append('ALL')
        buc_muti_dim(removedData, preDimValue_, dfOutput)

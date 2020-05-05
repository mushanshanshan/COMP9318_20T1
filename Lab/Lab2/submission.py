## import modules here 
import pandas as pd
import numpy as np
import helper


################### Question 1 ###################

def buc_rec_optimized(df):  # do not change the heading of the function
    header = list(df)
    dfOutput = pd.DataFrame(columns=header)
    buc_muti_dim(df, [], dfOutput)
    return dfOutput

def list_copy(list):
    newList = []
    for i in list:
        newList.append(i)
    return newList

def buc_muti_dim(df, preDimValue, dfOutput):
    if df.shape[0] == 1:
        originalRow = list(df.iloc[0])
        strbinList = []
        for i in range (2 ** (len(originalRow)-1)):
            strbinList.append((str(bin(i))[2:]).rjust(len(originalRow)-1,'0'))
        for s in strbinList:
            tempList = list_copy(originalRow)
            for i in range(len(s)):
                if s[i] == '1':
                    tempList[i] = 'ALL'
            tempList = preDimValue + tempList
            dfOutput.loc[len(dfOutput)] = tempList


    elif df.shape[1] == 1:
        _preDimValue = list_copy(preDimValue)
        _preDimValue.append(sum(helper.project_data(df, 0)))
        dfOutput.loc[len(dfOutput)] = _preDimValue

    else:
        dim1Value = set(helper.project_data(df, 0).values)
        _preDimvalue = list_copy(preDimValue)
        for value in dim1Value:
            slicedDimData = helper.slice_data_dim0(df, value)
            dimValue = list_copy(_preDimvalue)
            dimValue.append(value)
            buc_muti_dim(slicedDimData, dimValue, dfOutput)

        removedData = helper.remove_first_dim(df)
        preDimValue_ = list_copy(_preDimvalue)
        preDimValue_.append('ALL')
        buc_muti_dim(removedData, preDimValue_, dfOutput)

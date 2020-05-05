## import modules here 
import pandas as pd
import numpy as np
import helper


################# Question 1 #################

# you can call helper functions through the helper module (e.g., helper.slice_data_dim0)
def buc_rec_optimized(df):# do not change the heading of the function
    pass # **replace** this line with your code
    input_data = df
    d=input_data.shape[1]
    all_sum=sum(input_data.iloc[:,-1].values)
    row=input_data.loc[[0]]
    colum_name=list(input_data)
    for i in colum_name:
        row[[i]]='0'
    global whole
    whole=pd.DataFrame()
    def buc_rec(input,row,d,all_sum):
        global whole
        dims = input.shape[1]
        if dims !=1:
            dim0_vals = set(helper.project_data(input, 0).values)
            for dim0_v in dim0_vals:
                 sub_data = helper.slice_data_dim0(input, dim0_v)
                 if (dims==d and sub_data.shape[0]==1 ):
                    v=helper.select_data(input,0,dim0_v).values.tolist()[0]
                    p=[[v[0]],['0']]
                    t=[]
                    for i in v[1:-1]:
                        t=[]
                        for j in p:
                            t.append(j+[i])
                            t.append(j+['0'])
                        p=t
                    for i in range(len(t)):
                        if set(t[i])==set(['0']):
                             t[i]=t[i]+[all_sum]
                        else:
                            t[i]=t[i]+v[-1:]
                    #print(t)
                    for i in t:
                        for j in range(len(i)):
                            n_row=row
                            n_row[[j]]=i[j]
                        whole=whole.append(n_row,ignore_index=True)
                    if input.shape[0]==1:
                        return
                    else:
                        continue
                 row[[d-dims]]=dim0_v
                 buc_rec(sub_data,row,d,all_sum)

            row[[d-dims]]='0'
            sub_data = helper.remove_first_dim(input)
            buc_rec(sub_data,row,d,all_sum)
        else:
            input_sum = sum(helper.project_data(input, 0) )*1.0
            row[[-1]]=input_sum
            #print(row)
            whole=whole.append(row,ignore_index=True)
    buc_rec(input_data,row,d,all_sum)
    whole.iloc[:,-1] = pd.to_numeric(whole.iloc[:,-1], errors='coerce')
    whole=whole.drop_duplicates(subset=whole.columns[:-1],keep='last').reset_index(drop=True)
    return whole

def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)

input_data = read_data('./asset/a_.txt')
output = buc_rec_optimized(input_data)
output
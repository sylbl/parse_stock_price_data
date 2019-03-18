import pandas as pd
import os
import numpy as np

dataDirPath = "/Users/s1830409/Google ドライブ/過去データ"

#fetch nk225 members list
nk225list = pd.read_csv(dataDirPath+"/NKY/minashi.csv",
                            usecols=['コード','みなし額面','/倍率'],
                            dtype={'コード':str})
# Timestamp index
nk225list.set_index('コード', inplace=True)

datas = {}
nonData = []

#fetch datas
for stockCode in nk225list.index:

    # 存在チェック
    if os.path.exists(dataDirPath+"/TPX100/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX100/"+stockCode+".csv"
    elif os.path.exists(dataDirPath+"/TPX400/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX400/"+stockCode+".csv"
    elif os.path.exists(dataDirPath+"/NKY/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/NKY/"+stockCode+".csv"
    else:
        nonData.append(stockCode)
        print("!!!File Not Found:" + stockCode + ".csv")
        
    # [Date], [PX_LAST]
    df = pd.read_csv(dataFilePath, usecols=['Date', 'PX_LAST'])

    #Convert to Timestamp
    df['Date'] = pd.to_datetime(df['Date'])

    # Timestamp index
    df.set_index('Date', inplace=True)

    # store lists
    datas[stockCode] = df

# output no data list
noDataf = pd.DataFrame(nonData)
noDataf.to_csv(dataDirPath+"/no_data.csv")

# fetch N225 index datas
# [Date], [PX_LAST]
dataFilePath = dataDirPath + "/NKY/nky.csv"
df = pd.read_csv(dataFilePath, usecols=['Date', 'PX_LAST'])

#Convert to Timestamp
df['Date'] = pd.to_datetime(df['Date'])

# Timestamp index
df.set_index('Date', inplace=True)

# store lists
datas['NKY'] = df

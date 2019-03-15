import pandas as pd
import os
import numpy as np

dataDirPath = "/Users/s1830409/Google ドライブ/過去データ"

#fetch nk225 members list
nk225list = pd.read_csv(dataDirPath+"/nk225-20190314.csv", header=None)
codeList = map(str, nk225list[0].T.values.tolist())

datas = {}
nonData = []

#fetch datas
for stockCode in codeList:
    print(stockCode)

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
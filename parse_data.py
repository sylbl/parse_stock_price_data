import pandas as pd
import os

dataDirPath = "/Users/s1830409/Google ドライブ/過去データ"

#fetch nk225 members list
nk225list = pd.read_csv(dataDirPath+"/nk225-20190314.csv", header=None)
codeList = map(str, nk225list[0].T.values.tolist())

datas = {}

#fetch datas
for stockCode in codeList:
    print(stockCode)

    # 存在チェック
    if os.path.exists(dataDirPath+"/TPX100/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX100/"+stockCode+".csv"
    elif os.path.exists(dataDirPath+"/TPX400/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX400/"+stockCode+".csv"
    else:
        print("!!!File Not Found:" + stockCode + ".csv")
        
    # [Date], [PX_LAST]
    df = pd.read_csv(dataFilePath, usecols=['Date', 'PX_LAST'])

    #Convert to Timestamp
    df['Date'] = pd.to_datetime(df['Date'])

    # store lists
    datas[stockCode] = df

print(datas)
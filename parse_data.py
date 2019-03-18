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
    '''if os.path.exists(dataDirPath+"/TPX100/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX100/"+stockCode+".csv"
    elif os.path.exists(dataDirPath+"/TPX400/"+stockCode+".csv"):
        dataFilePath = dataDirPath+"/TPX400/"+stockCode+".csv"
    elif '''
    if os.path.exists(dataDirPath+"/NKY/"+stockCode+".csv"):
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



# check
d = '2019-01-04'
i = 0
sum225 = 0
for code in nk225list.index:
    i += 1
    sum225 += datas[code].loc[d, 'PX_LAST'] * 50 * nk225list.loc[code, '/倍率'] / nk225list.loc[code, 'みなし額面']


print("correct: " + str(datas['NKY'].loc[d, 'PX_LAST']))
print(str(i) + ": " + str(sum225 / 27.003))

# date range
stDate = '2019-01-04'
edDate = '2019-03-15'

# marge datas
oData = datas['NKY'][stDate:edDate].rename(columns={'PX_LAST':'NKY'})
for code in nk225list.index:
    oData = oData.join(datas[code][stDate:edDate].rename(columns={'PX_LAST':code}))

# output datas
print(oData)
oData.to_csv(dataDirPath + '/nk225datas.csv')
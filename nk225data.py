import pandas as pd
import os

class DfNk225:

    DATA_DIR_PATH = "/Users/s1830409/Google ドライブ/過去データ/"
    DATA_FILE_PATH = DATA_DIR_PATH + "nk225datas.csv"
    MINASHI_FILE_PATH = DATA_DIR_PATH + "/NKY/minashi.csv"
    DIVISOR = 27.003

    def __init__(self):
        self.data = pd.read_csv(self.DATA_FILE_PATH)
        self.data.set_index('Date', inplace=True)

        self.minashi = pd.read_csv(self.MINASHI_FILE_PATH,
                            usecols=['コード','みなし額面','/倍率'],
                            dtype={'コード':str})
        self.minashi.set_index('コード', inplace=True)
    
    @property
    def membersData(self):
        return (self.data.iloc[:, 1:])
    
    @property
    def indexData(self):
        return (self.data['NKY'])
    
    @property
    def minashiF(self):
        return (50 * self.minashi['/倍率'] / self.minashi['みなし額面'])
    
    def makeOrigin225(self, startDate, endDate):

        oData = pd.DataFrame()

        for code in self.minashi.index:
            if os.path.exists(self.DATA_DIR_PATH+"NKY/"+code+".csv"):
                dataFilePath = self.DATA_DIR_PATH+"NKY/"+code+".csv"
            else:
                print("!!!File Not Found:" + code + ".csv")
            
            # [Date], [PX_LAST]
            df = pd.read_csv(dataFilePath, usecols=['Date', 'PX_LAST'])
            df = df.rename(columns={'PX_LAST':code})

            #Convert to Timestamp
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

            # store lists
            oData = pd.concat([oData, df[startDate:endDate]], axis=1)

        # calc225
        ori225 = round((oData * self.minashiF).sum(axis=1) / self.DIVISOR, 2)
        ori225.columns = ['NKY']

        oData = pd.concat([ori225, oData], axis=1)
        return (oData)


if __name__ == '__main__':

    dk = DfNk225()
    sDate = '2018/10/01'
    eDate = '2019/03/15'

    data = dk.makeOrigin225(sDate, eDate)
    print(data)
    data.to_csv(dk.DATA_DIR_PATH+"origin225.csv")









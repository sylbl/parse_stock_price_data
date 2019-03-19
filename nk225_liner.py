import pandas as pd
import numpy as np

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



if __name__ == "__main__":

    df225 = DfNk225()

    #print(df225.membersData)

    #print(df225.indexData)
    price = df225.membersData.loc['2019-02-04', :]
    div = 50 * df225.minashi['/倍率'] / df225.minashi['みなし額面']
    print((price * div).sum() / df225.DIVISOR)
    print(df225.indexData['2019-02-04'])








import pandas as pd

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

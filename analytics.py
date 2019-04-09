import pandas as pd
import nk225data as n225
import matplotlib.pyplot as plt
import numpy as np

def track():

    # load learned minashi
    filePath = "/Users/s1830409/Google ドライブ/outputData/minashi-learn.csv"
    minashiDf = pd.read_csv(filePath)
    minashiDf.set_index('コード', inplace=True)

    sDate = '2018/10/01'
    eDate = '2019/03/15'
    
    # make225sim
    nk = n225.DfNk225()

    ansData = nk.makeOrigin225(sDate, eDate, minashiDf['answer'].values)
    s100Data = nk.makeOrigin225(sDate, eDate, minashiDf['100'].values)
    s1000Data = nk.makeOrigin225(sDate, eDate, minashiDf['1000'].values)
    s10000Data = nk.makeOrigin225(sDate, eDate, minashiDf['10000'].values)
    s100000Data = nk.makeOrigin225(sDate, eDate, minashiDf['100000'].values)
    

    plt.plot(ansData['NK'], label="answer")
    plt.plot(s100Data['NK'], label="100")
    plt.plot(s1000Data['NK'], label="1000")
    plt.plot(s10000Data['NK'], label="10000")
    plt.plot(s100000Data['NK'], label="100000")
    plt.legend()
    #plt.show()

    plt.savefig("/Users/s1830409/Google ドライブ/outputData/ori225.png")

    oData = pd.DataFrame({
                            'answer':ansData['NK'],
                            '100':s100Data['NK'],
                            '1000':s1000Data['NK'],
                            '10000':s10000Data['NK'],
                            '100000':s100000Data['NK'],
                        })
    oData.to_csv("/Users/s1830409/Google ドライブ/outputData/ori225.csv")

def err():

    # load ori225
    data = pd.read_csv("/Users/s1830409/Google ドライブ/outputData/ori225.csv")
    data.set_index('Date', inplace=True)


    #in-sample range
    sDate = "2019-01-04"
    eDate = "2019-03-15"


    for col in data.iloc[:,1:].columns.values:

        er = np.square(data['answer'][sDate:eDate] - data[col][sDate:eDate])
        er = np.average(er)
        
        print("[in]" + col + ":", end="")
        print(str(er) + " >" + str(np.sqrt(er)))

        er = np.square(data['answer'][:sDate] - data[col][:sDate])
        er = np.average(er)
        
        print("[out]" + col + ":", end="")
        print(str(er) + " >" + str(np.sqrt(er)))









if __name__ == '__main__':

    #track()
    err()


import pandas as pd
import numpy as np
import tensorflow as tf
import math

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



if __name__ == "__main__":

    # NK225データを用意
    df225 = DfNk225()

    # みなし額を計算
    minashiPrice = df225.membersData * df225.minashiF
    
    # 行毎に合計/序数 で指数を算出
    myCalc = round(minashiPrice.sum(axis=1)/df225.DIVISOR, 2)

    # 正解値と並べる
    #print(pd.concat([myCalc, df225.indexData], axis=1))


    # みなし額面と除数を機械学習で見つける
    # みなし額面variable
    vM = tf.Variable(tf.ones([len(df225.minashi)],dtype=tf.float64))
    # 除数variable
    vD = tf.Variable(27.00, dtype=tf.float64)

    # モデル＝株価 * vM / vD
    model = tf.convert_to_tensor(df225.membersData)
    model = model * tf.convert_to_tensor(df225.minashiF)
    #model = tf.convert_to_tensor(df225.membersData) * vM / vD
    model = tf.reduce_sum(tf.transpose(model), 0) / vD
    #model = tf.round(model * 100) / 100
    

    
    # Minimize
    answer = tf.convert_to_tensor(df225.indexData)
    loss = tf.reduce_mean(tf.square(model - answer))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)
    

    # Before starting, initialize the variables. We will 'run' this firs
    init = tf.global_variables_initializer()

    # Launch the graph.
    sess = tf.Session()
    sess.run(init)

    #print(sess.run(vM), sess.run(vD))
    print(sess.run(model))
    print(sess.run(loss))

    
    # Fitting
    for step in range(20001):
        sess.run(train)
        if step % 100 == 0:
            print(step, sess.run(vD), sess.run(loss))
    print(sess.run(model))

    # close
    sess.close()











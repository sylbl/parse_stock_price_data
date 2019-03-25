import nk225data as n225
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # 株価データを用意
    data = n225.DfNk225()

    # みなし株価調整値
    vM = tf.Variable(tf.ones([len(data.minashiF)], dtype=tf.float64))
    vM = vM / data.DIVISOR

    # 日経平均モデル = sum(個別銘柄株価(i) * vM(i))
    model = tf.convert_to_tensor(data.membersData) * vM
    model = tf.reduce_sum(tf.transpose(model), 0)

    # 正解データ
    answer = tf.convert_to_tensor(data.indexData)

    # コスト関数
    loss = tf.reduce_mean(tf.square(model - answer))

    # 学習法
    learnRate = 0.00000001
    optimizer = tf.train.GradientDescentOptimizer(learnRate)
    train = optimizer.minimize(loss)

    # session
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    print(sess.run(vM))

    # 記録用
    stepArr = []
    lossArr = []
    minashiDf = pd.DataFrame({'answer':data.minashiF})
    print(minashiDf)

    # Fitting
    step = 0
    while True:
        # 学習回数入力
        print("number: ", end="")
        n = int(input())

        # 0以下の入力で終了
        if (n <= 0):
            break
        else:
            
            for step in range(step + 1, step + n + 1):
                sess.run(train)

                if (step % 100 == 0):
                    stepArr.append(step)
                    lossArr.append(sess.run(loss))
                #print(step, sess.run(loss))
            
            # 学習結果表示
            print(step, sess.run(model), sess.run(answer))
            print(sess.run(vM) * data.DIVISOR, sess.run(loss))
            newDf = pd.DataFrame({step: sess.run(vM)*data.DIVISOR}, index=minashiDf.index)
            minashiDf = minashiDf.join(newDf)
            plt.plot(stepArr, lossArr, label="loss")
            plt.xlabel("step")
            plt.ylabel("loss")
            #plt.show()
    
    # 出力
    OUTPUT_DIR_PATH = "/Users/s1830409/Google ドライブ/outputData/"
    minashiDf.to_csv(OUTPUT_DIR_PATH+"minashi-learn.csv")
    plt.savefig(OUTPUT_DIR_PATH+"minashi-learn-fig.png")



        





import nk225data as n225
import pandas as pd
import tensorflow as tf


if __name__ == '__main__':

    data = n225.DfNk225()

    # 除数を学習
    # 除数
    vD = tf.Variable(20, dtype=tf.float64)
    # みなし額面
    vM = tf.Variable(tf.ones([len(data.minashiF)], tf.float64))
    # 株価
    hPrice = tf.placeholder(tf.float64, [len(data.minashiF)])
    # モデル構築
    model = hPrice * vM
    model = tf.reduce_sum(model) / vD

    
    # Minimize
    hAnswer = tf.placeholder(tf.float64)
    loss = tf.reduce_mean(tf.square(model - hAnswer))
    optimizer = tf.train.GradientDescentOptimizer(0.000001)
    train = optimizer.minimize(loss)
    

    # Before starting, initialize the variables. We will 'run' this firs
    init = tf.global_variables_initializer()

    # Launch the graph.
    sess = tf.Session()
    sess.run(init)

    for step in range(1001):
        
        for date in data.membersData.index:
            line = data.membersData.loc[date].values
            answer = data.indexData.loc[date]

            sess.run(train, feed_dict={ hPrice: line,
                                        hAnswer: answer})
            
            if step % 100 == 0:
                print(step, sess.run(model, feed_dict={hPrice:line}), answer, sess.run(loss, feed_dict={hPrice:line, hAnswer:answer}))

        '''
        if step % 100 == 0:
            print(step, sess.run(vD))
        '''

    # close
    sess.close()




# -*- coding: utf-8 -*-
import tensorflow as tf
from poems.model import rnn_model
from poems.poems import process_poems
import numpy as np
from get_datas import get_datas_from_database


start_token = 'B'
end_token = 'E'
model_dir = './model/'
corpus_file = './data/poems.txt'


def predict():
    batch_size = 1
    print('## loading model from %s...' % model_dir)
    input_data = tf.placeholder(tf.int32, [batch_size, None])

    end_points = rnn_model(model='lstm', input_data=input_data, output_data=None, vocab_size=33+16,
                           rnn_size=128, output_num=7,input_num=7,num_layers=7, batch_size=1, learning_rate=0.01)

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        checkpoint = tf.train.latest_checkpoint(model_dir)
        saver.restore(sess, checkpoint)
        ssqdata = get_datas_from_database()
        
        x=ssqdata[len(ssqdata)-1]
        print("input: %s"%(x+np.asarray([1,1,1,1,1,1,1])))
        [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                         feed_dict={input_data: [x]})
        results=get_correct(predict)
        print("output:%s"%results)
        print("预测下一组双色球结果：红 {} {} {} {} {} {}, 蓝 {}".format(results[0],results[1],results[2],results[3],results[4],results[5], results[6]))
        
def get_correct(predict):
    results = []
    for i in range(6):
        result=np.argmax(predict[i],axis=0)
        while result<0 or result>32:
            predict[i][result] -= 1
            result=np.argmax(predict[i],axis=0)
        results.append(result)
        for j in range(i+1, 6):
            predict[j][result] -= 1

    results.sort()

    result=np.argmax(predict[6],axis=0)
    while result<0 or result>15:
        predict[6][result] -= 1
        result=np.argmax(predict[6],axis=0)
    results.append(result)


    results=results+np.asarray([1,1,1,1,1,1,1])
    return results


if __name__ == '__main__':
    predict()







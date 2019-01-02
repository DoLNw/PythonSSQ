# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from functools import reduce

from poems.model import rnn_model
from poems.poems import process_poems
from get_datas import get_datas_from_database

start_token = 'B'
end_token = 'E'
model_dir = './model/'
corpus_file = './data/poems.txt'


def test():
    batch_size = 1
    print('## loading model from %s...' % model_dir)

    input_data = tf.placeholder(tf.int32, [batch_size, 7])
    end_points = rnn_model(model='lstm', input_data=input_data, output_data=None, vocab_size=33+16,
                            rnn_size=128, output_num=7,input_num=7,num_layers=7, batch_size=batch_size, learning_rate=0.01)

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        checkpoint = tf.train.latest_checkpoint(model_dir)
        saver.restore(sess, checkpoint)
        ssqdata = get_datas_from_database()

        predict = sess.run(end_points['prediction'], feed_dict={input_data: [ssqdata[2223]]})
        predict_result, aa = get_correct(predict)
        print("概率最大的一组: {}".format(predict_result))

        for c in range(2, 11):
            j = -1
            for i in aa:
                j += 1
                predict[j][i] -= 1
            predict_result, aa = get_correct(predict)
            print("概率第{}大的一组: {}".format(c, predict_result))


def get_correct(predict):
    results = []
    aa = []
    for i in range(6):
        result=np.argmax(predict[i],axis=0)
        while result<0 or result>32:
            predict[i][result] -= 1
            result=np.argmax(predict[i],axis=0)
        results.append(result)
        for j in range(i+1, 6):
            predict[j][result] -= 1
    aa = results[0:6]
    results.sort()

    result=np.argmax(predict[6],axis=0)
    while result<0 or result>15:
        predict[6][result] -= 1
        result=np.argmax(predict[6],axis=0)
    results.append(result)
    aa.append(result)

    results=results+np.asarray([1,1,1,1,1,1,1])
    return results, aa


if __name__ == '__main__':
    test()
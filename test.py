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

        accuracy = 0
        for i in range(2206, 2224):
            predict = sess.run(end_points['prediction'], feed_dict={input_data: [ssqdata[i]]})
            correct_result = np.asarray(ssqdata[i+1])+np.asarray([1,1,1,1,1,1,1])
            predict_result = get_correct(predict)
            matches = match(correct_result, predict_result)
            print("组{}正确率: {}".format(i, reduce(sum, matches)/8))
            accuracy += reduce(sum, matches)/8
        accuracy /= 18
        print("模型准确率: {}".format(accuracy))

def sum(x, y):
    return x+y

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

    result=np.argmax(predict[6],axis=0)
    while result<0 or result>15:
        predict[6][result] -= 1
        result=np.argmax(predict[6],axis=0)
    results.append(result)

    results.sort()
    results=results+np.asarray([1,1,1,1,1,1,1])
    return results

def match(correct_result, predict_result):
    mathes = []
    for i in correct_result:
        mathes.append(0)
        for j in predict_result:
            if i == j:
                mathes.pop()
                mathes.append(1)
                break
    mathes[-1] *= 2
    return mathes

if __name__ == '__main__':
    test()
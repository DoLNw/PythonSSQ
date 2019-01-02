# -*- coding: utf-8 -*-
import os
import numpy as np
import tensorflow as tf
import math

from poems.model import rnn_model
from poems.poems import process_poems, generate_batch
from get_datas import get_datas_from_database


tf.app.flags.DEFINE_integer('batch_size', -1, 'batch size.')
tf.app.flags.DEFINE_float('learning_rate', 0.0001, 'learning rate.')
tf.app.flags.DEFINE_string('model_dir', os.path.abspath('./model'), 'model save path.')
tf.app.flags.DEFINE_string('file_path', os.path.abspath('./data/poems.txt'), 'file name of poems.')
tf.app.flags.DEFINE_string('model_prefix', 'poems', 'model save prefix.')
tf.app.flags.DEFINE_integer('epochs', 15000, 'train how many epochs.')

FLAGS = tf.app.flags.FLAGS


def run_training():
    if not os.path.exists(FLAGS.model_dir):
        os.makedirs(FLAGS.model_dir)
    
    ssqdata=get_datas_from_database()
    trainnum = 2206
    batches_inputs=ssqdata[0:trainnum-1]
    batches_outputs = ssqdata[1:trainnum]
    FLAGS.batch_size=trainnum-1
    del ssqdata

    input_data = tf.placeholder(tf.int32, [FLAGS.batch_size, 7])
    output_targets = tf.placeholder(tf.int32, [FLAGS.batch_size, 7])
    end_points = rnn_model(model='lstm', input_data=input_data, output_data=output_targets, vocab_size=33+16,
                           output_num=7,input_num=7,
                           rnn_size=128, num_layers=7, batch_size=FLAGS.batch_size, learning_rate=FLAGS.learning_rate)
    

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        start_epoch = 0
        
        checkpoint = tf.train.latest_checkpoint(FLAGS.model_dir)
        if checkpoint:
            saver.restore(sess, checkpoint)
            print("## restore from the checkpoint {0}".format(checkpoint))
            start_epoch += int(checkpoint.split('-')[-1])
        print('## start training...')
        
        for epoch in range(start_epoch, FLAGS.epochs):
            loss, _, _ = sess.run([
                end_points['total_loss'],
                end_points['last_state'],
                end_points['train_op']
            ], feed_dict={input_data: batches_inputs, output_targets: batches_outputs})
            
            print('Epoch: %d, training loss: %.6f' % (epoch, loss))
            if epoch % 10 == 0:
                saver.save(sess, os.path.join(FLAGS.model_dir, FLAGS.model_prefix), global_step=epoch)

def main(_):
    run_training()


if __name__ == '__main__':
    tf.app.run()







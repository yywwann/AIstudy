# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

# creat data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.1 + 0.3

# create tensorflow structure start
Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights*x_data + biases  # 预测的y

loss = tf.reduce_mean(tf.square(y-y_data))  # 预测的y与真实的y的差别
optimizer = tf.train.GradientDescentOptimizer(0.5)  # 优化器 减少loss
train = optimizer.minimize(loss)

init = tf.initialize_all_variables()  # 初始化之前创建的变量
# create tensorflow structure end

sess = tf.Session()
sess.run(init)

for step in range(201):
    sess.run(train)
    if step% 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))

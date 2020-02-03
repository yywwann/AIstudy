>环境
macos
python3.7
tensorflow 1.8.0 (随便选的,不会2.0)
远古教程,会有远古代码

# Tensorflow 基础构架
## 0 处理结构
Tensorflow 首先要定义神经网络的结构, 然后再把数据放入结构当中去运算和 training.
![](https://www.tensorflow.org/images/tensors_flowing.gif)
因为TensorFlow是采用数据流图（data　flow　graphs）来计算, 所以首先我们得创建一个数据流流图, 然后再将我们的数据（数据以张量(tensor)的形式存在）放在数据流图中计算. 节点（Nodes）在图中表示数学操作,图中的线（edges）则表示在节点间相互联系的多维数据数组, 即张量（tensor). 训练模型时tensor会不断的从数据流图中的一个节点flow到另一节点, 这就是TensorFlow名字的由来.

## 1 练习1
训练 y = 0.1*x + 0.3


```python
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

```


```shell
(0, array([0.23127228], dtype=float32), array([0.31420913], dtype=float32))
(20, array([0.12664041], dtype=float32), array([0.28576964], dtype=float32))
(40, array([0.10737547], dtype=float32), array([0.2960603], dtype=float32))
(60, array([0.10204193], dtype=float32), array([0.29890928], dtype=float32))
(80, array([0.10056531], dtype=float32), array([0.29969805], dtype=float32))
(100, array([0.10015651], dtype=float32), array([0.29991642], dtype=float32))
(120, array([0.10004333], dtype=float32), array([0.2999769], dtype=float32))
(140, array([0.10001198], dtype=float32), array([0.2999936], dtype=float32))
(160, array([0.10000332], dtype=float32), array([0.29999822], dtype=float32))
(180, array([0.10000093], dtype=float32), array([0.2999995], dtype=float32))
(200, array([0.10000027], dtype=float32), array([0.29999986], dtype=float32))
```

## 2 Session 会话控制
`Session` 是 Tensorflow 为了控制,和输出文件的执行的语句. 运行 `session.run()` 可以获得你要得知的运算结果, 或者是你所要运算的部分.

首先，我们这次需要加载 Tensorflow ，然后建立两个 `matrix` ,输出两个 `matrix` 矩阵相乘的结果。


```python
import tensorflow as tf

# create two matrixes

matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],
                       [2]])
product = tf.matmul(matrix1,matrix2)
```

因为 `product` 不是直接计算的步骤, 所以我们会要使用 `Session` 来激活 `product` 并得到计算结果. 有两种形式使用会话控制 `Session` 。

```python
# method 1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()
# [[12]]

# method 2
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)
# [[12]]
```

## 3 Variable 变量

在 Tensorflow 中，定义了某字符串是变量，它才是变量，这一点是与 Python 所不同的。

定义语法： `state = tf.Variable()`


```python
import tensorflow as tf

state = tf.Variable(0, name='counter')

# 定义常量 one
one = tf.constant(1)

# 定义加法步骤 (注: 此步并没有直接计算)
new_value = tf.add(state, one)

# 将 State 更新成 new_value
update = tf.assign(state, new_value)
```

如果你在 Tensorflow 中设定了变量，那么初始化变量是最重要的！！所以定义了变量以后, 一定要定义 `init = tf.global_variables_initializer()` .

到这里变量还是没有被激活，需要再在 `sess` 里, `sess.run(init)` , 激活 `init` 这一步.


```python
# 如果定义 Variable, 就一定要 initialize
# init = tf.initialize_all_variables() # tf 马上就要废弃这种写法
init = tf.global_variables_initializer()  # 替换成这样就好
 
# 使用 Session
with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))
```

注意：直接 `print(state)` 不起作用！！

一定要把 `sess` 的指针指向 `state` 再进行 print 才能得到想要的结果！

## 4 Placeholder 传入值

`placeholder` 是 Tensorflow 中的占位符，暂时储存变量.

Tensorflow 如果想要从外部传入data, 那就需要用到 `tf.placeholder()`, 然后以这种形式传输数据 `sess.run(***, feed_dict={input: **})`.

示例：

```python
import tensorflow as tf

#在 Tensorflow 中需要定义 placeholder 的 type ，一般为 float32 形式
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

# mul = multiply 是将input1和input2 做乘法运算，并输出为 output 
ouput = tf.multiply(input1, input2)
```

接下来, 传值的工作交给了 `sess.run()` , 需要传入的值放在了`feed_dict={}` 并一一对应每一个 `input`. `placeholder` 与 `feed_dict={}` 是绑定在一起出现的。

```python
with tf.Session() as sess:
    print(sess.run(ouput, feed_dict={input1: [7.], input2: [2.]}))
# [ 14.]
```

## 5 建造神经网络
### 添加层 def add_layer()
在 Tensorflow 里定义一个添加层的函数可以很容易的添加神经层,为之后的添加省下不少时间.

神经层里常见的参数通常有`weights`、`biases`和激励函数。

定义添加神经层的函数`def add_layer()`,它有四个参数：输入值、输入的大小、输出的大小和激励函数，我们设定默认的激励函数是None。

在生成初始参数时，随机变量(normal distribution)会比全部为0要好很多，所以我们这里的`weights`为一个`in_size`行, `out_size`列的随机变量矩阵。

`biases`的推荐值不为0，所以我们这里是在0向量的基础上又加了`0.1`。

定义`Wx_plus_b`, 即神经网络未激活的值。其中，`tf.matmul()`是矩阵的乘法。

当activation_function——激励函数为None时，输出就是当前的预测值——Wx_plus_b，不为None时，就把Wx_plus_b传到activation_function()函数中得到输出。
```python
def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs
```

### 导入数据

构建所需的数据。 这里的`x_data`和`y_data`并不是严格的一元二次函数的关系，因为我们多加了一个`noise`,这样看起来会更像真实情况。

```python
x_data = np.linspace(-1,1,300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise
```

利用占位符定义我们所需的神经网络的输入。 `tf.placeholder()`就是代表占位符，这里的`None`代表无论输入有多少都可以，因为输入只有一个特征，所以这里是1。

```python
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])
```

接下来，我们就可以开始定义神经层了。 通常神经层都包括输入层、隐藏层和输出层。这里的输入层只有一个属性， 所以我们就只有一个输入；隐藏层我们可以自己假设，这里我们假设隐藏层有10个神经元； 输出层和输入层的结构是一样的，所以我们的输出层也是只有一层。 所以，我们构建的是——输入层1个、隐藏层10个、输出层1个的神经网络。

### 搭建网络

下面，我们开始定义隐藏层,利用之前的`add_layer()`函数，这里使用 Tensorflow 自带的激励函数`tf.nn.relu`。

```python
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
```

接着，定义输出层。此时的输入就是隐藏层的输出——l1，输入有10层（隐藏层的输出层），输出有1层。

```python
prediction = add_layer(l1, 10, 1, activation_function=None)
```

计算预测值prediction和真实值的误差，对二者差的平方求和再取平均。

```python
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))
```

接下来，是很关键的一步，如何让机器学习提升它的准确率。`tf.train.GradientDescentOptimizer()`中的值通常都小于1，这里取的是0.1，代表以0.1的效率来最小化误差`loss`。


```python
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
```

使用变量时，都要对它进行初始化，这是必不可少的。

```python
init = tf.global_variables_initializer()
```

定义`Session`，并用 Session 来执行 `init` 初始化步骤。 （注意：在tensorflow中，只有`session.run()`才会执行我们定义的运算。）

```python
sess = tf.Session()
sess.run(init)
```

### 训练

下面，让机器开始学习。

比如这里，我们让机器学习1000次。机器学习的内容是`train_step`, 用 `Session` 来 `run` 每一次 training 的数据，逐步提升神经网络的预测准确性。 (注意：当运算要用到`placeholder`时，就需要`feed_dict`这个字典来指定输入。)
每50步我们输出一下机器学习的误差。

```python
for i in range(1000):
    # training
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # to see the step improvement
        print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
```

### 结果可视化
`import matplotlib.pyplot as plt`

构建图形，用散点图描述真实数据之间的关系。 （注意：`plt.ion()`用于连续显示。）

```python
# plot the real data
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data, y_data)
plt.ion()#本次运行请注释，全局运行不要注释
plt.show()
```

散点图的结果为：

![](https://morvanzhou.github.io/static/results/tensorflow/3_3_1.png)

接下来，我们来显示预测数据。

每隔50次训练刷新一次图形，用红色、宽度为5的线来显示我们的预测数据和输入之间的关系，并暂停0.1s。


```python
for i in range(1000):
    # training
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # to visualize the result and improvement
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        prediction_value = sess.run(prediction, feed_dict={xs: x_data})
        # plot the prediction
        lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
        plt.pause(0.1)
```

最后，机器学习的结果为：

![](https://morvanzhou.github.io/static/results/tensorflow/3_3_2.png)

### 加速神经网络训练 (Speed Up Training)
* Stochastic Gradient Descent (SGD)
    * 分治
* Momentum
    * 下坡惯性
* AdaGrad
    * 弯路阻力
* RMSProp
    * 混合
* Adam
    * 混合优化

### 优化器 optimizer

![](https://morvanzhou.github.io/static/results/tensorflow/3_4_1.png)

## 6 Tensorboard 可视化

使用`with tf.name_scope('inputs')`可以将`xs`和`ys`包含进来，形成一个大的图层，图层的名字就是`with tf.name_scope()`方法里的参数。

```python
with tf.name_scope('inputs'):
    # define placeholder for inputs to network
    xs = tf.placeholder(tf.float32, [None, 1])
    ys = tf.placeholder(tf.float32, [None, 1])
```

我们需要使用 `tf.summary.FileWriter()` 将上面‘绘画’出的图保存到一个目录中，以方便后期在浏览器中可以浏览。 这个方法中的第二个参数需要使用`sess.graph` ， 因此我们需要把这句话放在获取`session`的后面。 这里的`graph`是将前面定义的框架信息收集起来，然后放在`logs/`目录下面。


```python
init = tf.global_variables_initializer()
sess = tf.Session()
+ writer = tf.summary.FileWriter("logs/", sess.graph)
sess.run(init)
```

### 在 layer 中为 Weights, biases 设置变化图表
我们在 `add_layer()` 方法中添加一个参数 `n_layer`,用来标识层数, 并且用变量 `layer_name` 代表其每层的名名称, 代码如下:

```python
layer_name='layer%s'%n_layer  ## define a new var
```

接下来,我们层中的`Weights`设置变化图, tensorflow中提供了`tf.summary.histogram()`方法,用来绘制图片, 第一个参数是图表的名称, 第二个参数是图表要记录的变量


```python
with tf.name_scope('layer'):
         with tf.name_scope('weights'):
              Weights= tf.Variable(tf.random_normal([in_size, out_size]),name='W')
            + tf.summary.histogram(layer_name + '/weights', Weights) # tensorflow >= 0.12
```

### 设置loss的变化图
loss是在tesnorBorad 的event下面的, 这是由于我们使用的是`tf.summary.scalar()` 方法.


```python
with tf.name_scope('loss'):
     loss= tf.reduce_mean(tf.reduce_sum(
              tf.square(ys- prediction), reduction_indices=[1]))
   + tf.summary.scalar('loss', loss)
```

接下来， 开始合并打包。 tf.summary.merge_all() 方法会对我们所有的 summaries 合并到一起. 因此在原有代码片段中添加：


```python
sess= tf.Session()

# merged= tf.merge_all_summaries()    # tensorflow < 0.12
merged = tf.summary.merge_all() # tensorflow >= 0.12

# writer = tf.train.SummaryWriter('logs/', sess.graph)    # tensorflow < 0.12
writer = tf.summary.FileWriter("logs/", sess.graph) # tensorflow >=0.12

# sess.run(tf.initialize_all_variables()) # tf.initialize_all_variables() # tf 马上就要废弃这种写法
sess.run(tf.global_variables_initializer())  # 替换成这样就好

for i in range(1000):
   sess.run(train_step, feed_dict={xs:x_data, ys:y_data})
   if i%50 == 0:
      rs = sess.run(merged,feed_dict={xs:x_data,ys:y_data})
      writer.add_summary(rs, i)
```

在 tensorboard 中查看效果


```shell
tensorboard --logdir logs
```





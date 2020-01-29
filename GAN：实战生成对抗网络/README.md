# GAN:实战生成对抗网络

## 2.2 使用GAN生成MNIST手写数字

无法运行
训练几次后就会发生


> /Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/matplotlib/image.py:395: UserWarning: Warning: converting a masked element to nan.
  dv = (np.float64(self.norm.vmax) -
/Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/matplotlib/image.py:396: UserWarning: Warning: converting a masked element to nan.
  np.float64(self.norm.vmin))
/Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/matplotlib/image.py:403: UserWarning: Warning: converting a masked element to nan.
  a_min = np.float64(newmin)
/Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/matplotlib/image.py:408: UserWarning: Warning: converting a masked element to nan.
  a_max = np.float64(newmax)
/Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/matplotlib/colors.py:918: UserWarning: Warning: converting a masked element to nan.
  dtype = np.min_scalar_type(value)
/Users/cccccccccchy/anaconda3/envs/ai_homework_1/lib/python3.6/site-packages/numpy/ma/core.py:713: UserWarning: Warning: converting a masked element to nan.
  data = np.array(a, copy=False, subok=subok)
Iter: 1000
D loss: nan
G_loss: nan

## 2.2.2 在Keras上利用DCGAN实现图像生成
#### Image generation with Deep Convolutional Generative Adversarial Network (DCGAN) using Keras
```bash
git clone https://github.com/jacobgil/keras-dcgan.git
cd keras-dcgan
```
#### Training MNIST 
```bash
python dcgan.py --mode train  --batch_size 128
```
#### Generating top 5% images according to discriminator
```bash
python dcgan.py --mode generate --batch_size 128 --nice
```

> OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.

若报上面错误,加上以下两行
```py
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
```
`macbook pro 2016`跑100轮估计要40h,跑了30h模型训练成这样
![](http://ultronxr-oss-02.oss-cn-shenzhen.aliyuncs.com/cdn/img/nbutacm/dcgan_1.png)

## 2.2.3 利用Tensorflow实现SSGAN
#### Implementing Semi-Supervised Learning-SSGAN on cifar-10 using Tensorflow

```bash
git clone https://github.com/gitlimlab/SSGAN-Tensorflow.git

cd SSGAN-Tensorflow
```
#### Download dataset
```bash
python download.py --dataset MNIST SVHN CIFAR10
```

#### Training MNIST
```bash
python trainer.py --dataset CIFAR10
```

#### Testing/Evaluating
```bash 
python evaler.py --dataset CIFAR10 --checkpoint ckpt_dir
```

#### Note: Both the training example procedure will take lot of times if run on cpu. So better to set up tensorflow on gpu and run on it.


> ModuleNotFoundError: No module named 'progressbar'

progressbar是Python2.6使用的，Python3.5装不了
```bash
pip install progressbar2
```

>  No module named 'cPickle'

```bash
在python3中将cPickle改为pickle
```

#### 搞了半天跑不起来,算了算了

## 3.2.1 利用CGAN生成时尚衣柜

```bash
python download.py
python simple-cgan.py
```

> WARNING: Logging before flag parsing goes to stderr.
calling dropout (from tensorflow.python.ops.nn_ops) with keep_prob is deprecated and will be removed in a future version.
Instructions for updating:
Please use ‘rate’ instead of ‘keep_prob’. Rate should be set to ‘rate = 1 - keep_prob’.

很奇怪,在win10上源码可以直接跑,mac上要改成下面的形式.
```py
例如:
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob )
改成：
h_fc1_drop = tf.nn.dropout(h_fc1, rate = 1-keep_prob )
```


利用下列代码进行类型强制转换
```py
GW1z = tf.Variable(tf.random_normal([noise_dim, Ghidden], stddev=0.1), name="GW1z")
GW1z = tf.cast(GW1z, tf.float32)
GW1y = tf.Variable(tf.random_normal([num_labels, Ghidden], stddev=0.1), name="GW1y")
GW1y = tf.cast(GW1y, tf.float32)
Gb1 = tf.Variable(tf.zeros(Ghidden), name="Gb1")
Gb1 = tf.cast(Gb1, tf.float32)
GW2 = tf.Variable(tf.random_normal([Ghidden, num_features], stddev=0.1), name="GW2")
GW2 = tf.cast(GW2, tf.float32)
Gb2 = tf.Variable(tf.zeros(num_features), name="Gb2")
Gb2 = tf.cast(Gb2, tf.float32)

DW1x = tf.Variable(tf.random_normal([num_features, K * Dhidden], stddev=0.01), name="DW1x")
DW1x = tf.cast(DW1x, tf.float32)
DW1y = tf.Variable(tf.random_normal([num_labels, K * Dhidden], stddev=0.01), name="DW1y")
DW1y = tf.cast(DW1y, tf.float32)
Db1 = tf.Variable(tf.zeros(K * Dhidden), name="Db1")
Db1 = tf.cast(Db1, tf.float32)
DW2 = tf.Variable(tf.random_normal([Dhidden, 1], stddev=0.01), name="DW2")
DW2 = tf.cast(DW2, tf.float32)
Db2 = tf.Variable(tf.zeros(1), name="Db2")
Db2 = tf.cast(Db2, tf.float32)
```

## 3.4.2 利用 TensorFlow 将苹果变成橘子
> 这些代码应该都是运行在linux环境下


```bash
# Clone Git repo
git clone https://github.com/xhujoy/CycleGAN-tensorflow
cd CycleGAN-tensorflow

# Download celebA dataset
bash ./download_dataset.sh apple2orange

# Training
python main.py --dataset_dir=apple2orange

# Tensorboard Visualization 
tensorboard --logdir=./logs
http://localhost:6006/

python main.py --dataset_dir=apple2orange --phase=test --which_direction=AtoB
```

垃圾电脑跑200趟要三个月 累了累了

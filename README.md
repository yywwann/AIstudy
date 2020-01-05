# RUN 
进去文件夹具体查看运行方式
# AIstudy
青年AI自强计划作业

## homework 1
熟悉python
制作字母雨

## homework 2
线性回归

## homework 3
- part1
    -  MNIST 逻辑回归
- part2
    - ann
- part3
    - MNIST nn

## homework 4
- part1
- part2
- part3
DNN
深度神经网络    
    
## homework 5
CNN
卷积神经网络
15000次跑了10个小时
Accyracy:87.35%
loss:0.3533
lr:0.0468

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





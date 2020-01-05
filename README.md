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

> OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.

加上以下两行
```py
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
```
`macbook pro 2016`跑100轮估计要`40h`




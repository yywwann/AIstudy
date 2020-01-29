# Tensorflow 基础构架

## 处理结构

Tensorflow 首先要定义神经网络的结构, 然后再把数据放入结构当中去运算和 training.

![](https://www.tensorflow.org/images/tensors_flowing.gif)

因为TensorFlow是采用数据流图（data　flow　graphs）来计算, 所以首先我们得创建一个数据流流图, 然后再将我们的数据（数据以张量(tensor)的形式存在）放在数据流图中计算. 节点（Nodes）在图中表示数学操作,图中的线（edges）则表示在节点间相互联系的多维数据数组, 即张量（tensor). 训练模型时tensor会不断的从数据流图中的一个节点flow到另一节点, 这就是TensorFlow名字的由来.

## 练习1

训练 y = 0.1*x + 0.3

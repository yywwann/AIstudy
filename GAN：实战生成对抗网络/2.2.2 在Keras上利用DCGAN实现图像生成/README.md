# MNIST Image generation with Deep Convolutional Generative Adversarial Network (DCGAN) using Keras

git clone https://github.com/jacobgil/keras-dcgan.git

cd keras-dcgan

# Training MNIST
python dcgan.py --mode train  --batch_size 128

# Generating top 5% images according to discriminator
python dcgan.py --mode generate --batch_size 128 --nice
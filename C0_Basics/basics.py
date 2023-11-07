### 小节1：介绍Python和NumPy

# 基础的Python操作
a = 10
b = 20
print("a + b =", a + b)

# 引入NumPy，一个专门用于数学处理的库
import numpy as np
x = np.array([1.0, 2.0, 3.0])
print("x:", x)

# 数组的基础操作
y = np.array([2.0, 4.0, 6.0])
print("x + y:", x + y)
print("x * y:", x * y)
print("x * y:", np.dot(x,y))


### 小节2：介绍激活函数
# 激活函数是神经网络中非常重要的组成部分。让我们从最基础的Sigmoid函数开始。
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.array([-1.0, 1.0, 2.0])
print("sigmoid(x):", sigmoid(x))


### 小节3：单层神经网络前向传播
# 在这一小节中，我们将实现一个简单的单层神经网络（也就是没有隐藏层的网络）。

```python
def forward(x, w, b):
    z = np.dot(x, w) + b
    return sigmoid(z)

w = np.array([0.5, 0.5])  # 权重
b = -0.2  # 偏置
x = np.array([0.9, 0.1])  # 输入

output = forward(x, w, b)
print("Output:", output)

### 小节4：多层神经网络前向传播
# 现在，我们将引入一个隐藏层来创建一个多层神经网络。

def multi_layer_forward(x, params):
    w1, w2 = params['W1'], params['W2']
    b1, b2 = params['b1'], params['b2']
    
    # 第一个隐藏层
    z1 = np.dot(x, w1) + b1
    a1 = sigmoid(z1)
    
    # 输出层
    z2 = np.dot(a1, w2) + b2
    output = sigmoid(z2)
    
    return output

params = {
    'W1': np.array([[0.1, 0.3], [0.2, 0.4]]),
    'b1': np.array([0.1, 0.2]),
    'W2': np.array([0.3, 0.4]),
    'b2': np.array([0.1])
}

x = np.array([1.0, 0.5])
output = multi_layer_forward(x, params)
print("Multi-layer Output:", output)

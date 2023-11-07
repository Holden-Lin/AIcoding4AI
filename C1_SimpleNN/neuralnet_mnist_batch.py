import numpy as np
import pickle
import sys, os
# 请在该脚本所在目录下运行该脚本（1_SimpleNN in this case)
sys.path.append(os.pardir)
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from dataset.mnist import load_mnist
from common.functions import sigmoid, softmax


# 本代码的目的是学习类，并了解简单的神经网络推理，代码改写自：https://github.com/oreilly-japan/deep-learning-from-scratch/tree/master/ch03
class SimpleNN:
    """
    一个用于图像分类的简单神经网络类。

    属性:
        network (字典): 存储预训练的权重和偏置项。
        x_test (np.ndarray): 测试集图片。
        t_test (np.ndarray): 测试集标签。
    """
    def __init__(self, weight_file="sample_weight.pkl"):
    #def __init__(self, weight_file=os.path.join(SCRIPT_DIR, "sample_weight.pkl")):
        """
        初始化 SimpleNN 类。

        参数:
            weight_file (字符串): 预训练权重的文件路径。
        """
        self.network = self.init_network(weight_file)
        self.x_test = None
        self.t_test = None

    def init_network(self, weight_file):
        """
        使用预训练的权重初始化网络。

        参数:
            weight_file (字符串): 预训练权重的文件路径。

        返回值:
            字典: 预训练的权重和偏置项。
        """
        try:
            with open(weight_file, "rb") as f:
                network = pickle.load(f)
            return network
        except FileNotFoundError as e:
            print(f"Could not find the weight file: {weight_file}")
            print("Please check the file path and try again.")
            sys.exit(1)  # Exit the program with an error code

    def load_data(
        self,
        dataset_loader=load_mnist,
        normalize=True,
        flatten=True,
        one_hot_label=False,
    ):
        """
        加载用于测试的数据集。

        参数:
            dataset_loader (函数): 加载数据集的函数。
            normalize (布尔值): 是否对数据集进行标准化。
            flatten (布尔值): 是否对数据集进行扁平化。
            one_hot_label (布尔值): 是否使用 one-hot 标签。
        """
        (x_train, t_train), (x_test, t_test) = dataset_loader(
            normalize=normalize, flatten=flatten, one_hot_label=one_hot_label
        )
        self.x_test = x_test
        self.t_test = t_test

    def predict(self, x):
        """
        预测给定输入图片的标签。

        参数:
            x (np.ndarray): 输入的图片数据。

        返回值:
            np.ndarray: Softmax 概率。
        """
        W1, W2, W3 = self.network["W1"], self.network["W2"], self.network["W3"]
        b1, b2, b3 = self.network["b1"], self.network["b2"], self.network["b3"]

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)
        a3 = np.dot(z2, W3) + b3
        y = softmax(a3)

        return y

    def evaluate(self):
        """
        评估模型在测试集上的准确率。
        """
        if self.x_test is None or self.t_test is None:
            print("测试数据尚未加载，请先运行 load_data()。")
            return

        accuracy_cnt = 0
        for i in range(len(self.x_test)):
            y = self.predict(self.x_test[i])
            p = np.argmax(y)
            if p == self.t_test[i]:
                accuracy_cnt += 1

        print("准确率:" + str(float(accuracy_cnt) / len(self.x_test)))


# 使用示例
nn = SimpleNN()
nn.load_data()  # 使用默认的MNIST数据集
nn.evaluate()

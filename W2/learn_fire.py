"""
Python Fire is a simple way to create a CLI in Python. Python Fire is a helpful tool for developing and debugging Python code. \
Python Fire helps with exploring existing code or turning other people's code into a CLI. \
Python Fire makes transitioning between Bash and Python easier. \
Python Fire makes using a Python REPL easier by setting up the REPL with the modules \
and variables you'll need already imported and created.
"""

# conda install -c conda-forge fire
import fire


# 定义一个函数，该函数有一个默认参数name，其默认值为"World"
# 可变参数 kwargs 表示还可以接受其他任意数量的参数
def hello(name="World", *kwargs):
    return f"Hello {name} {' '.join(kwargs)}!"


if __name__ == "__main__":
    # 使用fire库为hello函数生成命令行接口
    fire.Fire(hello)


# How to interact with this file in terminal
# 1. python learn_fire.py --help
# 2. python learn_fire.py Holden > this will replace the argument name with "Holden"
# 3. python learn_fire.py --name=Holden > this achieves the same effect
# 4. python learn_fire.py Holden How are you? > this

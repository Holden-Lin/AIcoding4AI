# psutil: A cross-platform process and system utilities module for Python
# conda install -c conda-forge psutil
import psutil as ps


class my_computer:
    def __init__(self):
        self.cores = ps.cpu_count(logical=False)
        self.logical_cores = None
        self.memories = ps.virtual_memory()

    def get_cpu_usage(self):
        cpu_usage = ps.cpu_percent(interval=1, percpu=True)
        for i, usage in enumerate(cpu_usage):
            print(f"CPU核心 {i + 1} 使用率: {usage}%")

    def show_cpus(self):
        self.logical_cores = ps.cpu_count(logical=True)
        print(f"物理CPU核心数量: {self.cores}")
        print(f"逻辑CPU核心数量: {self.logical_cores}")

    def show_memoreis(self):
        print(f"总内存容量: {self.memories.total / (1024 ** 3):.2f} GB")
        print(f"已使用内存: {self.memories.used / (1024 ** 3):.2f} GB")
        print(f"可用内存: {self.memories.available / (1024 ** 3):.2f} GB")
        print(f"内存使用率: {self.memories.percent}%")


if __name__ == "__main__":
    my_computer = my_computer()
    my_computer.get_cpu_usage()
    my_computer.show_cpus()
    my_computer.show_memoreis()

# ssh 批量执行命令程序
## 引言
使用本程序可连接到 ssh，然后批量执行命令，并可以在 excel 中显示执行命令的结果，以便快速进行操作。



## 环境

- 语言
    - Python 3.9.6
- 包
    - pandas 1.5.3
    - openpyxl 3.1.2
    - paramiko 3.3.1
    - PyYAML 6.0
    ```shell
    pip install pandas openpyxl paramiko PyYAML
    ```



## 运行

1. 请在 `config.yaml` 文件中修改需要连接的主机配置。

2. 请在 `command_list.txt` 文件中写入需要运行的命令（命令需逐行放置）

   

## 运行结果

<img src="http://file.stackboom.xin/img/image-20230812193534228.png" alt="image-20230812193534228" style="zoom:50%;" />

excel 结果：

<img src="http://file.stackboom.xin/img/image-20230812193636022.png" alt="image-20230812193636022" style="zoom: 50%;" />

## 青龙面板可用的雷神加速器自动暂停脚本

### 使用说明

1. 将 config.ini 文件中的 username、password 值修改为你自己的雷神账号、密码
2. 将 gateway_ip 替换为你自己使用雷神的电脑本地 ip 即可
3. 在青龙面板中新建文件夹 leigod，将 Python 文件和 cofig.ini 配置文件都上传到该文件夹下
4. 此脚本依赖的 Python 库为：requests

### 脚本原理

检测到装有雷神的电脑关机后，脚本就自动去暂停一下。建议设置每分钟都运行一次此脚本

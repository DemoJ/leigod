## 青龙面板可用的雷神加速器自动暂停脚本
### 使用说明
1. 将config.ini文件中的username、password值修改为你自己的雷神账号、密码  
2. 将gateway_ip替换为你自己使用雷神的电脑本地ip即可  
3. 在青龙面板中新建文件夹leigod，将Python文件和cofig.ini配置文件都上传到该文件夹下  
4. 此脚本依赖的Python库为：requests
### 脚本原理
检测到装有雷神的电脑关机后，脚本就自动去暂停一下。建议设置每分钟都运行一次此脚本

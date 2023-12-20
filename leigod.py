import requests
import configparser
import hashlib
import subprocess

def ping_gateway(gateway):
    try:
        output = subprocess.check_output(['ping', '-c', '4', gateway])  # 在 Windows 上使用 '-n' 代替 '-c'
        return True
    except subprocess.CalledProcessError:
        return False

def hash_password(password):
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 将密码转换为字节串
    password_bytes = password.encode("utf-8")
    # 更新哈希对象
    md5_hash.update(password_bytes)
    # 获取加密后的密码（哈希值）
    hashed_password = md5_hash.hexdigest()
    return hashed_password

# 创建 ConfigParser 对象
config = configparser.ConfigParser()
# 读取配置文件
config.read("config.ini")

username = config.get("login","username")
password = hash_password(config.get("login","password"))


base_url = "https://webapi.leigod.com"

data = {
    "account_token": None,
    "country_code": 86,
    "lang": "zh_CN",
    "password": "{}".format(password),
    "region_code": 1,
    "src_channel": "guanwang",
    "user_type": "0",
    "username": "{}".format(username),
}

def login(data):
    url = base_url + "/api/auth/login"
    req = requests.post(url, json=data)
    if req.status_code==200:
        account_token=eval(req.text)['data']['login_info']['account_token']
        data['account_token']=account_token
    else:
        print(req.text)

def pause(data):
    url = base_url + "/api/user/pause"
    req = requests.post(url, json=data)
    if req.status_code==200:
        print(req.text)
        return True
    else:
        print(req.text)
        return False

# 指定网关的 IP 地址
gateway_ip = config.get('pc','gateway_ip')
power_status=config.get('pc','status')

if ping_gateway(gateway_ip):
    # 修改配置项的值
    config.set('pc', 'status', 'on')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("--检测到当前电脑已开启--")
elif power_status=='on':
    login(data)
    if pause(data):
        config.set('pc', 'status', 'off')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("--检测到电脑关机，已暂停雷神加速器")


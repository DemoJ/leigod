import requests
import configparser
import hashlib
import subprocess
import sys
import time

sys.path.append("/ql/data/scripts/my_rss")


def ping_gateway(gateway):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "4", gateway]
        )  # 在 Windows 上使用 '-n' 代替 '-c'
        return True
    except subprocess.CalledProcessError:
        return False


def hash_password(password):
    md5_hash = hashlib.md5()
    password_bytes = password.encode("utf-8")
    md5_hash.update(password_bytes)
    hashed_password = md5_hash.hexdigest()
    return hashed_password


def generate_sign(ts, params, key):
    def map_to_string(param):
        ks = sorted(param.keys())
        return "&".join([f"{k}={param[k]}" for k in ks])

    query_string = map_to_string(params)
    query_string += f"&key={key}"

    return hashlib.md5(query_string.encode()).hexdigest()


def create_session():
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.leigod.com/",
            "Content-Type": "application/json",
        }
    )
    return session


def login(session, data):
    try:
        url = base_url + "/api/auth/login/v1"
        req = session.post(url, json=data, timeout=20)
        if req.status_code == 200:
            print(req.text)
            account_token = eval(req.text)["data"]["login_info"]["account_token"]
            pause_data["account_token"] = account_token
            return True
        elif req.status_code == 418:
            print("Request blocked by server (418).")
            return False
        else:
            print(req.text)
            return False
    except Exception as e:
        print("An error occurred: {}".format(e))
        return False


def pause(session, data):
    try:
        url = base_url + "/api/user/pause"
        req = session.post(url, json=data, timeout=20)
        if req.status_code == 200:
            print(req.text)
            return True
        elif req.status_code == 418:
            print("Request blocked by server (418).")
            return False
        else:
            print(req.text)
            return False
    except Exception as e:
        print("An error occurred: {}".format(e))
        return False


# 创建 ConfigParser 对象
config = configparser.ConfigParser()
# 读取配置文件
config.read("config.ini")

username = config.get("login", "username")
password = hash_password(config.get("login", "password"))
base_url = "https://webapi.leigod.com"
key = "5C5A639C20665313622F51E93E3F2783"  # 密钥

# 获取当前时间戳
ts = str(int(time.time()))

pause_data = {
    "account_token": None,
    "lang": "zh_CN",
    "os_type": 4,
}

login_data = {
    "country_code": 86,
    "lang": "zh_CN",
    "password": "{}".format(password),
    "region_code": 1,
    "src_channel": "guanwang",
    "username": "{}".format(username),
    "ts": ts,
    "mobile_num": "{}".format(username),
    "os_type": 4,
}

# 生成 sign 值
sign = generate_sign(ts, login_data, key)
login_data["sign"] = sign

# 指定网关的 IP 地址
gateway_ip = config.get("pc", "gateway_ip")
power_status = config.get("pc", "status")

session = create_session()

if ping_gateway(gateway_ip):
    config.set("pc", "status", "on")
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    print("--检测到当前电脑已开启--")
elif power_status == "on":
    if login(session, login_data) and pause(session, pause_data):
        config.set("pc", "status", "off")
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        print("--检测到电脑关机，已暂停雷神加速器--")
else:
    print("--当前电脑无活动，已跳过--")

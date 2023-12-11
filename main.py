import speedtest
import sqlite3
import time
import requests
from fake_useragent import UserAgent


"注意要关闭代理，并且确保没有网速占用(如下载资源)"
"id在数据库合并的时候会重复，所以在合并的时候需要删除"
place = input("please input the place num:")


def get_time():
    time_ymd = time.strftime("%Y-%m-%d", time.gmtime())
    time_hms = time.strftime("%H:%M:%S", time.localtime())
    weeks = time.strftime("%w", time.gmtime())
    print("现在时间：", time_ymd, time_hms, "星期：", weeks)
    return time_ymd, time_hms, weeks
    # print(type(time_ymd)) ,"str"


def post_data_old():
    print("正在检索本地数据并发送")
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("select * from speedtest")
    datas = cursor.fetchall()
    print(f"检索到本地数据{len(datas)}条")
    if datas:
        for data in datas:
            try:
                #  发送post到web服务器,删除本地的此条记录
                cursor.execute("delete from speedtest where id=?", (data[0]))
                db.commit()
            except:
                pass
    cursor.close()
    db.close()


def save_data():
    time_ymd, time_hms, weeks = get_time()
    speed_up, speed_down = get_speed()
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    print("-----------正在保存至数据库-----------------")
    cursor.execute('''insert into speedtest(upload,download,time_ymd,time_hms,weeks,place) values(?,?,?,?,?,?)''', (speed_up, speed_down, time_ymd, time_hms, weeks, place))
    db.commit()
    cursor.close()
    db.close()
    print("---------测试结束，已保存在数据库-------------")


def get_speed():
    print("------开始测速，请耐心等待------")
    st = speedtest.Speedtest()
    speed_up = st.upload()
    speed_up = speed_up / 1024 / 1024
    print("upload:", speed_up, "Mb")
    speed_down = st.download()
    speed_down = speed_down / 1024 / 1024
    print("download", speed_down, "Mb")
    return speed_up, speed_down


def post_data_to_web():
    speed_up, speed_down = get_speed()
    time_ymd, time_hms, weeks = get_time()
    ua = UserAgent()
    # ua.random随机生成一个User-Agent头部信息
    header = {'User-Agent': ua.random}
    url = 'xxx'
    data_dict = {}
    response = requests.post(url, headers=header, data=data_dict)
    print(response)


if __name__ == "__main__":
    post_data_old()

try:
    post_data_to_web()
except:
    save_data()

    #  连接web服务器发送post请求，若失败则保存在本地数据库，再次访问时重新发送


while True:
    pass

import speedtest
import sqlite3
import time
import requests
import sys


"注意要关闭代理，并且确保没有网速占用(如下载资源)"
"id在数据库合并的时候会重复，所以在合并的时候需要删除"
place = input("please input the place num:")


def error(e):
    print("!!!")
    print(e)
    print("出现错误，敲回车键结束程序")
    end = input()
    exit(1)


def get_time():
    time_ymd = time.strftime("%Y-%m-%d", time.gmtime())
    time_hms = time.strftime("%H:%M:%S", time.localtime())
    week = time.strftime("%w", time.gmtime())
    print("现在时间：", time_ymd, time_hms, "星期：", week)
    return time_ymd, time_hms, week
    # print(type(time_ymd)) ,"str"


def post_data_old():
    print("正在检索本地数据并发送至云服务器")
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("select * from speedtest")
    datas = cursor.fetchall()
    print(f"检索到本地数据{len(datas)}条")
    if datas:
        for data in datas:
            try:
                print(f"正在向服务器发送数据{data}")
                post_data_to_web(get_speed=(data[1], data[2]), get_time=(data[3], data[4], data[5]), place=data[6])
                #  发送post到web服务器,删除本地的此条记录
                cursor.execute("delete from speedtest where id=?", (data[0],))
                db.commit()
                print(f"从本地删除数据{data}")
            except Exception as e:
                error(e)

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
    print("upload:", speed_up, "Mb/s")
    speed_down = st.download()
    speed_down = speed_down / 1024 / 1024
    print("download", speed_down, "Mb/s")
    print("测速完毕")
    return speed_up, speed_down


def post_data_to_web(get_speed, get_time, place=place):
    print("正在连接云服务器")
    speed_up, speed_down = get_speed
    time_ymd, time_hms, week = get_time
    headers = {
        'Content-Type': 'application/json',  # 设置 Content-Type 为 JSON 格式
        'Authorization': 'Bearer 7e958935580e724a73fcb2691bda3b31a609b7c9feff6ae7d0b02a69368feb78'  # 设置 Authorization 头
    }

    url = 'https://sqtp.zju.external.foraphe.eu.org/api/upload?k=test1&salt=123'
    data_json = {"payload": [{
        "location": place,
        "upload": speed_up,
        "download": speed_down,
        "time": time_ymd + " " +time_hms
    }]}
    response = requests.post(url, headers=headers, json=data_json)
    print(response)


if __name__ == "__main__":
    try:
        post_data_old()
    except:
        print("连接云服务器失败，请稍后再尝试")
    get_time = get_time()
    try:
        get_speed = get_speed()
    except Exception as e:
        print("链接测速服务器失败，请稍后再尝试")
        error(e)

    try:
        post_data_to_web(get_speed=get_speed, get_time=get_time, place=place)
    except Exception as e:
        print(e, "\n将以本地方式存储！！！")
        save_data()
        #  连接web服务器发送post请求，若失败则保存在本地数据库，再次访问时重新发送
    print("所有进程已经结束，敲回车结束程序")
    end = input()
    exit(0)


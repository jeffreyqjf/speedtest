import speedtest
import sqlite3
import time


"注意要关闭代理，并且确保没有网速占用(如下载资源)"
"id在数据库合并的时候会重复，所以在合并的时候需要删除"
place = input("please input the place num:")
time_ymd = ""
time_hms = ""
weeks = ""
def make_time():
    global time_ymd, time_hms, weeks
    time_ymd = time.strftime("%Y-%m-%d", time.gmtime())
    time_hms = time.strftime("%H:%M:%S", time.gmtime())
    weeks = time.strftime("%w", time.gmtime())
    print("现在时间：",time_ymd, time_hms, "星期：", weeks)
    # print(type(time_ymd)) ,"str"
make_time()

try:
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    print("------开始测速，请耐心等待------")
    st = speedtest.Speedtest()
    speed_up = st.upload()
    speed_up = speed_up / 1024 / 1024
    print("upload:", speed_up, "Mb")
    speed_down = st.download()
    speed_down = speed_down / 1024 / 1024
    print("download", speed_down, "Mb")
    print("-----------正在保存至数据库-----------------")
    cursor.execute('''insert into speedtest(upload,download,time_ymd,time_hms,weeks,place) values(?,?,?,?,?,?)''', (speed_up, speed_down, time_ymd, time_hms, weeks, place))
    db.commit()
    cursor.close()
    db.close()
    print("---------测试结束，已保存在数据库-------------")

except:
    print("出错了，确保关闭代理，如果还是出错，请联系程序开发者")

while True:
    pass

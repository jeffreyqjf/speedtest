import speedtest
st = speedtest.Speedtest()
speed = st.upload()
print("upload:", speed)

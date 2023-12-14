import psutil
import socket

def get_active_network_interface():
    # 获取所有网络接口
    interfaces = psutil.net_if_addrs()

    # 遍历接口并找到有活动连接的接口
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                return interface

    return None

# 获取当前活动的网络接口
active_interface = get_active_network_interface()
if active_interface:
    print(f"当前活动网络接口: {active_interface}")
else:
    print("没有找到活动网络接口")

# 获取当前活动的网络接口
active_interface = get_active_network_interface()
if active_interface:
    print(f"当前活动网络接口: {active_interface}")
else:
    print("没有找到活动网络接口")


'''
import pywifi, time
def get_signal_strength(interface_name='wlan0'):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()

    for result in scan_results:
        if result.ssid and result.bssid:
            # 输出 SSID、BSSID 和信号强度
            print(f"SSID: {result.ssid}, BSSID: {result.bssid}, 信号强度: {result.signal}")

# 获取信号强度
get_signal_strength()

'''

import wifi
def get_wifi_info():
    wifi_data = wifi.scan.Cell.all("1")
    if wifi_data:
        first_network = wifi_data[0]
        ssid = first_network.ssid
        bssid = first_network.address
        frequency = first_network.frequency
        encryption_type = first_network.encryption_type
        return ssid, bssid, frequency, encryption_type
    else:
        return None

# 获取 Wi-Fi 信息
wifi_info = get_wifi_info()
if wifi_info:
    ssid, bssid, frequency, encryption_type = wifi_info
    print(f"Wi-Fi SSID: {ssid}")
    print(f"Wi-Fi BSSID: {bssid}")
    print(f"Wi-Fi Frequency: {frequency} MHz")
    print(f"Wi-Fi Encryption Type: {encryption_type}")
else:
    print("没有找到 Wi-Fi 接口")
import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import random

# ---------------------- 坐标系转换（WGS84 ↔ GCJ02）----------------------
def wgs84_to_gcj02(lat, lon):
    pi = 3.14159265358979323846
    a = 6378245.0
    ee = 0.00669342162296594323

    def transform_lat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * (abs(x))**0.5
        ret += (20.0 * (6.0 * (x * pi / 180.0)) + 20.0 * (6.0 * (y * pi / 180.0))) / 2.0
        ret += (20.0 * (6.0 * (x * pi / 180.0))) / 2.0
        ret += (40.0 * (6.0 * (x * pi / 180.0))) / 3.0
        ret += (160.0 * (x * pi / 180.0)) / 3.0
        ret += (320.0 * (x * pi / 180.0)) / 3.0
        return ret

    def transform_lon(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * (abs(x))**0.5
        ret += (20.0 * (6.0 * (x * pi / 180.0)) + 20.0 * (6.0 * (y * pi / 180.0))) / 2.0
        ret += (20.0 * (x * pi / 180.0)) / 2.0
        ret += (40.0 * (x * pi / 180.0)) / 3.0
        ret += (150.0 * (x * pi / 180.0)) / 3.0
        ret += (300.0 * (x * pi / 180.0)) / 3.0
        return ret

    dLat = transform_lat(lon - 105.0, lat - 35.0)
    dLon = transform_lon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * pi
    magic = 1 - ee * (radLat ** 2)
    sqrtMagic = (magic)**0.5
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * (radLat) * pi)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return mgLat, mgLon

# ---------------------- 页面布局 ----------------------
st.title("无人机智能化应用 - 项目Demo")

tab1, tab2 = st.tabs(["航线规划（地图）", "飞行监控（心跳包）"])

# ---------------------- 航线规划（地图）----------------------
with tab1:
    st.subheader("3D地图显示 & 坐标设置")
    st.write("坐标系：GCJ-02（高德/百度）")

    col1, col2 = st.columns(2)
    with col1:
        latA = st.number_input("A点纬度", value=32.2322, step=0.0001)
        lonA = st.number_input("A点经度", value=118.749, step=0.0001)
    with col2:
        latB = st.number_input("B点纬度", value=32.2343, step=0.0001)
        lonB = st.number_input("B点经度", value=118.749, step=0.0001)

    height = st.slider("飞行高度(m)", 0, 100, 50)

    # 转换坐标系
    a_lat, a_lon = wgs84_to_gcj02(latA, lonA)
    b_lat, b_lon = wgs84_to_gcj02(latB, lonB)

    # 地图
    m = folium.Map(location=[a_lat, a_lon], zoom_start=18)
    folium.Marker([a_lat, a_lon], popup="起点A", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker([b_lat, b_lon], popup="终点B", icon=folium.Icon(color="green")).add_to(m)
    folium.PolyLine(locations=[[a_lat, a_lon], [b_lat, b_lon]], color="blue").add_to(m)

    st_folium(m, width=800, height=400)

# ---------------------- 飞行监控（心跳包）----------------------
with tab2:
    st.subheader("实时心跳包数据")
    st.write("每秒自动刷新，模拟无人机回传")

    # 心跳显示区域
    hb_time = st.empty()
    hb_latlon = st.empty()
    hb_height = st.empty()
    hb_battery = st.empty()
    hb_status = st.empty()

    # 模拟心跳
    while True:
        t = time.strftime("%H:%M:%S")
        lat = round(32.2322 + random.uniform(-0.0005, 0.0005), 4)
        lon = round(118.749 + random.uniform(-0.0005, 0.0005), 4)
        h = random.randint(45, 55)
        bat = random.randint(80, 100)

        hb_time.metric("时间", t)
        hb_latlon.metric("当前坐标", f"{lat}, {lon}")
        hb_height.metric("飞行高度", f"{h} m")
        hb_battery.metric("电量", f"{bat}%")
        hb_status.success("连接状态：正常")

        time.sleep(1)

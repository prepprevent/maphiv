import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen  # ✅ Thêm import này
# ✅ Đặt layout rộng để mở rộng chiều ngang toàn trang
st.set_page_config(layout="wide")

# Load file Excel
file_path = "Toa do - Copy.xlsx"
df = pd.read_excel(file_path)

# Sidebar chọn dịch vụ
st.sidebar.title("Lọc dịch vụ")
all_services = ['ARV', 'PREP', 'Methadone', 'XNKĐ']
selected_services = st.sidebar.multiselect("Chọn dịch vụ:", all_services, default=all_services)

# Lọc theo dịch vụ
filtered_df = df[df[selected_services].notna().any(axis=1)]

# Tạo bản đồ với fullscreen
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11)
Fullscreen(position='topright').add_to(m)  # ✅ Thêm nút fullscreen

for _, row in filtered_df.iterrows():
    stt = row['STT']
    if stt == 51:
        color = 'red'
    elif stt == 72:
        color = 'purple'
    elif stt == 61:
        color = 'blue'
    else:
        color = 'gray'

    popup_content = f"""
    <b>{row['Tên phòng khám']}</b><br>
    {row['Địa chỉ']}<br>
    <i>Dịch vụ:</i> {', '.join([s for s in selected_services if pd.notna(row.get(s))])}
    """
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=popup_content,
        icon=folium.Icon(color=color)
    ).add_to(m)

# ✅ Tăng kích thước bản đồ hoặc dùng toàn bộ chiều ngang
st.title("Bản đồ cơ sở cung cấp dịch vụ tại Hồ Chí Minh mới")

# 📊 Box thống kê
st.subheader("📊 Thống kê số cơ sở theo dịch vụ được chọn")
counts = {}
for service in selected_services:
    counts[service] = filtered_df[service].notna().sum()
cols = st.columns(len(selected_services))
for i, service in enumerate(selected_services):
    cols[i].metric(label=service, value=counts[service])

# Hiển thị bản đồ
st_folium(m, use_container_width=True, height=800)

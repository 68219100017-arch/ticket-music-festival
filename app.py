
import streamlit as st
import csv
import io
from datetime import datetime

#ตั้งค่าหน้าเว็บไซต์
st.set_page_config(
    page_title="DIGITAL MUSIC FESTIVAL"
    page_icon="🎫"
    layout="centered"
)

#กำหนดราคาตั๋ว
prices = {
    "Standard" : 100,
    "VIP" : 250,
    "Permium" : 400
}

#เตรียมพื้นที่เก็บข้อมูล
if "order" not in st.session_state :
  st.session_state.order = []
if "last_order" not in st.session_state :
  st.session_state.order = None

#ส่วนหัวเว็บไซต์
st.title("🎫DIGITAL MUSIC FESTIVAL")
st.write(
    "ยินดีต้อนรับเข้าสู่ระบบจำหน่ายตั๋วออนไลน์"
    "กรุณาเลือกประเภทตั๋วและระบุจำนวนที่ต้องการ"
)
st.divider()

#แสดงประเภทตั๋ว
st.subheader("ประเภทตั๋ว🎫")
col1, col2, col3 = st.columns(3)
with col1:
  st.metric("Standard" , "100 บาท")
with col2:
  st.metric("VIP" , "250 บาท")
with col3:
  st.metric("Primuium" , "400 บาท")
st.divider

#แบบฟอร์มสั่งซื้อ
st.subheader("💌แบบฟอร์มคำสั่งซื้อ")
customer_name = st.text.input("ชื่อผู้ซื้อ")
ticket_type = st.selectbox(
    "เลือกประเภทตั๋ว",
    ["Standard", "VIP", "Premium"]
)

quantity = st.number_input(
    "จำนวนตั๋ว",
    min_value = 1,
    max_value = 10,
    value = 1,
    step = 1
)

#คำนวณราคา
price = prices[ticket_type]
total = price * quantity

st.info(f"ราคาต่อตั๋ว {price:,} บาท")
st.write(f"จำนวน {quantity,} ใบ")
st.subheader(f"ยอดรวม {total:,} บาท")

#ปุ่มยืนยันคำสั่งซื้อ
if st.button ("ยืนยันคำสั่งซื้อ", type="premium") :
  if customer_name.strip() == " ":
    st.error("กรุณากรอกชื่อผู็ซื้อ")

  else:
    order = {
        "order_id":f"T{len(st.session_state.orders)+1:04d}",
        "customer_name" : customer_name.strip(),
        "ticket_type" : ticket_type,
        "quantity":int(quantity),
        "price":price,
        "total":total,
        "order_time":datatime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    st.session_state.order.append(order)
    st.session_state.last_order = order

    st.success("สั่งซื้อตั๋วเรียบร้อยแล้ว!")

  #แสดงสรุปคำสั่งซื้อล่าสุด
  if st.session_state.last_order is not None:
    order = st.session_state.last_order

    st.divider()
    st.subheader("🎐สรุปคำสั่ง")

st.write(f"หมายเลขคำสั่งซื้อ: {order['order_id']}")
st.write(f"ชื่อผู้ซื้อซื้อ: {order['customer_name']}")
st.write(f"ประเภทตั๋ว: {order['ticket_type']}")
st.write(f"จำนวน: {order['quantity']} ใบ")

st.success(f"ยอดชำระรวม: {order['total']} บาท")

#ประวัติคำสั่งซื้อ
if st.session_state.orders:

  st.divider()
  st.subheader("ประวัติคำสั่งซื้อ")

  st.dataframe(
      st.session_state.orders,
      use_container_width=True
  )

#เตรียมไฟล์ csv สำหรับดาวน์โหลด
cvs_buffer = io.StringIO()
filednames = list(st.session_state.orders[0].keys())

writer = csv.DictWriter(
    cvs_buffer,
    fieldnames=filednames
)

writer.writeheader()
writer.writerows(st.session_state.orders)

st.download_button(
    label = "ดาวน์โหลดประวัติคำสั่งซื้อ"
    data=csv_buffer.getvalue().encode("utf-8-sig")
    file_name="ticket_orders.csv"
    mime="text/csv"
)
st.cuption("DIGITAL MUSIC FESTIVAL | ระบบสั่งซื้อตั๋ว")

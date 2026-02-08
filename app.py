import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import date
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="مركز التحكم بالنظافة", page_icon="🏢", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'my_units' not in st.session_state:
    st.session_state.my_units = []

st.title("🏨 لوحة تحكم وحدات التأجير")
st.info(f"📅 تاريخ اليوم: {date.today().strftime('%Y-%m-%d')}")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ الإعدادات")
    with st.expander("📝 إضافة عقار جديد", expanded=True):
        u_name = st.text_input("اسم الشقة")
        u_link = st.text_input("رابط iCal")
        if st.button("➕ حفظ في القائمة"):
            if u_name and u_link:
                st.session_state.my_units.append({"name": u_name, "link": u_link})
                st.success(f"✅ تم إضافة {u_name}")

    phone = st.text_input("📱 رقم واتساب الشركة (مثال: 9665xxxxxxxx)")

with col2:
    st.markdown("### 📋 حالة النظافة اليوم")
    to_clean = []
    
    if st.session_state.my_units:
        for unit in st.session_state.my_units:
            try:
                today = date.today()
                evs = events(url=unit['link'], start=today, end=today)
                is_out = any(e.end.date() == today for e in evs)
                color = "#ff4b4b" if is_out else "#28a745"
                status_text = "🚨 خروج اليوم" if is_out else "✅ لا يوجد خروج"
                if is_out: to_clean.append(unit['name'])
                
                st.markdown(f"""
                    <div style="border-left: 10px solid {color}; background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <h4 style="margin:0;">{unit['name']}</h4>
                        <p style="margin:0; color: {color}; font-weight: bold;">{status_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.error(f"❌ خطأ في رابط: {unit['name']}")
    
    if to_clean and phone:
        clean_phone = ''.join(filter(str.isdigit, phone))
        msg = f"*تقرير النظافة* 🧹\nخروج في:\n" + "\n".join([f"📍 {n}" for n in to_clean])
        whatsapp_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; font-size: 22px;">
                     إرسال عبر WhatsApp 📲
                </div>
            </a>
        ''', unsafe_allow_html=True)

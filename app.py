import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import date
import urllib.parse

st.set_page_config(page_title="نظام النظافة الذكي", page_icon="🧹")

# حفظ البيانات في الجلسة مؤقتاً
if 'my_units' not in st.session_state:
    st.session_state.my_units = []

st.title("🏨 إدارة حجوزات النظافة")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    phone = st.text_input("رقم الواتساب (مثال: 9665xxxxxxxx)")
    
    st.divider()
    st.header("➕ إضافة عقار")
    u_name = st.text_input("اسم الشقة")
    u_link = st.text_input("رابط iCal")
    
    if st.button("حفظ العقار"):
        if u_name and u_link:
            st.session_state.my_units.append({"name": u_name, "link": u_link})
            st.success(f"تمت إضافة {u_name}")
        else:
            st.error("أدخل الاسم والرابط!")

st.subheader("📋 جدول المواعيد اليوم")
to_clean = []

if st.session_state.my_units:
    for unit in st.session_state.my_units:
        try:
            today = date.today()
            evs = events(url=unit['link'], start=today, end=today)
            is_out = any(e.end.date() == today for e in evs)
            
            if is_out:
                st.warning(f"🚨 {unit['name']}: خروج اليوم")
                to_clean.append(unit['name'])
            else:
                st.success(f"✅ {unit['name']}: لا يوجد خروج")
        except:
            st.error(f"⚠️ {unit['name']}: خطأ في الرابط")

    if to_clean and phone:
        clean_phone = ''.join(filter(str.isdigit, phone))
        msg = "🔔 *تقرير النظافة اليومي* 🧹\n\nتوجد عمليات خروج في:\n" + "\n".join([f"- {n}" for n in to_clean])
        whatsapp_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
        
        st.divider()
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 20px;">
                    إرسال عبر واتساب الآن 📲
                </div>
            </a>
        ''', unsafe_content_safe=True)
else:
    st.info("أضف عقاراتك من القائمة الجانبية.")

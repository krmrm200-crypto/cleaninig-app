import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import date
import urllib.parse

st.set_page_config(page_title="مدير النظافة", page_icon="🧹")

# استخدام "session_state" لحفظ الشقق مؤقتاً في المتصفح
if 'my_units' not in st.session_state:
    st.session_state.my_units = []

st.title("🏡 نظام إدارة النظافة")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    phone = st.text_input("رقم واتساب الشركة (مثال: 966500000000)")
    
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

# العرض الرئيسي
st.subheader("📋 جدول اليوم")
to_clean = []

if st.session_state.my_units:
    for unit in st.session_state.my_units:
        try:
            today = date.today()
            # فحص التقويم
            evs = events(url=unit['link'], start=today, end=today)
            is_out = any(e.end.date() == today for e in evs)
            
            status = "🚨 خروج اليوم" if is_out else "✅ محجوز/لا خروج"
            if is_out: to_clean.append(unit['name'])
            
            st.write(f"**{unit['name']}**: {status}")
        except:
            st.write(f"**{unit['name']}**: ⚠️ خطأ في الرابط")

    st.divider()
    
    # زر الواتساب المطور
    if st.button("📲 تجهيز رسالة الواتساب"):
        if to_clean and phone:
            msg = "🔔 تقرير النظافة اليومي:\n" + "\n".join([f"- {n}" for n in to_clean])
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'[اضغط هنا للإرسال من واتسابك]({url})')
        else:
            st.warning("لا توجد شقق للتنظيف أو لم تضع رقم الهاتف")
else:
    st.info("أضف عقاراتك من القائمة الجانبية.")

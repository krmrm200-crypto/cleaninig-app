import streamlit as st
import pandas as pd
import sqlite3
from icalevents.icalevents import events
from datetime import date
import urllib.parse

# إعداد قاعدة البيانات في السيرفر
def init_db():
    conn = sqlite3.connect('properties.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS units 
                 (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, ical_link TEXT)''')
    conn.commit()
    conn.close()

# دالة لجلب المواعيد (تم تحسينها لتجنب الأخطاء في السيرفر)
def check_ical(url):
    try:
        today = date.today()
        # جلب الفعاليات
        es = events(url=url, start=today, end=today)
        for event in es:
            # إذا كان موعد انتهاء الحجز (الخروج) هو اليوم
            if event.end.date() == today:
                return True
        return False
    except:
        return None

# --- الواجهة ---
st.set_page_config(page_title="مدير نظافة العقارات", page_icon="🧹")
init_db()

st.title("🏡 لوحة تحكم النظافة الذكية")
st.info("هذا الموقع يراقب حجوزات Airbnb و Gathern ويرسل تنبيهات لشركة النظافة.")

# إدارة البيانات
conn = sqlite3.connect('properties.db', check_same_thread=False)
units_df = pd.read_sql_query("SELECT * FROM units", conn)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    phone = st.text_input("رقم واتساب شركة النظافة", placeholder="9665xxxxxxxx")
    
    st.divider()
    st.header("➕ إضافة عقار")
    new_name = st.text_input("اسم الوحدة")
    new_plat = st.selectbox("المنصة", ["Airbnb", "Gathern"])
    new_link = st.text_input("رابط iCal")
    
    if st.button("حفظ"):
        if new_name and new_link:
            conn.execute("INSERT INTO units (name, platform, ical_link) VALUES (?, ?, ?)", 
                         (new_name, new_plat, new_link))
            conn.commit()
            st.success("تم الحفظ!")
            st.rerun()

# العرض الرئيسي لجدول اليوم
st.subheader("🧹 المهام المطلوبة اليوم")
if not units_df.empty:
    results = []
    to_clean_today = []
    
    for _, row in units_df.iterrows():
        is_checkout = check_ical(row['ical_link'])
        status = "✅ لا يوجد خروج"
        if is_checkout is True:
            status = "🚨 خروج (بحاجة تنظيف)"
            to_clean_today.append(row['name'])
        elif is_checkout is None:
            status = "⚠️ خطأ في الرابط"
            
        results.append({"العقار": row['name'], "المنصة": row['platform'], "الحالة": status})
    
    st.table(pd.DataFrame(results))

    # إرسال الواتساب
    if st.button("🚀 إرسال التقرير لشركة النظافة"):
        if to_clean_today and phone:
            message = f"🔔 *تقرير النظافة اليومي* \nتوجد عمليات خروج في:\n" + "\n".join([f"- {n}" for n in to_clean_today])
            encoded_msg = urllib.parse.quote(message)
            link = f"https://wa.me/{phone}?text={encoded_msg}"
            st.markdown(f"### [اضغط هنا للإرسال عبر واتساب]({link})")
        else:
            st.warning("لا توجد شقق للتنظيف أو لم يتم إدخال رقم الهاتف.")
else:
    st.write("لا توجد عقارات مضافة.")

conn.close()

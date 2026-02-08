import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import date
import urllib.parse

st.set_page_config(page_title="مدير النظافة", page_icon="🧹")

# حفظ البيانات في الجلسة
if 'my_units' not in st.session_state:
    st.session_state.my_units = []

st.title("🏡 نظام إدارة النظافة")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    # توضيح أهمية الصيغة الدولية
    phone = st.text_input("رقم الواتساب (مثال: 966501234567)", help="اكتب الرقم بدون أصفار وبدون علامة +")
    
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
st.subheader("📋 جدول المواعيد اليوم")
to_clean = []

if st.session_state.my_units:
    for unit in st.session_state.my_units:
        try:
            today = date.today()
            evs = events(url=unit['link'], start=today, end=today)
            is_out = any(e.end.date() == today for e in evs)
            
            if is_out:
                st.warning(f"🚨 {unit['name']}: خروج اليوم - بحاجة تنظيف")
                to_clean.append(unit['name'])
            else:
                st.success(f"✅ {unit['name']}: محجوز أو لا يوجد خروج")
        except:
            st.error(f"⚠️ {unit['name']}: خطأ في الرابط")

    st.divider()
    
    if to_clean:
        if phone:
            # تنظيف الرقم من أي رموز زائدة
            clean_phone = ''.join(filter(str.isdigit, phone))
            msg = "🔔 *تقرير النظافة اليومي* 🧹\n\nتوجد عمليات خروج في:\n" + "\n".join([f"- {n}" for n in to_clean])
            encoded_msg = urllib.parse.quote(msg)
            
            # رابط الواتساب المباشر
            whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
            
            st.info("اضغط على الزر أدناه ليفتح لك الواتساب مباشرة:")
            # زر كبير وواضح للجوال
            st.markdown(f'''
                <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 20px;">
                        إرسال عبر واتساب الآن 📲
                    </div>
                </a>
            ''', unsafe_content_safe=True)
        else:
            st.error("⚠️ لازم تكتب رقم الجوال في القائمة الجانبية أولاً")
    else:
        st.write("✨ لا توجد شقق تحتاج تنظيف اليوم.")
else:
    st.info("أضف عقاراتك من القائمة الجانبية (الزر اللي في الزاوية).")

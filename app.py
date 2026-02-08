import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import date
import urllib.parse

# إعداد الصفحة بثيم داكن وأنيق
st.set_page_config(page_title="مركز التحكم بالنظافة", page_icon="🏢", layout="wide")

# تصميم واجهة احترافية باستخدام CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .unit-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_content_safe=True)

# حفظ البيانات في الجلسة
if 'my_units' not in st.session_state:
    st.session_state.my_units = []

# العنوان العلوي
st.title("🏨 لوحة تحكم وحدات التأجير")
st.info(f"📅 تاريخ اليوم: {date.today().strftime('%Y-%m-%d')}")

# تقسيم الشاشة لعمودين
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ الإعدادات والإضافة")
    with st.expander("📝 إضافة عقار جديد", expanded=True):
        u_name = st.text_input("اسم الشقة (مثلاً: شقة 101)")
        u_link = st.text_input("رابط iCal (من Airbnb/Booking)")
        if st.button("➕ حفظ في القائمة"):
            if u_name and u_link:
                st.session_state.my_units.append({"name": u_name, "link": u_link})
                st.success(f"✅ تم إضافة {u_name}")
            else:
                st.error("أكمل البيانات أولاً")
    
    st.divider()
    phone = st.text_input("📱 رقم واتساب الشركة", placeholder="9665xxxxxxxx")
    st.caption("ملاحظة: اكتب الرقم دولي بدون أصفار")

with col2:
    st.markdown("### 📋 حالة النظافة اليوم")
    to_clean = []
    
    if st.session_state.my_units:
        for unit in st.session_state.my_units:
            try:
                today = date.today()
                evs = events(url=unit['link'], start=today, end=today)
                is_out = any(e.end.date() == today for e in evs)
                
                # تصميم بطاقة لكل شقة
                color = "#ff4b4b" if is_out else "#28a745"
                status_text = "🚨 خروج اليوم - يحتاج تنظيف" if is_out else "✅ محجوز أو لا يوجد خروج"
                
                if is_out: to_clean.append(unit['name'])
                
                st.markdown(f"""
                    <div style="border-left: 10px solid {color}; background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <h4 style="margin:0;">{unit['name']}</h4>
                        <p style="margin:0; color: {color}; font-weight: bold;">{status_text}</p>
                    </div>
                """, unsafe_content_safe=True)
            except:
                st.error(f"❌ خطأ في رابط الشقة: {unit['name']}")
    else:
        st.warning("⚠️ لا توجد عقارات مضافة حالياً. استخدم القائمة الجانبية للإضافة.")

    # منطقة زر الإرسال (تظهر فقط إذا فيه شقق خروج)
    if to_clean:
        st.divider()
        st.subheader("🚀 إرسال التقرير النهائي")
        if phone:
            clean_phone = ''.join(filter(str.isdigit, phone))
            msg = f"*تقرير النظافة ليوم {date.today()}* 🧹\n\nيوجد خروج في الشقق التالية:\n" + "\n".join([f"📍 {n}" for n in to_clean]) + "\n\n يرجى التوجه للتنظيف فوراً ⚡"
            whatsapp_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
            
            st.markdown(f'''
                <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; font-size: 22px; box-shadow: 0 4px 15px rgba(37,211,102,0.4);">
                         إرسال القائمة لشركة النظافة (WhatsApp) 📲
                    </div>
                </a>
            ''', unsafe_content_safe=True)
        else:
            st.error("👈 يرجى كتابة رقم الواتساب في جهة اليمين لتتمكن من الإرسال")

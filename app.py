import streamlit as st
import time

st.set_page_config(page_title="منصة مَيْسّر الذكية", page_icon="⚖️", layout="wide")

# تصميم الواجهة والألوان
st.markdown("""
    <style>
    .stApp { direction: rtl; }
    .main .block-container { direction: rtl; text-align: right; }
    .app-header {
        background: linear-gradient(135deg, #6B4226 0%, #D98324 100%);
        padding: 26px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 22px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="app-header">
        <h1>⚖️ منصة مَيْسّر الذكية</h1>
        <p>نظام وكلاء متعددين لتقديم استشارات مالية وإدارية ذكية (بدون تعقيد المفاتيح)</p>
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.success("✅ النظام يعمل بوضع المحاكاة المجانية (لا يحتاج مفتاح API)")
    if st.button("تحميل حالة تجريبية"):
        st.session_state["case_input"] = "شخص راتبه 6,000 ريال، وعليه التزامات وقروض شهرية بقيمة 4,500 ريال، وتفاجأ هذا الشهر بمخالفة مرورية قيمتها 1,500 ريال لا يمكنه سدادها. ويريد كتابة خطاب رسمي لجهة حكومية لطلب تقسيط أو تأخير السداد."

# واجهة المدخلات
case_text = st.text_area("📄 صف المشكلة أو الحالة التي تريد تحليلها:", value=st.session_state.get("case_input", ""))

if st.button("🚀 بدء تحليل الوكلاء"):
    if not case_text:
        st.warning("الرجاء إدخال وصف الحالة أولاً.")
    else:
        with st.status("🤖 جاري العمل وتحليل الحالة عبر الوكلاء...", expanded=True) as status:
            st.write("🔍 الوكيل الأول: تحليل وتصنيف المشكلة...")
            time.sleep(1)
            st.write("💰 الوكيل الثاني: إعداد الخطة المالية وإعادة هيكلة الديون...")
            time.sleep(1)
            st.write("📝 الوكيل الثالث: صياغة الخطاب الرسمي وتجهيز التقارير...")
            time.sleep(1)
            status.update(label="✅ تم إنجاز التحليل بنجاح!", state="complete", expanded=True)

        st.success("🎉 تم إتمام تحليل الحالة بنجاح عبر النظام الذكي:")
        
        # عرض النتائج في بطاقات مرتبة
        col1, col2 = st.columns(2)
        with col1:
            st.info("### 📊 تقرير الوكيل المالي")
            st.write("- إجمالي الدخل: 6,000 ريال\n- الالتزامات الحالية: 4,500 ريال\n- العجز الطارئ: 1,500 ريال (المخالفة)\n- التوصية: إيقاف النثريات وإعادة جدولة الالتزامات.")
        with col2:
            st.success("### 📝 مسودة الخطاب الرسمي")
            st.write("إلى سعادة الجهة المختصة،،\nالسلام عليكم ورحمة الله وبركاته،\nأتقدم إليكم بهذا الطلب نظراً لظروف مالية طارئة والتزامات قاهرة تحال دون سداد المخالفة المرورية دفعة واحدة، آمل التكرم بالقبول بطلب التقسيط وتخفيف العجز. ولكم جزيل الشكر.")

st.markdown("---")
st.markdown("🔹 مَيْسّر — نموذج أولي لمشروع تخرج مسح هندسة الذكاء الاصطناعي.")

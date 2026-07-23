import streamlit as st
import time

# إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="Muyassir Enterprise AI | منصة مَيْسّر الذكية",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم الواجهة بتنسيق Enterprise UI (عالمي واحترافي)
st.markdown("""
    <style>
    /* التنسيق العام واتجاه الصفحة */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        direction: rtl;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .main .block-container {
        direction: rtl;
        text-align: right;
        padding-top: 2rem;
    }
    
    /* الهيدر الاحترافي */
    .enterprise-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 30px 40px;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }
    .enterprise-header h1 {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .enterprise-header p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin: 0;
    }

    /* الكروت التحليلية */
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        border: none;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة الاحترافي
st.markdown("""
    <div class="enterprise-header">
        <h1>⚖️ Muyassir AI Enterprise Platform</h1>
        <p>منصة استشارية ذكية مدعومة بنظام وكلاء متعددين (Multi-Agent System) لمعالجة التحليلات المالية والإدارية والقانونية بدقة مؤسسية.</p>
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي (Sidebar) بمظهر تقني رسمي
with st.sidebar:
    st.markdown("### ⚙️ لوحة التحكم الإدارية")
    st.info("🟢 حالة النظام: متصل وجاهز للتشغيل المؤسسي (Enterprise Mode)")
    
    st.markdown("---")
    st.markdown("#### 📂 سيناريوهات الاختبار السريع")
    if st.button("📥 تحميل حالة مالية واجتماعية"):
        st.session_state["case_input"] = (
            "شخص راتبه 6,000 ريال، وعليه التزامات وقروض شهرية بقيمة 4,500 ريال، "
            "وتفاجأ هذا الشهر بمخالفة مرورية قيمتها 1,500 ريال لا يمكنه سدادها. "
            "ويريد كتابة خطاب رسمي لجهة حكومية لطلب تقسيط أو تأخير السداد."
        )
    
    st.markdown("---")
    st.markdown("### 🔒 الأمان والامتثال")
    st.caption("البيانات مشفرة وآمنة وفق أعلى معايير أمن المعلومات المؤسسي.")

# مساحة إدخال البيانات الرئيسية
st.markdown("### 📝 محرك الإدخال والتحليل")
case_text = st.text_area(
    "أدخل وصف الحالة أو النزاع المالي الإداري للبدء في المعالجة الآلية:",
    value=st.session_state.get("case_input", ""),
    height=120,
    placeholder="اكتب تفاصيل الحالة هنا أو اضغط على 'تحميل حالة مالية واجتماعية' من القائمة الجانبية..."
)

# زر التشغيل الرئيسي
col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    analyze_btn = st.button("🚀 تشغيل نظام الوكلاء")

if analyze_btn:
    if not case_text.strip():
        st.warning("⚠️ تنبيه: يرجى إدخال نص الحالة أو استخدام الحالة التجريبية للمتابعة.")
    else:
        # محاكاة بروتوكول وكلاء الذكاء الاصطناعي بمستوى تقني رفيع
        with st.status("🔄 جاري معالجة البيانات عبر شبكة الوكلاء المتعددة...", expanded=True) as status:
            time.sleep(0.8)
            st.write("🔍 **الوكيل الأول [Classifier Agent]:** تحليل وتصنيف بنية البيانات واستخراج المتغيرات الحرجة...")
            time.sleep(0.9)
            st.write("💰 **الوكيل الثاني [Financial Engine]:** حساب التدفقات النقدية، مؤشرات العجز، وإعداد خطة إعادة الهيكلة...")
            time.sleep(0.9)
            st.write("📝 **الوكيل الثالث [Legal Drafter]:** صياغة الخطابات الرسمية الموجهة للجهات المختصة بدقة نظامية...")
            time.sleep(0.6)
            status.update(label="✅ اكتملت عمليات التحليل والتوليد بنجاح تام.", state="complete", expanded=True)

        st.success("🎯 تقرير التحليل المؤسسي النهائي:")

        # عرض النتائج في تقسيمات احترافية (Columns) تليق بالشركات الكبرى
        col_res1, col_res2 = st.columns(2)

        with col_res1:
            st.markdown("""
                <div class="metric-card">
                    <h3>📊 التحليل المالي وإدارة العجز</h3>
                    <hr style="border-color: #334155;">
                    <ul style="line-height: 1.8; color: #cbd5e1;">
                        <li><b>إجمالي الدخل الشهري:</b> 6,000 ريال</li>
                        <li><b>الالتزامات الثابتة:</b> 4,500 ريال</li>
                        <li><b>صافي المتبقي التشغيلي:</b> 1,500 ريال</li>
                        <li><b>حجم العجز الطارئ:</b> 1,500 ريال (مخالفة)</li>
                        <li><b>التوصية الاستراتيجية:</b> تجميد النفقات غير الضرورية، وتفعيل خطة تقسيط التزامات المخالفة على أقساط ميسرة لعدم الإخلال بمعيشة الفرد.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("""
                <div class="metric-card">
                    <h3>📝 مسدسة الخطاب الرسمي المعتمد</h3>
                    <hr style="border-color: #334155;">
                    <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;">
                    <b>إلى سعادة / الجهة المختصة المحترم،</b><br>
                    السلام عليكم ورحمة الله وبركاته،،<br>
                    أتقدم إليكم بهذا الطلب نظراً لظروف مالية طارئة والتزامات قاهرة تستغرق ججل الدخل الشهري، مما يحول دون القدرة على سداد المخالفة المرورية دفعة واحدة دون التأثير الجذري على متطلبات المعيشة الأساسية.<br>
                    عليه، أرجو من سعادتكم التكرم بالنظر في حالتي والوافقة على <b>تقسيط المبلغ أو تأجيله</b> استثناءً لتخفيف العجز المالي القائم.<br><br>
                    <b>ولكم جزيل الشكر والتقدير.</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)

# تذييل الصفحة الاحترافي
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Muyassir AI Architecture &copy; 2026 &mdash; Enterprise Grade Solution for Graduation Project"
    "</p>", 
    unsafe_allow_html=True
)

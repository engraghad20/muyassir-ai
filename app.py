"""
منصة مُيسّر الذكية (Muyassir AI Platform)
نموذج أولي (Prototype) لنظام وكلاء متعددين (Multi-Agent System)
يجمع بين: الوكيل الموجّه، الوكيل المالي، والوكيل الإداري/القانوني
مبني بلغة Python باستخدام Streamlit وواجهة Anthropic Claude API الفعلية.
"""

import json
import re

import anthropic
import pandas as pd
import streamlit as st

# ==========================================================
# إعدادات عامة
# ==========================================================
MODEL_NAME = "claude-sonnet-5"   # يمكن تبديله لاحقاً بأي موديل آخر من عائلة Claude
MAX_TOKENS = 1200

DEMO_CASE = (
    "شخص راتبه 6,000 ريال، وعليه التزامات وقروض شهرية بقيمة 4,500 ريال، "
    "وتفاجأ هذا الشهر بمخالفة مرورية قيمتها 1,500 ريال لا يمكنه سدادها، "
    "ويريد كتابة خطاب رسمي لجهة حكومية لطلب تقسيط أو تأخير السداد، "
    "بالإضافة إلى خطة مالية سريعة لتخفيف العجز."
)

st.set_page_config(
    page_title="مُيسّر | Muyassir AI Platform",
    page_icon="🧭",
    layout="wide",
)

# ==========================================================
# تنسيق الواجهة (RTL + هوية بصرية دافئة)
# ==========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; }

    .stApp { direction: rtl; }
    .main .block-container { direction: rtl; text-align: right; }
    textarea, input { direction: rtl !important; text-align: right !important; }
    h1, h2, h3, h4, h5, h6, p, li, label, span { text-align: right; }

    :root {
        --brand-brown: #6B4226;
        --brand-orange: #D98324;
        --brand-cream: #FDF1E3;
    }

    .app-header {
        background: linear-gradient(135deg, var(--brand-brown) 0%, var(--brand-orange) 100%);
        padding: 26px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 22px;
    }
    .app-header h1 { color: white; margin: 0; font-size: 1.7rem; }
    .app-header p { color: #FCEFE0; margin: 6px 0 0 0; }

    .agent-card {
        background: linear-gradient(135deg, #FFFDFB 0%, var(--brand-cream) 100%);
        border-right: 5px solid var(--brand-orange);
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(107,66,38,0.08);
    }
    .agent-title {
        color: var(--brand-brown);
        font-weight: 900;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    .badge {
        display: inline-block;
        background: var(--brand-orange);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        margin-right: 6px;
    }

    .stButton>button {
        background-color: var(--brand-orange);
        color: white; font-weight: 700; border: none;
        border-radius: 8px; padding: 0.55rem 1.3rem;
    }
    .stButton>button:hover { background-color: var(--brand-brown); color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# نصوص أنظمة الوكلاء (System Prompts)
# ==========================================================
ROUTER_SYSTEM = """أنت "الوكيل الموجّه" (Router Agent) في منصة مُيسّر الذكية، وهي منصة استشارات
مجتمعية ومعيشية. مهمتك الوحيدة هي قراءة حالة المستخدم وتصنيفها لتوجيهها للوكيل المختص.

الوكلاء المتاحون:
- الوكيل المالي: للنفقات، الميزانيات، الديون، الالتزامات المالية.
- الوكيل الإداري/القانوني: لخطابات رسمية، عقود مبسطة، إجراءات حكومية/إدارية.

أجب حصراً بكائن JSON صالح دون أي نص إضافي أو علامات markdown، بالتنسيق التالي بالضبط:
{
  "classification": "مالية" أو "إدارية" أو "مركبة",
  "needs_financial_agent": true أو false,
  "needs_administrative_agent": true أو false,
  "urgency": "منخفضة" أو "متوسطة" أو "عاجلة",
  "reasoning": "شرح موجز جداً (جملة أو اثنتين) بالعربية"
}"""

FINANCIAL_SYSTEM = """أنت "الوكيل المالي" (Financial Advisor Agent) في منصة مُيسّر الذكية.
مهمتك تحليل الوضع المالي المذكور في حالة المستخدم، وتقديم خطة عملية وواقعية لتخفيف العجز
أو تحسين الوضع، دون تقديم أرقام أو نصائح غير مبنية على المعطيات المذكورة فعلياً.
لا تقدّم نفسك كمستشار مالي مرخّص، واذكر ذلك بوضوح في حقل disclaimer.

أجب حصراً بكائن JSON صالح دون أي نص إضافي أو علامات markdown، بالتنسيق التالي بالضبط:
{
  "summary": "ملخص التشخيص المالي في جملتين بالعربية",
  "monthly_income": رقم أو null إن لم يُذكر,
  "monthly_obligations": رقم أو null إن لم يُذكر,
  "extra_expense": رقم أو null إن لم يُذكر (المصروف الطارئ إن وجد),
  "net_position": رقم أو null (الفائض أو العجز الفعلي بعد كل الالتزامات),
  "recommendations": ["توصية 1", "توصية 2", "توصية 3"],
  "disclaimer": "جملة توضح أن هذه إرشادات عامة وليست استشارة مالية مرخّصة"
}"""

ADMIN_SYSTEM = """أنت "الوكيل الإداري/القانوني" (Administrative Agent) في منصة مُيسّر الذكية.
مهمتك اقتراح المسار الإجرائي الأنسب لحالة المستخدم (إلكتروني أو خطاب رسمي)، وصياغة خطاب رسمي
مبسّط بالعربية الفصحى عند الحاجة، مستخدماً أقواساً مربعة [ ] لأي بيانات ناقصة (مثل الاسم ورقم الهوية).
لا تقدّم نفسك كجهة قانونية رسمية، واذكر ذلك بوضوح في حقل disclaimer.

أجب حصراً بكائن JSON صالح دون أي نص إضافي أو علامات markdown، بالتنسيق التالي بالضبط:
{
  "summary": "ملخص الإجراء الإداري المطلوب في جملتين بالعربية",
  "recommended_channel": "المسار الأنسب (مثال: منصة إلكترونية حكومية / خطاب رسمي / كلاهما)",
  "steps": ["خطوة 1", "خطوة 2", "خطوة 3"],
  "official_letter_draft": "نص خطاب رسمي كامل بالعربية الفصحى مع أقواس [ ] للبيانات الناقصة",
  "disclaimer": "جملة توضح أن هذا مسودة عامة وليست استشارة قانونية رسمية"
}"""

# ==========================================================
# دوال مساعدة
# ==========================================================
def get_secret_api_key():
    try:
        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        return None


def extract_json(raw_text: str):
    """تنظيف استجابة النموذج واستخراج كائن JSON منها بأمان."""
    text = raw_text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return None
    return None


def call_agent(client: anthropic.Anthropic, system_prompt: str, user_message: str) -> str:
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()


def fmt_number(value):
    if value is None or value == "":
        return "غير محدد"
    try:
        return f"{float(value):,.0f} ريال"
    except Exception:
        return str(value)


# ==========================================================
# الشريط الجانبي
# ==========================================================
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")

    secret_key = get_secret_api_key()
    if secret_key:
        st.success("✅ تم العثور على مفتاح API من إعدادات النشر (Secrets)")
        api_key = secret_key
    else:
        api_key = st.text_input(
            "🔑 مفتاح Anthropic API",
            type="password",
            value=st.session_state.get("manual_api_key", ""),
            help="احصل على مفتاحك من console.anthropic.com — يُستخدم فقط أثناء هذه الجلسة ولا يُخزَّن.",
        )
        st.session_state["manual_api_key"] = api_key

    st.divider()
    if st.button("📋 تحميل حالة تجريبية", use_container_width=True):
        st.session_state["case_text"] = DEMO_CASE

    if st.button("🗑️ مسح النتائج", use_container_width=True):
        for key in ["router_result", "financial_result", "admin_result"]:
            st.session_state.pop(key, None)
        st.rerun()

    st.divider()
    st.caption("منصة مُيسّر — نموذج أولي لمشروع تخرج معسكر هندسة وكلاء الذكاء الاصطناعي")

# ==========================================================
# الرأس
# ==========================================================
st.markdown(
    """
    <div class="app-header">
        <h1>🧭 منصة مُيسّر الذكية — Muyassir AI Platform</h1>
        <p>نظام وكلاء متعددين لتقديم استشارات مالية وإدارية متكاملة عبر Claude API</p>
    </div>
    """,
    unsafe_allow_html=True,
)

case_text = st.text_area(
    "📝 صف المشكلة أو الحالة التي تريد تحليلها",
    value=st.session_state.get("case_text", ""),
    height=150,
    key="case_text",
    placeholder="مثال: راتبي لا يكفي التزاماتي الشهرية وأحتاج خطاب لتأجيل سداد قرض...",
)

run = st.button("🚀 بدء تحليل الوكلاء", use_container_width=True)

# ==========================================================
# تشغيل خط أنابيب الوكلاء (Pipeline)
# ==========================================================
if run:
    if not api_key:
        st.error("⚠️ الرجاء إدخال مفتاح Anthropic API من الشريط الجانبي أولاً.")
    elif not case_text.strip():
        st.error("⚠️ الرجاء كتابة وصف الحالة أولاً.")
    else:
        try:
            client = anthropic.Anthropic(api_key=api_key)

            with st.status("🔄 الوكيل الموجّه يحلل الحالة ويصنّفها...", expanded=False) as status:
                router_raw = call_agent(client, ROUTER_SYSTEM, case_text)
                router_json = extract_json(router_raw) or {
                    "classification": "مركبة",
                    "needs_financial_agent": True,
                    "needs_administrative_agent": True,
                    "urgency": "غير محدد",
                    "reasoning": router_raw[:200],
                }
                st.session_state["router_result"] = router_json
                status.update(label="✅ اكتمل تصنيف الوكيل الموجّه", state="complete")

            if router_json.get("needs_financial_agent"):
                with st.status("💰 الوكيل المالي يحلل الجوانب المالية...", expanded=False) as status:
                    fin_raw = call_agent(client, FINANCIAL_SYSTEM, case_text)
                    st.session_state["financial_result"] = extract_json(fin_raw) or {"summary": fin_raw}
                    status.update(label="✅ اكتمل تحليل الوكيل المالي", state="complete")
            else:
                st.session_state.pop("financial_result", None)

            if router_json.get("needs_administrative_agent"):
                with st.status("📋 الوكيل الإداري يصيغ التوصيات والخطاب...", expanded=False) as status:
                    admin_raw = call_agent(client, ADMIN_SYSTEM, case_text)
                    st.session_state["admin_result"] = extract_json(admin_raw) or {"summary": admin_raw}
                    status.update(label="✅ اكتمل عمل الوكيل الإداري", state="complete")
            else:
                st.session_state.pop("admin_result", None)

            st.success("🎯 اكتمل التحليل — التقرير النهائي جاهز أدناه")

        except anthropic.AuthenticationError:
            st.error("❌ مفتاح API غير صحيح أو منتهي الصلاحية. تحقق منه من الشريط الجانبي.")
        except Exception as exc:  # noqa: BLE001
            st.error(f"⚠️ حدث خطأ أثناء الاتصال بواجهة Claude API: {exc}")

# ==========================================================
# عرض النتائج
# ==========================================================
router_json = st.session_state.get("router_result")

if router_json:
    st.divider()
    st.markdown("## 📑 نتائج تفاعل الوكلاء")

    # --- بطاقة الوكيل الموجّه ---
    st.markdown(
        f"""
        <div class="agent-card">
            <div class="agent-title">🔄 الوكيل الموجّه (Router Agent)</div>
            <span class="badge">التصنيف: {router_json.get('classification', 'غير محدد')}</span>
            <span class="badge">الإلحاح: {router_json.get('urgency', 'غير محدد')}</span>
            <p style="margin-top:10px;">{router_json.get('reasoning', '')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- بطاقة الوكيل المالي ---
    fin = st.session_state.get("financial_result")
    if fin:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-title">💰 الوكيل المالي (Financial Advisor Agent)</div>
                <p>{fin.get('summary', '')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([1, 1.3])
        with col1:
            fin_table = pd.DataFrame(
                {
                    "البند": ["الدخل الشهري", "الالتزامات الشهرية", "مصروف طارئ", "الموقف الصافي"],
                    "القيمة": [
                        fmt_number(fin.get("monthly_income")),
                        fmt_number(fin.get("monthly_obligations")),
                        fmt_number(fin.get("extra_expense")),
                        fmt_number(fin.get("net_position")),
                    ],
                }
            )
            st.table(fin_table)
        with col2:
            st.markdown("**التوصيات:**")
            for rec in fin.get("recommendations", []):
                st.markdown(f"- {rec}")
        if fin.get("disclaimer"):
            st.caption(f"ℹ️ {fin['disclaimer']}")

    # --- بطاقة الوكيل الإداري ---
    admin = st.session_state.get("admin_result")
    if admin:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-title">📋 الوكيل الإداري/القانوني (Administrative Agent)</div>
                <p>{admin.get('summary', '')}</p>
                <span class="badge">المسار المقترح: {admin.get('recommended_channel', 'غير محدد')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if admin.get("steps"):
            st.markdown("**خطوات التنفيذ:**")
            for i, step in enumerate(admin["steps"], start=1):
                st.markdown(f"{i}. {step}")

        if admin.get("official_letter_draft"):
            st.markdown("**مسودة الخطاب الرسمي:**")
            st.text_area(
                "يمكنك نسخ النص أو تحميله",
                value=admin["official_letter_draft"],
                height=220,
                key="letter_draft_display",
            )
            st.download_button(
                "⬇️ تحميل الخطاب كملف نصي",
                data=admin["official_letter_draft"],
                file_name="خطاب_مُيسّر.txt",
                mime="text/plain",
            )
        if admin.get("disclaimer"):
            st.caption(f"ℹ️ {admin['disclaimer']}")

    # --- التقرير النهائي الموحّد ---
    st.divider()
    st.markdown("## 📊 التقرير النهائي الموحّد")

    agents_active = ["الوكيل الموجّه"]
    if fin:
        agents_active.append("الوكيل المالي")
    if admin:
        agents_active.append("الوكيل الإداري")

    report_table = pd.DataFrame(
        {
            "العنصر": ["تصنيف الحالة", "درجة الإلحاح", "الوكلاء المُفعّلون", "الموقف المالي الصافي", "المسار الإداري المقترح"],
            "التفاصيل": [
                router_json.get("classification", "—"),
                router_json.get("urgency", "—"),
                " + ".join(agents_active),
                fmt_number(fin.get("net_position")) if fin else "—",
                admin.get("recommended_channel", "—") if admin else "—",
            ],
        }
    )
    st.table(report_table)

    full_report_text = (
        f"تقرير منصة مُيسّر الذكية\n"
        f"========================\n\n"
        f"تصنيف الحالة: {router_json.get('classification', '—')}\n"
        f"درجة الإلحاح: {router_json.get('urgency', '—')}\n"
        f"سبب التصنيف: {router_json.get('reasoning', '—')}\n\n"
    )
    if fin:
        full_report_text += (
            "الوكيل المالي\n---------------\n"
            f"{fin.get('summary', '')}\n"
            f"الدخل الشهري: {fmt_number(fin.get('monthly_income'))}\n"
            f"الالتزامات الشهرية: {fmt_number(fin.get('monthly_obligations'))}\n"
            f"مصروف طارئ: {fmt_number(fin.get('extra_expense'))}\n"
            f"الموقف الصافي: {fmt_number(fin.get('net_position'))}\n"
            "التوصيات:\n" + "\n".join(f"- {r}" for r in fin.get("recommendations", [])) + "\n\n"
        )
    if admin:
        full_report_text += (
            "الوكيل الإداري/القانوني\n-------------------------\n"
            f"{admin.get('summary', '')}\n"
            f"المسار المقترح: {admin.get('recommended_channel', '')}\n"
            "الخطوات:\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(admin.get("steps", []), 1)) + "\n\n"
            "مسودة الخطاب:\n" + admin.get("official_letter_draft", "") + "\n"
        )

    st.download_button(
        "⬇️ تحميل التقرير الكامل",
        data=full_report_text,
        file_name="تقرير_مُيسّر.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.info("👆 اكتب الحالة أعلاه واضغط \"بدء تحليل الوكلاء\" لبدء التشغيل الفعلي عبر Claude API.")

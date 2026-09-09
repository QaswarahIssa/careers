import streamlit as st
import requests

st.set_page_config(page_title="اختبار تحديد المهنة السيبرانية", layout="centered")

# رابط Web App الخاص بك معتمد ومباشر
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyPaFxrAVilhOTR-61EcFICNj29jAcWUlAjmgLNEa7NnbuYLtqVYJ7pr16mbpy6UP9E/exec"

st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    .stRadio > div { text-align: right; direction: rtl; }
    div[data-testid="stMarkdownContainer"] { text-align: right; }
    </style>
""", unsafe_allow_html=True)

questions = [
    {
        "question": "مع التقنيات الجديدة، أفضل...",
        "options": {
            "اختبار الأشياء بدقة وتجربة اختراقها": "Red Team",
            "مراقبة كيفية عملها والبحث عن ميزات الأمان": "Blue Team"
        }
    },
    {
        "question": "عندما أسمع عن المخترقين في الأخبار، أقوم بـ...",
        "options": {
            "التفكير في كيفية دخول المخترقين والرغبة في التفكير مثلهم": "Red Team",
            "معرفة سبب عدم إيقاف الهجوم والتفكير في كيفية منع المهاجم مستقبلاً": "Blue Team"
        }
    },
    {
        "question": "الخيارات الأكثر ترجيحاً لشراء لعبة فيديو هي التي...",
        "options": {
            "تسمح لي بالاستكشاف، حل الألغاز، والتغلب على الخصوم": "Red Team",
            "تتضمن الاستراتيجية، اتخاذ القرارات، وبناء الأنظمة": "Blue Team"
        }
    },
    {
        "question": "توقف جهاز الكمبيوتر فجأة عن العمل، أقوم بـ...",
        "options": {
            "محاولة إعادة إنشاء المشكلة لفهم كيفية حدوث العطل": "Red Team",
            "الذهاب لسجلات النظام، التدخل لمنع انتشار المشكلة، واكتشافها مبكراً": "Blue Team"
        }
    },
    {
        "question": "عند العمل في مشروع جماعي، أقوم بـ...",
        "options": {
            "مراجعة عمل الفريق والتفكير في المشكلات المحتملة قبل حدوثها": "Red Team",
            "التأكد من تسليم المهام وتنظيم الفريق وتوفير جميع الأدوات": "Blue Team"
        }
    },
    {
        "question": "يعتقد صديقي أن بريده الإلكتروني تعرض للاختراق، أول ما أقوم به...",
        "options": {
            "محاولة اكتشاف كيفية وصول المخترق والتفكير في خطوته التالية": "Red Team",
            "التحقق من التنبيهات، تغيير كلمة المرور، وإعداد ميزات أمان إضافية": "Blue Team"
        }
    }
]

role_translations = {
    "Red Team": "مُختَبِر اختراق وهجوم سيبراني (Red Teamer / Ethical Hacker)",
    "Blue Team": "محلل أمن ومستجيب للحوادث / دفاع سيبراني (SOC Analyst / Incident Responder)"
}

st.title("🛡️ اختبار تحديد المجال السيبراني")

with st.form("quiz_form"):
    user_answers = []
    for idx, q in enumerate(questions):
        st.subheader(f"السؤال {idx + 1}: {q['question']}")
        choice = st.radio("اختر الإجابة المناسبة:", list(q["options"].keys()), key=f"q_{idx}")
        user_answers.append(q["options"][choice])
        st.write("---")

    submit_button = st.form_submit_button("عرض المهنة المقترحة وحفظ النتيجة")

if submit_button:
    red_score = user_answers.count("Red Team")
    blue_score = user_answers.count("Blue Team")
    
    top_role = "Red Team" if red_score > blue_score else "Blue Team"
    suggested_job = role_translations[top_role]

    # إرسال البيانات أوتوماتيكياً إلى Google Sheets عبر Apps Script
    payload = {
        "job_result": suggested_job,
        "answers": f"Red: {red_score}, Blue: {blue_score}"
    }
    
    try:
        response = requests.post(WEB_APP_URL, json=payload, timeout=5)
        st.balloons()
        st.success("تم حفظ إجابتك أوتوماتيكياً في شيت جوجل!")
    except Exception as e:
        st.warning("تم إظهار النتيجة، ولم نتمكن من الاتصال بالشيت تلقائياً.")

    st.markdown(f"### ✨ المجال والمهنة الأكثر ملاءمة لك هي:\n **{suggested_job}**")
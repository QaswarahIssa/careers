import streamlit as st
import requests

st.set_page_config(page_title="اختبار تحديد المهنة السيبرانية", layout="centered")

# رابط Google Apps Script الخاص بك
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyPaFxrAVilhOTR-61EcFICNj29jAcWUlAjmgLNEa7NnbuYLtqVYJ7pr16mbpy6UP9E/exec"

# ضبط الاتجاه من اليمين إلى اليسار (RTL)
st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    .stRadio > div { text-align: right; direction: rtl; }
    div[data-testid="stMarkdownContainer"] { text-align: right; }
    div.stButton > button { width: 100%; font-size: 18px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# الأسئلة الموجهة خصيصاً للمهن الست
questions = [
    {
        "question": "مع التقنيات الجديدة، أفضل...",
        "options": {
            "اختبار الأشياء بدقة وتجربة اختراقها": "Penetration Tester",
            "مراقبة كيفية عملها وتحليل التنبيهات والأمان": "Security Analyst",
            "البحث عن ميزات الأمان وتصميم أدوات الحماية": "Security Engineer",
            "التدخل السريع والتعلم فور حدوث المشكلات": "Incident Responder",
            "قراءة السجلات وفحص الملفات للتحقيق في الآثار": "Digital Forensics Examiner"
        }
    },
    {
        "question": "عندما أسمع عن المخترقين في الأخبار، أقوم بـ...",
        "options": {
            "التفكير في كيفية دخولهم واكتشاف نقاط الضعف": "Penetration Tester",
            "معرفة سبب عدم إيقاف الهجوم وتحليل الثغرات": "Security Analyst",
            "التمني لو أنني كنت هناك للسيطرة وقمع الهجوم فوراً": "Incident Responder",
            "الرغبة في محاكاة هجوم معقد واختبار جاهزية الفرق": "Red Teamer",
            "التفكير في كيفية بناء أنظمة دفاعية تمنع المهاجم مستقبلاً": "Security Engineer"
        }
    },
    {
        "question": "الخيارات الأكثر ترجيحاً لشراء لعبة فيديو هي التي...",
        "options": {
            "تتضمن حل الألغاز والغموض والبحث عن الأدلة": "Digital Forensics Examiner",
            "تتضمن التغلب على الخصوم واستكشاف الثغرات": "Penetration Tester",
            "تتضمن محاكاة هجمات استراتيجية طويلة المدى": "Red Teamer",
            "تتضمن الاستراتيجية واتخاذ القرارات لحماية القاعدة": "Security Analyst",
            "تسمح لي ببناء وتصميم الأنظمة والدفاعات": "Security Engineer"
        }
    },
    {
        "question": "توقف جهاز الكمبيوتر فجأة عن العمل، أقوم بـ...",
        "options": {
            "الذهاب مباشرة إلى سجلات النظام (Logs) لجمع الأدلة ومعرفة السبب": "Digital Forensics Examiner",
            "التدخل فوراً ومنع انتشار المشكلة للحد من الخسائر": "Incident Responder",
            "البحث عن طرق ومؤشرات لاكتشاف المشكلة مبكراً ومراقبتها": "Security Analyst",
            "إعادة بناء وتعديل برمجيات النظام لتفادي الخلل": "Security Engineer",
            "محاولة إعادة إنشاء المشكلة واستغلالها لفهم العطل": "Penetration Tester"
        }
    },
    {
        "question": "عند العمل في مشروع جماعي، أقوم بـ...",
        "options": {
            "مراجعة وتقييم النظام والتفكير في كيفية محاكاة سيناريو الفشل": "Red Teamer",
            "التأكد من سلامة الأدوات والبيانات ومراقبة سير العمل": "Security Analyst",
            "تأمين وتصميم البنية التحتية للمشروع بشكل قوي": "Security Engineer",
            "التصرف السريع وتدارك الأخطاء فور وقوعها": "Incident Responder",
            "التحقيق في الأخطاء السابقة وتوثيق الأدلة والتفاصيل": "Digital Forensics Examiner"
        }
    },
    {
        "question": "يعتقد صديقي أن بريده الإلكتروني تعرض للاختراق، أول ما أقوم به...",
        "options": {
            "محاولة اكتشاف الثغرة التي وصل من خلالها المخترق": "Penetration Tester",
            "التحقق من محاولات التسجيل والتنبيهات المشبوهة": "Security Analyst",
            "إعادة تعيين كلمة المرور وقمع الهجوم للسيطرة عليه": "Incident Responder",
            "فحص سجلات الحساب والملفات الجنائية لجمع الأدلة": "Digital Forensics Examiner",
            "إعداد ميزات وتطبيقات أمان إضافية لمنع تكرار ذلك": "Security Engineer"
        }
    }
]

# القاموس المخصص للمهن الست
role_details = {
    "Security Analyst": "محلل أمني (Security Analyst)\n* بمثابة خط الدفاع الأول؛ يقوم بمراقبة الشبكات وتحليل التنبيهات والتحقيق في الثغرات.",
    "Security Engineer": "مهندس أمني (Security Engineer)\n* يقوم بتصميم وبناء وصيانة الأنظمة الدفاعية والبرمجيات لحماية بنية الشركة التحتية.",
    "Incident Responder": "مستجيب للحوادث (Incident Responder)\n* يتولى قمع الهجمات والسيطرة عليها فور حدوثها للتقليل من الخسائر.",
    "Digital Forensics Examiner": "محلل الأدلة الجنائية الرقمية (Digital Forensics Examiner)\n* يعمل كالمحقق الرقمي؛ يبحث في السجلات لجمع الأدلة بعد وقوع الجريمة السيبرانية.",
    "Penetration Tester": "مخترق أخلاقي / فاحص اختراق (Penetration Tester)\n* يقوم باختراق الأنظمة بشكل قانوني ومصرح به لكشف نقاط الضعف قبل المخترقين الحقيقيين.",
    "Red Teamer": "عضو الفريق الأحمر (Red Teamer)\n* دور متقدم لمحاكاة هجمات معقدة وطويلة المدى لاختبار مدى كفاءة واستعداد الفرق الدفاعية بالشركة."
}

# تحديد الفريق التابع له كل تخصص
team_category = {
    "Security Analyst": "🛡️ الفريق الدفاعي (Blue Team)",
    "Security Engineer": "🛡️ الفريق الدفاعي (Blue Team)",
    "Incident Responder": "🛡️ الفريق الدفاعي (Blue Team)",
    "Digital Forensics Examiner": "🛡️ الفريق الدفاعي (Blue Team)",
    "Penetration Tester": "⚔️ الفريق الهجومي (Red Team)",
    "Red Teamer": "⚔️ الفريق الهجومي (Red Team)"
}

st.title("🛡️ اختبار تحديد المهنة السيبرانية المناسبة")
st.write("أجب عن الأسئلة التالية لاكتشاف التخصص والأدوار الأكثر ملاءمة لشخصيتك:")

with st.form("quiz_form"):
    user_answers = []
    for idx, q in enumerate(questions):
        st.subheader(f"السؤال {idx + 1}: {q['question']}")
        choice = st.radio("اختر إجابة واحدة:", list(q["options"].keys()), key=f"q_{idx}")
        user_answers.append(q["options"][choice])
        st.write("---")

    submit_button = st.form_submit_button("عرض المهنة المقترحة وحفظ النتيجة")

if submit_button:
    # حساب أعلى مهنة تكررت بناءً على الخيارات
    scores = {}
    for role in user_answers:
        scores[role] = scores.get(role, 0) + 1
    
    top_role = max(scores, key=scores.get)
    suggested_job = role_details[top_role]
    team_type = team_category[top_role]

    # إرسال البيانات إلى Google Sheets
    payload = {
        "job_result": f"{team_type} - {top_role}",
        "answers": f"النقاط المفصلة: {scores}"
    }
    
    try:
        response = requests.post(WEB_APP_URL, json=payload, timeout=5)
        st.balloons()
        st.success("تم حفظ نتيجتك أوتوماتيكياً في جدول بيانات جوجل!")
    except Exception as e:
        st.warning("تم إظهار النتيجة، وتأذر الحفظ الأوتوماتيكي في الشيت حالياً.")

    st.markdown(f"### {team_type}")
    st.markdown(f"### ✨ المهنة الأكثر ملاءمة لشخصيتك هي:\n**{suggested_job}**")

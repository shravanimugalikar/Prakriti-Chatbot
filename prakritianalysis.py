import streamlit as st
import base64

# ------------------------------------------------------
# BACKGROUND IMAGE
# ------------------------------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

add_bg_from_local("spring-floral-border-background-green-with-leaf-watercolor-illustration.jpg")

# ------------------------------------------------------
# GLOBAL STYLING
# ------------------------------------------------------
st.set_page_config(page_title="Prakriti Analysis", layout="centered")

st.markdown("""
<style>
body, p, h1, h2, h3, label, .stButton button {
    font-family: "Poppins", sans-serif;
}

/* Title and subtitles */
h1 {
    font-size: 34px !important;
    color: #1b5e20 !important;
    text-align: center;
    font-weight: 800 !important;
}
h2, .stSubheader {
    font-size: 26px !important;
    color: #2e7d32 !important;
    font-weight: 700 !important;
}
h3 {
    font-size: 22px !important;
    color: #1b5e20 !important;
    font-weight: 700 !important;
}

/* Paragraphs and radio labels */
p {
    font-size: 18px !important;
}
div[role="radiogroup"] label p {
    font-size: 18px !important;
}

/* Buttons */
.stButton>button {
    background-color: #2e7d32 !important;
    color: white !important;
    font-size: 18px !important;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
}
.stButton>button:hover {
    background-color: #1b5e20 !important;
}

/* Alert boxes */
div[data-testid="stAlertContainer"] p {
    font-size: 17px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# QUESTION BANK
# ------------------------------------------------------
CATEGORIES = {
    "Physical Features (शारीरिक वैशिष्ट्ये)": [
        ("Body Frame (शरीराचा आकार)", ["Thin, lean, underweight (बारीक, सडपातळ)", "Medium, muscular (मध्यम, स्नायूयुक्त)", "Heavy, broad (जड, भरदार)"]),
        ("Height (उंची)", ["Very tall or very short (फार उंच किंवा फार ठेंगू)", "Moderate, symmetrical (मध्यम, सममित)", "Medium to tall, proportionate (मध्यम ते उंच, प्रमाणबद्ध)"]),
        ("Hair Texture (केसांची रचना)", ["Dry, rough, thin (कोरडे, खरडे, पातळ)", "Soft, fine, reddish (मऊ, बारीक, तांबूस)", "Thick, oily, wavy (घट्ट, तेलकट, लहरदार)"]),
        ("Skin Condition (त्वचेची स्थिती)", ["Dry, cracked, rough (कोरडी, फाटलेली, खरडे)", "Warm, soft, reddish (उबदार, मऊ, तांबूस)", "Smooth, oily, cool (गुळगुळीत, तेलकट, थंड)"]),
        ("Eyes (डोळे)", ["Small, dull (लहान, फिकट)", "Medium-sized, sharp (मध्यम, तीव्र)", "Large, calm (मोठे, शांत)"]),
        ("Nails (नखं)", ["Dry, brittle (कोरडी, तुटणारी)", "Soft, pinkish (मऊ, गुलाबी)", "Strong, smooth (मजबूत, गुळगुळीत)"]),
        ("Teeth (दात)", ["Irregular, protruding (वाकडे, बाहेर आलेले)", "Medium size, yellowish (मध्यम, पिवळसर)", "Strong, white (मजबूत, पांढरे)"]),
        ("Joints (सांधे)", ["Prominent, crack easily (ठळक, चटकन आवाज येतो)", "Well-formed, flexible (सुंदर, लवचिक)", "Cushioned, stable (गादीसारखे, स्थिर)"]),
    ],
    "Physiological Functions (शारीरिक कार्ये)": [
        ("Appetite (भूक)", ["Irregular (अनियमित)", "Strong (तीव्र)", "Moderate (मध्यम)"]),
        ("Digestion (पचन)", ["Variable (बदलते)", "Strong (तीव्र)", "Slow (हळू)"]),
        ("Bowel Movements (मलविसर्जन)", ["Dry stools (कोरडे मल)", "Loose stools (सैल मल)", "Soft, regular (मऊ, नियमित)"]),
        ("Sleep Pattern (झोपेचा प्रकार)", ["Light, disturbed (हलकी, खंडित)", "Moderate (मध्यम)", "Deep, sound (गाढ, शांत)"]),
        ("Speech Style (बोलण्याची शैली)", ["Fast, unclear (जलद, अस्पष्ट)", "Sharp, clear (तीव्र, स्पष्ट)", "Slow, calm (हळू, शांत)"]),
        ("Energy Levels (ऊर्जेची पातळी)", ["Variable, fatigues easily (बदलते, लवकर थकते)", "Good stamina (चांगली सहनशक्ती)", "Stable, slow fatigue (स्थिर, हळूहळू थकते)"]),
        ("Sweating (घाम येणे)", ["Less (कमी)", "Excessive (जास्त)", "Moderate (मध्यम)"]),
    ],
    "Mental & Emotional Traits (मानसिक व भावनिक वैशिष्ट्ये)": [
        ("Mind Activity (मनाची क्रिया)", ["Restless, imaginative (चंचल, कल्पक)", "Sharp, logical (तीव्र, तर्कशुद्ध)", "Calm, steady (शांत, स्थिर)"]),
        ("Memory (स्मरणशक्ती)", ["Quick to learn, quick to forget (लवकर शिकते, लवकर विसरते)", "Sharp recall (तीव्र स्मरण)", "Slow to learn, strong memory (हळू शिकते, मजबूत स्मरण)"]),
        ("Emotional Tendencies (भावनिक प्रवृत्ती)", ["Anxiety, fear (चिंता, भीती)", "Anger, irritability (राग, चिडचिड)", "Calm, affectionate (शांत, प्रेमळ)"]),
        ("Decision-Making (निर्णय घेणे)", ["Indecisive (अनिश्चित)", "Quick (जलद)", "Firm (ठाम)"]),
        ("Work Style (कामाची शैली)", ["Multitasking, distracted (अनेक कामे, विचलित)", "Focused (एकाग्र)", "Methodical (पद्धतशीर)"]),
        ("Tolerance to Food/Weather (अन्न/हवामान सहनशीलता)", ["Low, dislikes cold (कमी, थंडी नकोशी)", "Low, dislikes heat (कमी, उष्णता नकोशी)", "High tolerance (जास्त सहनशीलता)"]),
        ("Response to Stress (तणावावर प्रतिक्रिया)", ["Easily overwhelmed, anxious (लवकर गोंधळते, चिंताग्रस्त होते)", "Reactive, irritable (प्रतिक्रियाशील, चिडचिड करते)", "Calm, composed (शांत, संयमी राहते)"]),
        ("Mood Stability (मनःस्थिती स्थिरता)", ["Unstable (अस्थिर)", "Irritable (चिडचिड)", "Stable (स्थिर)"]),
        ("Disease Resistance (रोगप्रतिकारक शक्ती)", ["Low (कमी)", "Moderate (मध्यम)", "High (जास्त)"]),
    ]
}

def classify_prakriti(answers):
    # STEP 1 — COUNT DOSHA SCORES (treated as feature likelihoods)
    scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}

    for choice in answers:
        if choice == 0:
            scores["Vata"] += 1
        elif choice == 1:
            scores["Pitta"] += 1
        elif choice == 2:
            scores["Kapha"] += 1

    total = sum(scores.values())

    # STEP 2 — TREAT SCORES AS LIKELIHOODS (Bayes-compatible)
    likelihood = {
        "Vata": scores["Vata"] / total,
        "Pitta": scores["Pitta"] / total,
        "Kapha": scores["Kapha"] / total,
    }

    # STEP 3 — PRIORS (equal, as per NB assumption)
    priors = {"Vata": 1/3, "Pitta": 1/3, "Kapha": 1/3}

    # STEP 4 — POSTERIOR COMPUTATION (Bayes Theorem)
    posterior = {
        d: priors[d] * likelihood[d]
        for d in ["Vata", "Pitta", "Kapha"]
    }

    # STEP 5 — NORMALIZE posterior → percentages
    total_post = sum(posterior.values())
    probs = {
        d: round((posterior[d] / total_post) * 100, 2)
        for d in posterior
    }

    # STEP 6 — DETERMINE DOMINANT DOSHA OR DUAL
    sorted_doshas = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    top1, top2 = sorted_doshas[0], sorted_doshas[1]

    if abs(top1[1] - top2[1]) <= 10:
        dominant = f"{top1[0]}–{top2[0]}"
    else:
        dominant = top1[0]

    return probs, dominant


# ------------------------------------------------------
# QUIZ UI
# ------------------------------------------------------
st.markdown("<h1> Prakriti Analysis (प्रकृती विश्लेषण)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:19px;'>Please select the option that best describes you.<br>जी गोष्ट तुम्हाला उत्तम प्रकारे लागू होते तो पर्याय निवडा.</p>", unsafe_allow_html=True)

if "answers" not in st.session_state:
    st.session_state.answers = [None] * sum(len(qs) for qs in CATEGORIES.values())

idx = 0
serial = 1

for category, questions in CATEGORIES.items():
    st.markdown(f"<h3>{category}</h3>", unsafe_allow_html=True)
    for q_text, options in questions:
        st.markdown(f"<p style='font-size:19px; font-weight:600;'>{serial}. {q_text}</p>", unsafe_allow_html=True)
        choice = st.radio(
            label=q_text,
            options=list(range(3)),
            format_func=lambda x, opts=options: opts[x],
            index=None,
            key=f"q_{idx}",
            label_visibility="collapsed"
        )
        st.session_state.answers[idx] = choice
        idx += 1
        serial += 1

# ------------------------------------------------------
# RESULTS
# ------------------------------------------------------
if st.button(" Show My Prakriti Results"):
    if None in st.session_state.answers:
        st.warning("Please answer all questions. (कृपया सर्व प्रश्नांची उत्तरे द्या.)")
    else:
        probs, dominant = classify_prakriti(st.session_state.answers)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>Your Prakriti Profile (आपली प्रकृती)</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#2e7d32;'>Dominant Dosha (प्रधान दोष):** {dominant}</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Vata", f"{probs['Vata']}%")
        col1.progress(probs['Vata'] / 100)
        col2.metric("Pitta", f"{probs['Pitta']}%")
        col2.progress(probs['Pitta'] / 100)
        col3.metric("Kapha", f"{probs['Kapha']}%")
        col3.progress(probs['Kapha'] / 100)

        if "–" in dominant:
            st.success(f"You have a **Dual Prakriti** type: {dominant}. You exhibit traits of both doshas in nearly equal measure.")
            st.info(f"तुमची **द्विदोष प्रकृती** आहे: {dominant}. तुम्ही दोन्ही दोषांचे गुण जवळजवळ समान प्रमाणात दर्शवता.")
        else:
            st.info(f"You have a **Single-Dominant Prakriti** type: {dominant}. This represents your core Ayurvedic constitution.")
            st.info(f"तुमची **एकदोष प्रधान प्रकृती** आहे: {dominant}. ही तुमच्या मूलभूत आयुर्वेदिक प्रकृतीचे प्रतिनिधित्व करते.")

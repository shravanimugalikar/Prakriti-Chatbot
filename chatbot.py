import streamlit as st
import os
import time  
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np
import spacy

# =====================================================
# Tech Stack
# -----------------------------------------------------
# Streamlit (UI)
# Gemini (reasoning)
# Hugging Face Transformers (text classification)
# spaCy (trait extraction)
# FAISS + Sentence-Transformers (retrieval)
# =====================================================

# ------------------------------
# Load Gemini API Key
# ------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash"

# =====================================================
#  NLP MODELS (Safe loading + auto spaCy download)
# =====================================================
@st.cache_resource
def load_nlp_models():
    # Load transformer pipeline (generic model placeholder)
    prakriti_classifier = pipeline("text-classification", model="bert-base-uncased")

    # Auto-download spaCy model if not found
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    return prakriti_classifier, nlp

prakriti_classifier, nlp = load_nlp_models()

# Safe Prakriti prediction logic (handles any model output)
def predict_prakriti(text):
    """Predict Prakriti using transformer output or fallback to rule-based."""
    try:
        preds = prakriti_classifier(text[:512])[0]  # model output
        # Handle different label counts safely
        if len(preds) == 2:
            # Sentiment-style model fallback
            scores = {
                "Vata": preds[0]["score"],
                "Pitta": preds[1]["score"],
                "Kapha": 1 - max(p["score"] for p in preds)
            }
        elif len(preds) >= 3:
            labels = ["Vata", "Pitta", "Kapha"]
            scores = {labels[i]: preds[i]["score"] for i in range(3)}
        else:
            scores = {"Vata": 0.33, "Pitta": 0.33, "Kapha": 0.34}

        prakriti = max(scores, key=scores.get)
        return prakriti, scores

    except Exception:
        # Rule-based fallback if transformer fails
        t = text.lower()
        if any(x in t for x in ["cold", "dry", "anxious", "light", "irregular"]):
            return "Vata", {"Vata": 0.9, "Pitta": 0.05, "Kapha": 0.05}
        elif any(x in t for x in ["hot", "anger", "spicy", "sweat", "acidic"]):
            return "Pitta", {"Vata": 0.05, "Pitta": 0.9, "Kapha": 0.05}
        elif any(x in t for x in ["heavy", "lazy", "slow", "oily", "sleep"]):
            return "Kapha", {"Vata": 0.05, "Pitta": 0.05, "Kapha": 0.9}
        else:
            return "Unknown", {"Vata": 0.33, "Pitta": 0.33, "Kapha": 0.34}

def extract_traits(text):
    """Extract useful entities / traits using spaCy."""
    doc = nlp(text)
    traits = [ent.text for ent in doc.ents]
    return traits

# =====================================================
# KNOWLEDGE BASE (RAG)
# =====================================================
@st.cache_resource
def load_knowledge_base(pdf_path="Comprehensive_Conversational_Prakriti_Knowledge_Base_v2.pdf"):
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    chunks = [text[i:i+800] for i in range(0, len(text), 800)]
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return chunks, index, embedder

chunks, index, embedder = load_knowledge_base()

def retrieve_context(query):
    q_emb = embedder.encode([query])
    D, I = index.search(np.array(q_emb), k=3)
    return "\n\n".join([chunks[i] for i in I[0]])

# =====================================================
#  CHATBOT LOGIC (NLP + RAG + Gemini)
# =====================================================
def chatbot_response(user_input):
    prakriti_type, prakriti_scores = predict_prakriti(user_input)
    traits = extract_traits(user_input)
    context = retrieve_context(user_input)

    # Intent detection
    text = user_input.lower()
    if any(k in text for k in ["diet", "food", "eat"]):
        intent = "diet"
    elif any(k in text for k in ["lifestyle", "routine", "daily"]):
        intent = "lifestyle"
    elif any(k in text for k in ["yoga", "exercise", "asana"]):
        intent = "yoga"
    else:
        intent = "general"

    # Build Gemini prompt
    prompt = f"""
    You are Prakriti, an Ayurvedic expert chatbot.
    Inferred Prakriti: {prakriti_type} ({prakriti_scores})
    Extracted traits: {traits}
    Intent: {intent}

    Use this Ayurvedic knowledge base context to give a personalized answer:
    {context}

    User question: {user_input}

    Respond naturally, using Ayurvedic principles.
    """

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
    ):
        if hasattr(chunk, "text") and chunk.text:
           response_text += chunk.text

    return prakriti_type, response_text

# =====================================================
# STREAMLIT UI (Fixed Input Clearing)
# =====================================================
import streamlit as st
import base64
import os
import time

st.set_page_config(page_title="Prakriti Chatbot", layout="wide")

# ---------- Local image filenames (update if different) ----------
bot_image_path = "Bot image.png"
user_image_path = "User image.png"
background_path = "Chatbot_bg.jpg"  # or "background.png"

# ---------- helper: image -> data URI ----------
def image_to_data_uri(path):
    if not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/{mime};base64,{b64}"

bot_uri = image_to_data_uri(bot_image_path)
user_uri = image_to_data_uri(user_image_path)
bg_uri = image_to_data_uri(background_path)

bg_css_url = f'url("{bg_uri}")'

# ---------- CSS ----------
st.markdown(f"""
<style>
/* full-screen background layer */
body::before {{
  content: "";
  position: fixed;
  inset: 0;
  background-image: linear-gradient(rgba(247,251,249,0.78), rgba(238,249,240,0.78)), {bg_css_url};
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: blur(0px) saturate(100%);
  z-index: -9999; /* behind everything */
  pointer-events: none;
  opacity: 1;
}}

/* Make core Streamlit containers transparent so background shows */
[data-testid="stAppViewContainer"], .stApp, .main, .block-container, .stApp>div {{
  background: transparent !important;
  box-shadow: none !important;
}}

/* Keep header transparent too */
header, .css-1v3fvcr, .css-18e3th9 {{
  background: transparent !important;
}}

/* your chat styles (unchanged, but ensured transparent where needed) */
.chat-header {{
    background: linear-gradient(90deg, #3a653a, #71ab4a);
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: white;
    font-weight: 600;
    font-size: 1.1rem;
    margin-top: -10px;
}}
.chat-header img {{
    width: 30px;
    height: 30px;
    border-radius: 50%;
}}

.chat-messages {{
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px 20px 30px 20px;
    display: flex;
    flex-direction: column;
    gap: 22px;
}}

.msg-row {{
    display: flex;
    align-items: flex-end;
    gap: 10px;
}}
.user-row {{ flex-direction: row-reverse; }}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid #71ab4a;
}}

.user-msg, .bot-msg {{
    padding: 12px 18px;
    border-radius: 20px;
    font-size: 1rem;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.user-msg {{
    background: #71ab4a;
    color: white;
    border-bottom-right-radius: 5px;
}}
.bot-msg {{
    background: #f6fff7;
    border: 1.5px solid #71ab4a;
    color: #3a653a;
    border-bottom-left-radius: 5px;
}}

form {{
    background: rgba(231,243,228,0.9);
    padding: 10px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-top: 2px solid #cde8c6;
}}
textarea {{
    resize: none;
    border: none;
    background: white;
    border-radius: 24px;
    padding: 12px 18px;
    font-size: 1rem;
    flex-grow: 1;
    height: 68px; 
}}
button {{
    background-color: #3a653a;
    color: white;
    border-radius: 50%;
    border: none;
    width: 46px;
    height: 46px;
    cursor: pointer;
    font-size: 1.3rem;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
# st.sidebar.image accepts path directly; show fallback if none
if bot_uri:
    st.sidebar.image(bot_image_path, width=200, caption="Your Ayurvedic AI Companion")
else:
    st.sidebar.markdown("**Prakriti AI**")

st.sidebar.markdown("### About Prakriti Chatbot")
st.sidebar.info("""
I'm your Ayurvedic assistant — blending **AI and Ayurveda**
to help you discover your **Prakriti (mind-body type)**  
and receive personalized diet, yoga, and lifestyle advice.
""")

# ---------- Chat state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("Prakriti AI", "Hello I'm Prakriti AI — your Ayurvedic companion. Ask me about your Prakriti, doshas, diet, or lifestyle.")
    ]
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def send_message():
    user_msg = st.session_state.user_input.strip()
    if not user_msg:
        return
    st.session_state.chat_history.append(("You", user_msg))
    st.session_state.user_input = ""
    with st.spinner("Prakriti AI is thinking..."):
        prakriti_type, response = chatbot_response(user_msg)
        time.sleep(0.6)
    st.session_state.chat_history.append(("Prakriti AI", response))

# ---------- chat container & messages ----------
st.markdown('<div class="chat-phone-container">', unsafe_allow_html=True)

# header image uses data URI if available otherwise file path (Streamlit should serve sidebar path)
header_img_src = bot_uri if bot_uri else bot_image_path
user_img_src = user_uri if user_uri else user_image_path
bot_img_src = bot_uri if bot_uri else bot_image_path

st.markdown(f"""
    <div class="chat-header">
        <img src="{header_img_src}" />
        Chat with Prakriti AI
    </div>
    <div class="chat-messages" id="chat-messages-area">
""", unsafe_allow_html=True)

for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"""
        <div class="msg-row user-row">
            <img class="avatar" src="{user_img_src}">
            <div class="user-msg">{msg}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row">
            <img class="avatar" src="{bot_img_src}">
            <div class="bot-msg">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- input form ----------
with st.form("chat_form", clear_on_submit=False):
    st.text_area("Type your message:", key="user_input",
                 placeholder="Ask about your Prakriti, diet, or yoga...",
                 label_visibility="collapsed", height=68)
    submitted = st.form_submit_button("➤", on_click=send_message)

st.markdown("</div>", unsafe_allow_html=True)





# Prakriti-Chatbot
Prakriti Chatbot is a full-stack AI-healthcare project designed to identify a user’s Prakriti (Vata, Pitta, Kapha) and offer personalized Ayurvedic recommendations. The system integrates a Retrieval-Augmented Generative (RAG) chatbot using Google Gemini, Prakriti analysis engine, and a PHP/MySQL backend for user management and doctor consultation. 

A complete AI-powered Ayurveda wellness platform that integrates:

-RAG-based Prakriti Chatbot (Gemini + FAISS + SentenceTransformer)

-Prakriti Analysis Quiz (Naive Bayes)

-Doctor Consultation (PHP + PHPMailer)

-User Login/Registration (PHP + MySQL)

-HTML/CSS responsive frontend

**Key Features:**

**1. AI-Powered Prakriti Chatbot**

-Built using Google Gemini 2.0 Flash

-Uses RAG (Retrieval-Augmented Generation) for accurate Ayurvedic answers

-Embedding model: SentenceTransformer (all-MiniLM-L6-v2)

-Vector DB: FAISS

-Detects intent: Diet, lifestyle, yoga, remedies, and Prakriti quiz request

-Natural, personalized conversations

**2. Prakriti Analysis System**

-Ayurvedic questionnaire items

-Supports Vata, Pitta, Kapha & Dual-Dosha types

-Uses scoring + Naive Bayes classification

-Results shown with progress bars + explanation

-Marathi + English support

**3. User Login & Registration**

-PHP + MySQL

-Secure password hashing

-Form validation

-User records stored in database

**4. Doctor Consultation Module**

-Appointment/consultation form

-Integrated using PHPMailer

-Sends consultation requests directly to doctor’s email

**5. Modern Clean UI**

-HTML/CSS landing page

-WhatsApp-style Streamlit chat UI


**Algorithms & Techniques Used:**

**1. Retrieval-Augmented Generation (RAG)**

-Converts PDF knowledge base into text chunks

-Generates embeddings using SentenceTransformer

-FAISS retrieves the most relevant Ayurvedic content

-Gemini uses retrieved context to produce accurate answers

**2. NLP Intent Classification**
-Detects when user asks:
"Find my Prakriti"
"I want to know my body type"

**3. Naive Bayes Based Prakriti Classification**

-Each quiz answer mapped to Vata/Pitta/Kapha

-Scores converted into percentages

-Dual-dosha detected using probability thresholds

**4. Embedding Similarity Search**

-Cosine similarity → finds closest Ayurvedic text

-Ensures answers are grounded in authentic knowledge

**5. PHPMailer SMTP Messaging**

-Sends consultation requests securely

-Handles HTML formatted email

**Tech Stack:**

**Frontend**
-HTML5, CSS3,
Streamlit (Chatbot + Quiz)

**Backend**
-Python,
PHP (Auth + Consultation),
MySQL Database

**AI & NLP**
-Google Gemini API,
FAISS Vector Store,
SentenceTransformer Embeddings,
RAG retrieval pipeline

**Tools**
-PyPDF2
dotenv,
PHPMailer,
XAMPP / Apache / MySQL


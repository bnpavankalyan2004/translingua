import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


# ==========================================
# Load API Key
# ==========================================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=API_KEY)


# ==========================================
# Automatically Find Working Model
# ==========================================
def get_model():
    try:
        models = genai.list_models()

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)

    except Exception as e:
        st.error(f"Model discovery failed:\n{e}")

    return None


model = get_model()

if model is None:
    st.error("❌ No compatible Gemini model available.")
    st.stop()


# ==========================================
# Supported Languages (25+)
# ==========================================
LANGUAGES = [
    "English", "Spanish", "French", "German", "Hindi", "Telugu",
    "Tamil", "Japanese", "Chinese", "Korean", "Arabic", "Russian",
    "Portuguese", "Italian", "Dutch", "Turkish", "Thai",
    "Vietnamese", "Indonesian", "Bengali", "Urdu",
    "Malayalam", "Kannada", "Gujarati", "Punjabi", "Marathi"
]


# ==========================================
# Translation Function
# ==========================================
def translate_text(text, source_language, target_language):

    prompt = f"""
    Translate the following text from {source_language} to {target_language}.
    Only return the translated text.

    Text:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Gemini API Error:\n{e}"


# ==========================================
# Streamlit UI
# ==========================================
def main():

    st.set_page_config(page_title="TransLingua - AI Translator")

    st.title("🌍 AI-Powered Language Translator")

    text = st.text_input("Enter text to translate:")

    col1, col2 = st.columns(2)

    with col1:
        source_language = st.selectbox("Select source language:", LANGUAGES)

    with col2:
        target_language = st.selectbox("Select target language:", LANGUAGES)

    if st.button("Translate"):

        if text.strip():

            if source_language == target_language:
                st.warning("Source and target languages cannot be the same.")
            else:
                with st.spinner("Translating..."):
                    translated_text = translate_text(
                        text,
                        source_language,
                        target_language
                    )

                st.text_area("Translated Text", translated_text, height=200)

        else:
            st.warning("Please enter text to translate.")


# ==========================================
# Run App
# ==========================================
if __name__ == "__main__":
    main()
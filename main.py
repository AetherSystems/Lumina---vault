import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 💎 LUMINA AI CONFIGURATION
st.set_page_config(page_title="Lumina AI", page_icon="💎")
st.title("💎 Lumina AI Vault")

# CONNECT THE BRAIN (GOOGLE GEMINI)
try:
    # This pulls the key from your Streamlit Secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("System Offline: Ensure GOOGLE_API_KEY is in Streamlit Secrets.")

# DOCUMENT UPLOADER
uploaded_file = st.file_uploader("Upload Revolut Receipt (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Processing Document..."):
        try:
            # Read the PDF text
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.success("Document Loaded into Vault.")
            
            # The Analysis Interface
            user_query = st.text_input("What should Lumina extract from this document?")
            
            if user_query:
                with st.spinner("Lumina is thinking..."):
                    # Send context to Gemini
                    response = model.generate_content(f"You are Lumina AI. Based on this text: {text}, answer this: {user_query}")
                    st.markdown("### Lumina Analysis:")
                    st.write(response.text)
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

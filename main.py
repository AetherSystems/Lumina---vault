import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Lumina AI Vault", page_icon="💎")

# 2. EXECUTIVE GATEKEEPER (PASSWORD)
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 AetherSystems Secure Portal")
        password = st.text_input("Enter Vault Access Code", type="password")
        if st.button("Unlock"):
            # This looks for PORTAL_PASSWORD in your Streamlit Secrets
            if password == st.secrets["PORTAL_PASSWORD"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Access Denied.")
        return False
    return True

# 3. THE VAULT (ONLY RUNS IF PASSWORD IS CORRECT)
if check_password():
    st.title("💎 Lumina AI Vault")
    st.write("Welcome, Commander.")
    
    # Connect to Google Gemini
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error("System Offline: API Key Missing.")

    # File Uploader
    uploaded_file = st.file_uploader("Upload Revolut Receipt (PDF)", type="pdf")

    if uploaded_file:
        with st.spinner("Analyzing document..."):
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.success("Document Loaded into Vault.")
            
            user_query = st.text_input("Ask Lumina about this document:")
            
            if user_query:
                with st.spinner("Lumina is thinking..."):
                    response = model.generate_content(f"Context: {text}\nQuestion: {user_query}")
                    st.markdown("### Lumina Analysis:")
                    st.write(response.text)

    # Footer Signature
    st.divider()
    st.caption("Powered by AetherSystems | Secure Data Protocol v1.0")

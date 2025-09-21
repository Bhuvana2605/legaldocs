import streamlit as st
import pdfplumber
import google.generativeai as genai

# Set your Gemini key (you can also load it from st.secrets if you want)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Smart Legal Lens (Gemini Prototype)")

uploaded_file = st.file_uploader("Upload a legal document (PDF or TXT)", type=['pdf', 'txt'])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        text = uploaded_file.read().decode(errors="replace")

    st.subheader("Contract Preview")
    st.write(text[:1000] + "...")

    st.subheader("Gemini AI Clause Simplification")
    sample_clause = text[:500]

    prompt = (
        "You are a legal assistant. Summarize the following contract clause for a non-lawyer. "
        "Also extract any parties, dates, monetary amounts, and deadlines in a small table.\n---\n"
        f"{sample_clause}\n---"
    )

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        st.success(response.text)
    except Exception as e:
        st.error(f"Error from Gemini: {e}")

    st.subheader("Sample Flowchart")
    st.markdown("""
    ```
    [Contract Start] --> [Obligation Missed?]
    [Obligation Missed?] --> [Yes: Penalty]
    [Obligation Missed?] --> [No: Continue]
    ```
    """)
else:
    st.info("Upload a PDF or TXT contract to get started!")

   

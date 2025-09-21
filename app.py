import streamlit as st
import pdfplumber
import subprocess
import sys

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    import spacy
    nlp = spacy.load("en_core_web_sm")

import openai

# For public app, use:
# openai.api_key = st.secrets["OPENAI_API_KEY"]
# For local/manual, keep your input box.
api_key = st.sidebar.text_input("OpenAI API Key (leave blank for rule-based only)", type="password")
if api_key:
    openai.api_key = api_key

st.title("Smart Legal Lens (Prototype)")


uploaded_file = st.file_uploader("Upload a legal document (PDF or TXT)", type=['pdf','txt'])

if uploaded_file:
    # Step 1: Parse document
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        text = uploaded_file.read().decode(errors="replace")
    
    st.subheader("Contract Preview")
    st.write(text[:1000])  # Preview of document

    # Step 2: Extract and display entities
    doc = nlp(text)
    st.subheader("Extracted Entities")
    ents = [(ent.label_, ent.text) for ent in doc.ents]
    if ents:
        st.table(ents)
    else:
        st.info("No named entities found in the sample text.")

    # Step 3: (Optional) Ask OpenAI to simplify a sample paragraph/section
    st.subheader("AI Clause Simplification")
    sample_clause = text[:500]  # Take first 500 chars as a demo clause
    if api_key:
        prompt = f"Explain the following legal contract clause in simple terms for a non-lawyer:\n---\n{sample_clause}\n---"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Use gpt-4/gpt-3.5-turbo-16k if available for your account
                prompt=prompt,
                max_tokens=150,
                temperature=0.5,
            )
            st.success(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error from OpenAI: {e}")
    else:
        st.write("Add your OpenAI API key in the sidebar for clause simplification.")

    # Step 4: Static demo flowchart (SVG/Markdown, for visual touch)
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



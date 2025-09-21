import streamlit as st
import pdfplumber
import openai

st.title("Smart Legal Lens (Prototype)")

# For Streamlit Cloud deployment, the API key is set in st.secrets!
openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload a legal document (PDF or TXT)", type=['pdf', 'txt'])

if uploaded_file:
    # Step 1: Parse document
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        text = uploaded_file.read().decode(errors="replace")
    
    st.subheader("Contract Preview")
    st.write(text[:1000] + "...")  # Preview first 1000 characters

    # Step 2: AI Clause Simplification
    st.subheader("AI Clause Simplification")
    sample_clause = text[:500]  # Take first 500 chars as a demo clause

    prompt = (
        "You are a legal assistant. Summarize the following contract clause for a non-lawyer. "
        "Also extract any parties, dates, monetary amounts, and deadlines in a small table.\n---\n"
        f"{sample_clause}\n---"
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or "gpt-3.5-turbo-instruct"
            prompt=prompt,
            max_tokens=250,
            temperature=0.2,
        )
        st.success(response.choices[0].text.strip())
    except Exception as e:
        st.error(f"Error from OpenAI: {e}")

    # Step 3: Static demo flowchart (simple Markdown)
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

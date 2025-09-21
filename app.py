import streamlit as st
import pdfplumber
import google.generativeai as genai

# Configure Gemini with your API key (in Streamlit secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Smart Legal Lens - AI Contract Analyzer")

uploaded_file = st.file_uploader("Upload contract (PDF or TXT)", type=['pdf','txt'])
if uploaded_file:
    # Extract contract text
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        text = uploaded_file.read().decode(errors="replace")

    st.subheader("Contract Preview")
    st.write(text[:1000] + "...")

    # Gemini: Overall contract summary in plain English
    st.subheader("📄 Contract Summary (AI-generated)")
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        prompt_summary = (
            "Summarize the following contract in plain, simple English for a non-lawyer. "
            "Highlight key topics and obligations in general, but keep the summary concise:\n\n" + text[:1500]
        )
        summary_result = model.generate_content(prompt_summary)
        st.write(summary_result.text)
    except Exception as e:
        st.error(f"Gemini error (summary): {e}")

    # Clause highlighting/classification
    st.subheader("📝 Key Clauses & Types (AI-extracted)")
    try:
        prompt_clauses = (
            "List all important clauses in the following contract. For each, output:\n"
            "1. Clause type (e.g. Payment, Termination, Penalty, Confidentiality, etc.)\n"
            "2. The full clause text (one sentence short version)\n"
            "3. Why it is important (one line)\n"
            "Present your answer as a Markdown table: |Type|Short Text|Why Important|. Use no extra commentary.\n"
            "Contract:\n" + text[:2000]
        )
        result = model.generate_content(prompt_clauses)
        st.markdown(result.text)
    except Exception as e:
        st.error(f"Gemini error (clauses): {e}")

    # Flowchart/logic extraction
    st.subheader("🔄 Contract If-Then Flow (AI-generated)")
    try:
        prompt_flowchart = (
            "Read the following contract excerpt. Summarize the 'if this, then that' logic as a simple flowchart "
            "in Markdown code block using node arrows (->) style. Make it clear and short. "
            "Omit any extra commentary, just output the flowchart.\n\n"
            + text[:1500]
        )
        result_flow = model.generate_content(prompt_flowchart)
        st.markdown(result_flow.text)
    except Exception as e:
        st.error(f"Gemini error (flowchart): {e}")

else:
    st.info("Upload a PDF or TXT contract to get started!")

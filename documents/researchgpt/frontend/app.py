import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ResearchGPT", page_icon="📄")

st.title("📄 ResearchGPT")
st.caption("Upload a document and ask questions about it — answered by a local AI, with sources.")

# ---- Upload section ----
st.header("1. Upload a document")
uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file is not None:
    if st.button("Process Document"):
        with st.spinner("Processing document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Processed {uploaded_file.name} — {data['chunks_created']} chunks created.")
        else:
            st.error("Failed to process document.")

# ---- Question section ----
st.header("2. Ask a question")
question = st.text_input("Type your question about the document")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please type a question first.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(f"{API_URL}/query", data={"question": question})

        if response.status_code == 200:
            data = response.json()
            st.subheader("Answer")
            st.write(data["answer"])

            with st.expander("View source chunks used"):
                for i, source in enumerate(data["sources"]):
                    st.markdown(f"**Source {i+1}:**")
                    st.text(source)
        else:
            st.error("Failed to get an answer. Did you upload a document first?")
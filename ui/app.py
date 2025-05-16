
import streamlit as st
import json
from app.orchestrator import orchestrate

st.set_page_config(layout="wide", page_title="NexTurn RAG Platform")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Equinor_logo.svg/320px-Equinor_logo.svg.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>NexTurn RAG Assistant</h1>", unsafe_allow_html=True)
with col3:
    st.image("https://i.imgur.com/bXjzKZg.png", width=100)  # Placeholder NexTurn logo

st.markdown("### Ask your enterprise documents (PDF or CSV)")

with open("vector_db/metadata.json") as f:
    metadata = json.load(f)

source_keys = list(metadata.keys())
selected_key = st.selectbox("📄 Select a document source:", source_keys)
query = st.text_input("💬 Enter your question:")

if query and selected_key:
    with st.spinner("🔍 Thinking..."):
        answer = orchestrate(query, selected_key)
        st.success("✅ Answer")
        st.write(answer)

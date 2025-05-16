
import streamlit as st
import json
from app.orchestrator import orchestrate
import os
st.set_page_config(layout="wide", page_title="NexTurn RAG Platform")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("logo/equinor.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>NexTurn RAG Assistant</h1>", unsafe_allow_html=True)
with col3:
    st.image("logo/nexturn.png", width=100)  # Placeholder NexTurn logo

st.markdown("### Ask your documents")

# with open("vector_db/metadata.json") as f:
#     metadata = json.load(f)

# source_keys = list(metadata.keys())
# selected_key = st.selectbox("📄 Select a document source:", source_keys)
# Initialize session state
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# st.markdown("### 🗂️ Conversation History")
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**NexTurn Assistant:** {chat['assistant']}")
    if "sources" in chat:
        with st.expander("🔎 Sources used"):
            for src in chat["sources"]:
                if src["type"] == "figure" and src.get("image_path"):
                    img_name = os.path.basename(src["image_path"])
                    st.markdown(f'''
                    <div style="position:relative; margin-bottom: 10px;">
                        <strong>Figure</strong> (Page {src["page"]}): {src["snippet"]}
                        <div style="display:none; position:absolute; z-index:10; background:white; border:1px solid #ccc; padding:5px;" class="hover-image">
                            <img src="/static/{img_name}" width="300"/>
                        </div>
                    </div>
                    <script>
                    const blocks = window.parent.document.querySelectorAll('.element-container div[style*="position:relative"]');
                    blocks.forEach(block => {{
                        const hover = block.querySelector('.hover-image');
                        block.addEventListener('mouseover', () => hover.style.display = 'block');
                        block.addEventListener('mouseout', () => hover.style.display = 'none');
                    }});
                    </script>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f"- **{src['type'].capitalize()}** (Page {src['page']}): {src['snippet']}")
    st.markdown("---")

st.markdown("### 💬 Ask Your Question")
with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_input("Your question", key="chat_input")
    submitted = st.form_submit_button("Send")

if submitted and query:
    with st.spinner("🤖 Thinking..."):
        answer, sources = orchestrate(query)
    st.session_state.chat_history.append({
        "user": query,
        "assistant": answer,
        "sources": sources
    })
    st.rerun()
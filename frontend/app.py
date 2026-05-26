import streamlit as st
import requests


# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="AstraRAG-X",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------- CUSTOM CSS ----------

st.markdown(
    """
    <style>

    /* Main App */

    .stApp {
        background-color: #f5f7fb;
        color: #111827;
    }

    /* Main Layout */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-left: 4rem;
        padding-right: 4rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Header */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .sub-title {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 32px;
    }

    /* Chat Cards */

    .user-card {
        background-color: #2563eb;
        color: white;
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 16px;
        line-height: 1.7;
    }

    .assistant-card {
        background-color: white;
        color: #111827;
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        line-height: 1.7;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    /* Labels */

    .card-label {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* Chat Input */

    .stChatInputContainer {
        border-top: 1px solid #e5e7eb;
        background-color: #f5f7fb;
    }

    textarea {
        font-size: 16px !important;
    }

    /* Buttons */

    .stButton button {
        background-color: #111827;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        transition: 0.2s ease;
    }

    .stButton button:hover {
        background-color: #1f2937;
    }

    /* Divider */

    hr {
        border-color: #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------- HEADER ----------

st.markdown(
    '<div class="main-title">AstraRAG-X</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Agentic AI Research Assistant</div>',
    unsafe_allow_html=True
)


# ---------- SIDEBAR ----------

with st.sidebar:

    st.title("Workspace")

    api_url = st.text_input(
        "Backend URL",
        value="http://127.0.0.1:8000"
    )

    st.divider()

    st.subheader("Capabilities")

    st.markdown("""
    - Hybrid Retrieval  
    - Conversational Memory  
    - Streaming Responses  
    - LangGraph Workflows  
    - Multi-Agent Routing  
    - Research Workflows  
    """)

    st.divider()

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    if uploaded_file:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:

            response = requests.post(
                f"{api_url}/upload-pdf",
                files=files
            )

            if response.status_code == 200:

                st.success(
                    "PDF uploaded successfully."
                )

            else:

                st.error(
                    "Upload failed."
                )

        except Exception as error:

            st.error(
                f"Error: {error}"
            )

    st.divider()

    if st.button("Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# ---------- SESSION STATE ----------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------- CHAT HISTORY ----------

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-card">
                <div class="card-label">
                    User
                </div>

                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-card">
                <div class="card-label">
                    AstraRAG-X
                </div>

                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------- USER INPUT ----------

user_query = st.chat_input(
    "Ask AstraRAG-X..."
)


# ---------- RESPONSE FLOW ----------

if user_query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    st.markdown(
        f"""
        <div class="user-card">
            <div class="card-label">
                User
            </div>

            {user_query}
        </div>
        """,
        unsafe_allow_html=True
    )

    assistant_placeholder = st.empty()
    status_placeholder = st.empty()

    full_response = ""

    try:

        status_placeholder.info(
            "Routing query..."
        )

        response = requests.get(
            f"{api_url}/chat",
            params={
                "query": user_query
            }
        )

        data = response.json()
        status_placeholder.info(
            "Retrieving knowledge..."
        )

        full_response = data["answer"]

        sources = data["sources"]

        status_placeholder.info(
            "Generating response..."
        )

        # Assistant Response
        assistant_placeholder.markdown(
            f"""
            <div class="assistant-card">
                <div class="card-label">
                    AstraRAG-X
                </div>

                {full_response}
            </div>
            """,
            unsafe_allow_html=True
        )

        status_placeholder.success(
            "Response generated"
        )

        # Source Cards
        if sources:
            with st.expander("View Sources"):

                for index, source in enumerate(
                    sources,
                    start=1
                ):

                    st.markdown(
                        f"""
                        <div style="
                            background-color: white;
                            padding: 14px;
                            border-radius: 14px;
                            border: 1px solid #e5e7eb;
                            margin-bottom: 12px;
                            font-size: 14px;
                            line-height: 1.6;
                        ">

                        <strong>Source {index}</strong>

                        <br><br>

                        <strong>Document:</strong>
                        {source["document"]}

                        <br>

                        <strong>Page:</strong>
                        {source["page"]}

                        <br><br>

                        <strong>Preview:</strong><br>
                        {source["preview"][:180]}...

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as error:

        full_response = f"Error: {error}"

        assistant_placeholder.error(
            full_response
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
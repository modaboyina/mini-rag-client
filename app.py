# import streamlit as st
# import os
# import time
# from rag import build_index, Searcher, INDEX_PATH, CHUNKS_PATH, MODEL_NAME, DATA_DIR

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Mini-RAG Document Q&A",
#     page_icon="📚",
#     layout="wide"
# )

# st.title("📚 Mini-RAG: Query Your Documents")
# st.markdown("This app allows you to ask questions about your PDF documents using a local retrieval system.")

# # --- State Management ---
# if 'searcher' not in st.session_state:
#     st.session_state.searcher = None
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# # --- Helper Functions ---
# @st.cache_resource
# def load_searcher():
#     """Loads the searcher object, building the index if necessary."""
#     if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
#         with st.spinner(f"No index found. Building index from PDFs in `{DATA_DIR}`... This may take a moment."):
#             if not build_index():
#                 st.error("Failed to build the index. Please check the console for errors.")
#                 return None
#             st.success("Index built successfully!")
    
#     with st.spinner("Loading the search engine..."):
#         searcher = Searcher(MODEL_NAME, INDEX_PATH, CHUNKS_PATH)
#     return searcher

# # --- Main App Logic ---

# # Initialize the searcher
# if st.session_state.searcher is None:
#     st.session_state.searcher = load_searcher()

# if st.session_state.searcher is None:
#     st.warning(f"Please add PDF files to the '{DATA_DIR}' directory and restart the app.")
# else:
#     # Display chat messages from history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Accept user input
#     if prompt := st.chat_input("Ask a question about your documents"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Display assistant response in chat message container
#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             with st.spinner("Searching for relevant passages..."):
#                 results = st.session_state.searcher.search(prompt, k=3)
            
#             response = ""
#             if not results:
#                 response = "Sorry, I couldn't find any relevant passages in your documents to answer that question."
#                 message_placeholder.markdown(response)
#             else:
#                 response_parts = ["Here are the top 3 most relevant passages I found:\n"]
#                 for i, res in enumerate(results):
#                     response_parts.append(
#                         f"""
#                         ---
#                         **Result {i+1} | Score: {res['score']:.2f}**
#                         *   **Source:** `{res['doc_id']}`, Page: `{res['page']}`
#                         *   **Text:** *"{res['text']}"*
#                         """
#                     )
#                 response = "\n".join(response_parts)
#                 message_placeholder.markdown(response)

#         # Add assistant response to chat history
#         st.session_state.messages.append({"role": "assistant", "content": response})

####################################### to see all upload files #########################


# import streamlit as st
# import os
# import time
# import shutil  # NEW: For deleting the old index directory
# from rag import build_index, Searcher, INDEX_PATH, CHUNKS_PATH, MODEL_NAME, DATA_DIR

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Mini-RAG Document Q&A",
#     page_icon="📚",
#     layout="wide"
# )

# # --- State Management ---
# if 'searcher' not in st.session_state:
#     st.session_state.searcher = None
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# # --- Helper Functions ---
# @st.cache_resource
# def load_searcher():
#     """
#     Loads the searcher object. This function is cached by Streamlit, so it will
#     only run once unless the cache is cleared.
#     """
#     # Check if the index exists. If not, build it.
#     if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
#         with st.spinner(f"No index found. Building index from PDFs in `{DATA_DIR}`... This may take a moment."):
#             # Ensure the data directory exists before trying to build
#             if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
#                  st.warning(f"The '{DATA_DIR}' directory is empty. Please upload PDF files using the sidebar.")
#                  return None
            
#             if not build_index():
#                 st.error("Failed to build the index. Please check the console for errors.")
#                 return None
#             st.success("Index built successfully!")
    
#     # If the index exists, load the searcher
#     with st.spinner("Loading the search engine..."):
#         try:
#             searcher = Searcher(MODEL_NAME, INDEX_PATH, CHUNKS_PATH)
#             return searcher
#         except Exception as e:
#             st.error(f"Failed to load the search engine: {e}")
#             st.error("The index might be corrupted. Try deleting the 'index' folder and reprocessing files.")
#             return None

# # --- Sidebar for File Management (NEW) ---
# with st.sidebar:
#     st.title("📄 Document Management")
#     st.markdown("Upload your PDF files here and process them to update the knowledge base.")

#     # Ensure the data directory exists
#     os.makedirs(DATA_DIR, exist_ok=True)

#     uploaded_files = st.file_uploader(
#         "Upload PDF files",
#         type="pdf",
#         accept_multiple_files=True,
#         label_visibility="collapsed"
#     )

#     if st.button("Process Uploaded Files", use_container_width=True):
#         if uploaded_files:
#             # Save uploaded files to the data directory
#             for file in uploaded_files:
#                 save_path = os.path.join(DATA_DIR, file.name)
#                 with open(save_path, "wb") as f:
#                     f.write(file.getbuffer())
#             st.success(f"Successfully saved {len(uploaded_files)} file(s)!")

#             # Invalidate the old index by deleting it
#             index_dir = os.path.dirname(INDEX_PATH)
#             if os.path.exists(index_dir):
#                 with st.spinner("Deleting old index..."):
#                     shutil.rmtree(index_dir)
#                 st.info("Old index removed.")

#             # Clear the cached searcher and rerun the app to trigger a rebuild
#             st.cache_resource.clear()
#             st.session_state.searcher = None
#             st.rerun()
#         else:
#             st.warning("No files uploaded. Please upload at least one PDF.")

#     # Display current files in the data directory
#     with st.expander("View Current Documents"):
#         try:
#             files = os.listdir(DATA_DIR)
#             if files:
#                 for file in files:
#                     st.info(file)
#             else:
#                 st.write("No documents found.")
#         except FileNotFoundError:
#             st.write("No documents found.")


# # --- Main App Logic ---
# st.title("📚 Mini-RAG: Query Your Documents")
# st.markdown("This app allows you to ask questions about your PDF documents using a local retrieval system.")

# # Initialize the searcher
# if st.session_state.searcher is None:
#     st.session_state.searcher = load_searcher()

# if st.session_state.searcher is None:
#     st.info(f"Please upload PDF files to the '{DATA_DIR}' directory using the sidebar and click 'Process'.")
# else:
#     # Display chat messages from history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             # This will render the beautified output from history
#             if isinstance(message["content"], list):
#                 for res in message["content"]:
#                     with st.container(border=True):
#                         st.markdown(f"**Source:** `{res['doc_id']}` | **Page:** `{res['page']}`")
#                         with st.expander(f"**Score: {res['score']:.2f}** - Click to see text"):
#                             st.write(res['text'])
#             else:
#                 st.markdown(message["content"])

#     # Accept user input
#     if prompt := st.chat_input("Ask a question about your documents"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Display user message
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Display assistant response
#         with st.chat_message("assistant"):
#             with st.spinner("Searching for relevant passages..."):
#                 results = st.session_state.searcher.search(prompt, k=3)
            
#             if not results:
#                 response_text = "Sorry, I couldn't find any relevant passages in your documents to answer that question."
#                 st.markdown(response_text)
#                 st.session_state.messages.append({"role": "assistant", "content": response_text})
#             else:
#                 # NEW: Beautified output using containers and expanders
#                 for res in results:
#                     with st.container(border=True):
#                         st.markdown(f"**Source:** `{res['doc_id']}` | **Page:** `{res['page']}`")
#                         with st.expander(f"**Score: {res['score']:.2f}** - Click to see text"):
#                             st.write(res['text'])
                
#                 # Save the structured results to history for correct re-rendering
#                 st.session_state.messages.append({"role": "assistant", "content": results})


############################# for upload and delete files #########################################
import streamlit as st
import os
import shutil
from rag import build_index, Searcher, INDEX_PATH, CHUNKS_PATH, MODEL_NAME, DATA_DIR

# --- Page Configuration ---
st.set_page_config(
    page_title="Mini-RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

# --- State Management ---
if 'searcher' not in st.session_state:
    st.session_state.searcher = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Helper Functions ---

# NEW: Helper function to trigger a rebuild of the index
def trigger_rebuild():
    """Deletes the old index, clears caches, and reruns the app to force a rebuild."""
    index_dir = os.path.dirname(INDEX_PATH)
    if os.path.exists(index_dir):
        with st.spinner("Removing old index..."):
            shutil.rmtree(index_dir)
    
    # Clear Streamlit's cache and session state for the searcher
    st.cache_resource.clear()
    st.session_state.searcher = None
    st.rerun()

@st.cache_resource
def load_searcher():
    """
    Loads the searcher object. This function is cached by Streamlit, so it will
    only run once unless the cache is cleared.
    """
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        with st.spinner(f"No index found. Building index from PDFs in `{DATA_DIR}`... This may take a moment."):
            if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
                 st.warning(f"The '{DATA_DIR}' directory is empty. Please upload PDF files to get started.")
                 return None
            
            if not build_index():
                st.error("Failed to build the index. Please check the console for errors.")
                return None
            st.success("Index built successfully!")
    
    with st.spinner("Loading the search engine..."):
        try:
            searcher = Searcher(MODEL_NAME, INDEX_PATH, CHUNKS_PATH)
            return searcher
        except Exception as e:
            st.error(f"Failed to load the search engine: {e}")
            st.error("The index might be corrupted. Try deleting files and reprocessing.")
            return None

# --- Sidebar for File Management (MODIFIED) ---
with st.sidebar:
    st.title("📄 Document Management & Settings") # Title changed
    st.markdown("Upload, manage documents, and adjust settings.")

    # NEW: Add a settings container with the threshold slider
    with st.container(border=True):
        st.subheader("Search Settings")
        score_threshold = st.slider(
            "Minimum Score Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.3, # Default value
            step=0.05,
            help="Filters out results with a similarity score below this value."
        )

    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Section for uploading files
    with st.container(border=True):
        st.subheader("Upload New Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if st.button("Process Uploaded Files", use_container_width=True, type="primary"):
            if uploaded_files:
                for file in uploaded_files:
                    save_path = os.path.join(DATA_DIR, file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                st.success(f"Successfully saved {len(uploaded_files)} file(s)!")
                trigger_rebuild()
            else:
                st.warning("No files uploaded. Please select at least one PDF.")

    # Section for managing existing files (MODIFIED)
    with st.container(border=True):
        st.subheader("Manage Existing Documents")
        try:
            files = os.listdir(DATA_DIR)
            if not files:
                st.info("No documents found in the data directory.")
            else:
                for file in files:
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.text(file)
                    with col2:
                        # Use the file name as a unique key for the button
                        if st.button("Delete", key=f"delete_{file}", use_container_width=True):
                            file_path = os.path.join(DATA_DIR, file)
                            os.remove(file_path)
                            st.success(f"Deleted `{file}`.")
                            trigger_rebuild()
                
                # Add a button to delete all files
                if st.button("Delete All Documents", use_container_width=True):
                    for file in files:
                        os.remove(os.path.join(DATA_DIR, file))
                    st.success("All documents have been deleted.")
                    trigger_rebuild()

        except FileNotFoundError:
            st.info("The data directory does not exist yet.")


# --- Main App Logic ---
st.title("📚 Mini-RAG: Query Your Documents")
st.markdown("This app allows you to ask questions about your PDF documents using a local retrieval system.")

if st.session_state.searcher is None:
    st.session_state.searcher = load_searcher()

if st.session_state.searcher is None:
    st.info(f"Please upload PDF files using the sidebar and click 'Process' to begin.")
else:
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], list):
                for res in message["content"]:
                    with st.container(border=True):
                        st.markdown(f"**Source:** `{res['doc_id']}` | **Page:** `{res['page']}`")
                        with st.expander(f"**Score: {res['score']:.2f}** - Click to see text"):
                            st.write(res['text'])
            else:
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching for relevant passages..."):
               results = st.session_state.searcher.search(prompt, k=3, score_threshold=score_threshold)
            
            if not results:
                response_text = "Sorry, I couldn't find any relevant passages to answer that question."
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                for res in results:
                    with st.container(border=True):
                        st.markdown(f"**Source:** `{res['doc_id']}` | **Page:** `{res['page']}`")
                        with st.expander(f"**Score: {res['score']:.2f}** - Click to see text"):
                            st.write(res['text'])
                
                st.session_state.messages.append({"role": "assistant", "content": results})
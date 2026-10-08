import streamlit as st
import requests


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Hybrid RAG System",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# FastAPI URL
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📚 Hybrid RAG System")

st.write(
    "Upload a document, process it, and ask questions "
    "from the document using RAG."
)


# --------------------------------------------------
# Sidebar - Document Processing
# --------------------------------------------------

st.sidebar.header("📄 Document Processing")


uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


# --------------------------------------------------
# Process Document
# --------------------------------------------------

if uploaded_file is not None:

    st.sidebar.success(
        f"File selected: {uploaded_file.name}"
    )

    if st.sidebar.button("Process Document"):

        # ------------------------------------------
        # Step 1: Upload PDF
        # ------------------------------------------

        with st.spinner("Uploading document..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            upload_response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        if upload_response.status_code != 200:

            st.error(
                f"Upload failed: {upload_response.text}"
            )

        else:

            st.success("✅ Document uploaded successfully")


            # --------------------------------------
            # Step 2: Convert PDF to Markdown
            # --------------------------------------

            with st.spinner(
                "Converting PDF to Markdown..."
            ):

                uploaded_file.seek(0)

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                markdown_response = requests.post(
                    f"{API_URL}/convert-to-markdown",
                    files=files
                )

            if markdown_response.status_code != 200:

                st.error(
                    f"Markdown conversion failed: "
                    f"{markdown_response.text}"
                )

            else:

                markdown_data = markdown_response.json()

                st.success(
                    "✅ PDF converted to Markdown"
                )


                # ----------------------------------
                # Show Markdown
                # ----------------------------------

                with st.expander(
                    "👀 View Markdown"
                ):

                    st.markdown(
                        markdown_data["markdown"]
                    )


                # ----------------------------------
                # Step 3: Create Chunks
                # ----------------------------------

                markdown_text = markdown_data["markdown"]

                markdown_filename = (
                    markdown_data["markdown_filename"]
                )

                with st.spinner(
                    "Creating chunks and embeddings..."
                ):

                    files = {
                        "file": (
                            markdown_filename,
                            markdown_text.encode("utf-8"),
                            "text/markdown"
                        )
                    }

                    chunk_response = requests.post(
                        f"{API_URL}/create-chunks",
                        files=files
                    )

                if chunk_response.status_code != 200:

                    st.error(
                        f"Chunk creation failed: "
                        f"{chunk_response.text}"
                    )

                else:

                    chunk_data = chunk_response.json()

                    st.success(
                        "✅ Chunks and embeddings created"
                    )

                    st.info(
                        f"Total chunks: "
                        f"{chunk_data['total_chunks']}"
                    )


                    # ------------------------------
                    # Show Chunks
                    # ------------------------------

                    with st.expander(
                        "🧩 View Chunks"
                    ):

                        for i, chunk in enumerate(
                            chunk_data["chunks"]
                        ):

                            st.markdown(
                                f"### Chunk {i + 1}"
                            )

                            st.write(chunk)

                            st.divider()


# --------------------------------------------------
# Question Answering Section
# --------------------------------------------------

st.divider()

st.header("💬 Ask a Question")


query = st.text_input(
    "Enter your question",
    placeholder="Example: What is the leave policy?"
)


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

if st.button("🔍 Ask Question"):

    if not query:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            response = requests.post(
                f"{API_URL}/query",
                params={
                    "query": query
                }
            )

        if response.status_code != 200:

            st.error(
                f"Query failed: {response.text}"
            )

        else:

            data = response.json()


            # --------------------------------------
            # Display Answer
            # --------------------------------------

            st.subheader("🤖 Answer")

            st.write(
                data["answer"]
            )


            # --------------------------------------
            # Display Retrieved Chunks
            # --------------------------------------

            st.subheader(
                "📖 Retrieved Context"
            )

            retrieved_chunks = data[
                "retrieved_chunks"
            ]

            for i, chunk in enumerate(
                retrieved_chunks
            ):

                with st.expander(
                    f"Retrieved Chunk {i + 1}"
                ):

                    st.write(chunk)
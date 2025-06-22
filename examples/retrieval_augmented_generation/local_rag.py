import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFacePipeline
from langchain_text_splitters import CharacterTextSplitter

# --- Load environment variables ---
load_dotenv()

MODEL_NAME = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3.1-405B-Instruct")
RAG_DIRECTORY = os.getenv("DIRECTORY", "meeting_notes")

# --- Helpers ---


@st.cache_resource
def get_local_llm():
    """Load the local or endpoint HuggingFace LLM."""
    # Uncomment to run fully local (requires large resources!)
    # return HuggingFacePipeline.from_model_id(
    #     model_id=MODEL_NAME,
    #     task="text-generation",
    #     pipeline_kwargs={
    #         "max_new_tokens": 1024,
    #         "top_k": 50,
    #         "temperature": 0.4,
    #     }
    # )
    return HuggingFaceEndpoint(
        repo_id=MODEL_NAME,
        task="text-generation",
        max_new_tokens=1024,
        do_sample=False,
    )


@st.cache_resource
def load_documents(directory):
    """Load and split documents from the specified directory."""
    if not os.path.exists(directory) or not os.path.isdir(directory):
        st.error(f"Directory '{directory}' not found. Please check the DIRECTORY environment variable.")
        return []
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


@st.cache_resource
def get_chroma_instance(directory):
    """Create a Chroma vector store from documents in the directory."""
    docs = load_documents(directory)
    if not docs:
        return None
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(docs, embedding_function)


def query_documents(question, db):
    """
    Query the Chroma vector store for documents relevant to the question.
    Returns a list of formatted strings.
    """
    if db is None:
        return ["No document database loaded."]
    similar_docs = db.similarity_search(question, k=5)
    if not similar_docs:
        return ["No similar documents found."]
    return [f"Source: {doc.metadata.get('source', 'N/A')}\nContent: {doc.page_content}" for doc in similar_docs]


def prompt_ai(messages, db, llm):
    """
    Build a prompt that includes the most relevant document context, and ask the model to answer.
    """
    user_prompt = messages[-1].content
    retrieved_context = query_documents(user_prompt, db)
    formatted_context = "\n\n".join(retrieved_context)
    formatted_prompt = f"Context for answering the question:\n{formatted_context}\n\n" f"Question/user input:\n{user_prompt}"
    doc_chatbot = ChatHuggingFace(llm=llm)
    ai_response = doc_chatbot.invoke(messages[:-1] + [HumanMessage(content=formatted_prompt)])
    return ai_response


# --- Streamlit UI ---


def main():
    st.title("Chat with Local Documents (RAG Agent)")

    # Load LLM and database
    llm = get_local_llm()
    db = get_chroma_instance(RAG_DIRECTORY)

    # System prompt sets the persona and constraints of the agent
    system_prompt = (
        "You are a personal assistant who answers questions based on the context provided. "
        "If the context does not sufficiently answer the user's question, say you don't know. "
        f"The current date is: {datetime.now().date()}."
    )

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=system_prompt)]

    # Display chat history
    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])

    # User input
    prompt = st.chat_input("What questions do you have about your documents?")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Get assistant response
        with st.chat_message("assistant"):
            ai_response = prompt_ai(st.session_state.messages, db, llm)
            st.markdown(ai_response.content)
        st.session_state.messages.append(ai_response)


if __name__ == "__main__":
    main()

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from utils import *
from prompts import SUMMARY_PROMPT
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Split transcript into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create vector database
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize the LLM (Language Model)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("YouTube AI Assistant")


video_url = st.text_input("Enter Youtube URL")

if st.button("Analyze"):
    try:
        # Extract video information
        video_id = extract_video_id(video_url)
        title = get_video_title    (video_id)
        transcript = get_transcript(video_id)

        st.header(title)

        # Create and run summary chain
        prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
        chain = prompt | llm
        summary = chain.invoke({"transcript": transcript})

        st.subheader("Summary")
        st.write(summary.content)

        # Split transcript into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = splitter.create_documents([transcript])

        # Create embeddings and vector store
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = FAISS.from_documents(docs, embedding)
        retriever = vectorstore.as_retriever()

        # Create QA chain
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant answering questions about a YouTube video. Use the provided context to answer questions accurately."),
            ("human", "Context from the video:\n\n{context}\n\nQuestion: {question}")
        ])
        qa_chain = qa_prompt | llm

        # Store in session state
        st.session_state["retriever"] = retriever
        st.session_state["qa_chain"] = qa_chain
        st.session_state["chat_history"] = []
        
        st.success("Video analyzed! Now ask questions below.")

    except Exception as e:
        st.error(f"Error analyzing video: {str(e)}")

# Q&A Section
if "qa_chain" in st.session_state:
    st.divider()
    question = st.text_input("Ask anything about the video")

    if st.button("Ask"):
        try:
            retriever = st.session_state["retriever"]
            qa_chain = st.session_state["qa_chain"]
            
            # Find relevant context
            relevant_docs = retriever.invoke(question)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            print(context)
            
            # Get answer from LLM
            response = qa_chain.invoke({
                "context": context,
                "question": question
            })
            
            st.write(response.content)
            
            # Save to history
            st.session_state["chat_history"].append({
                "question": question,
                "answer": response.content
            })
            
        except Exception as e:
            st.error(f"Error getting answer: {str(e)}")
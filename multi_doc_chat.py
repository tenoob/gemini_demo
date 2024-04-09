# gemini chatbot working on multi doc's
#Facebook AI Similarity Search (Faiss) 

import streamlit as st
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS,Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts.prompt import PromptTemplate

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdfs):
    """
    read the pfds and return the texts in each of the pages
    """
    text = ""
    for pdf in pdfs:
        read_pdf = PdfReader(pdf)
        for page in read_pdf.pages:
            text+=page.extract_text()
    return text

def get_chunks_from_text(text):
    """
    divide the text into chunks
    """
    text_splitter  = RecursiveCharacterTextSplitter(
        chunk_size = 8000, chunk_overlap = 800
    )
    chunks = text_splitter.create_documents(text)
    return chunks

def get_vector_store_from_chunks(chunks):
    """
    get vector store from the chunks using goggleembeddings
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors_store = FAISS.from_documents(chunks,embeddings)
    vectors_store.save_local("faiss_index")

def convosational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context","question"]
    )

    chain = load_qa_chain(model,chain_type="stuff")
    return chain

def ui_input(question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(question)
    chain = convosational_chain()
    response = chain(
        {"input_documents":docs,"question":question},
        return_only_outputs=True
    )
    print(response)
    st.write("Reply: ",response["output_text"])

def main():
    st.set_page_config("Multi Doc Chat")
    st.header("Gemini Chatbot")

    question = st.text_input("Ask Que related to pdf files")

    if question:
        ui_input(question=question)

    with st.sidebar:
        st.title("Menu:")
        docs = st.file_uploader("Upload PDF files",accept_multiple_files=True)
        if st.button("Submit "):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(docs)
                text_chunks = get_chunks_from_text(raw_text)
                get_vector_store_from_chunks(text_chunks)
                st.success("Done")


if __name__=="__main__":
    main()









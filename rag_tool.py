import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

file_path = "data/10050-medicare-and-you_0.pdf"

async def data_loader(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)

    return pages

def configure_embedding_model():
    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embedding_model

async def split_into_chunks(file_path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    pages = await data_loader(file_path)
    chunks = text_splitter.split_documents(pages)
    
    return chunks

def get_retriever(query):
    chunks = asyncio.run(split_into_chunks(file_path))
    embedding_model = configure_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": 3})

    return retriever.invoke(query)

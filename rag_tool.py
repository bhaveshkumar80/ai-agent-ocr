import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

file_path = "data/10050-medicare-and-you_0.pdf"

# Load data
async def data_loader(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)

    return pages

# Configure a embedding model
def configure_embedding_model():
    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embedding_model

# Split data into managable chunks
async def split_into_chunks(file_path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    pages = await data_loader(file_path)
    chunks = text_splitter.split_documents(pages)
    
    return chunks

#Store vector locally
def store_vector_embeddings():
    embeddings = configure_embedding_model()
    chunks = asyncio.run(split_into_chunks(file_path))

    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vector_store.save_local("faiss_medical_docs")

    print("Data Successfully Stored!")
    return vector_store

# Create a retriever
def get_retriever(query):
 
    embedding_model = configure_embedding_model()
    vectorstore = FAISS.load_local("faiss_medical_docs", embeddings=embedding_model, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": 1})

    response = retriever.invoke(query)

    info = ""
    for res in response:
        info = info + res.page_content + "\n\n"

    return info


store_vector_embeddings()

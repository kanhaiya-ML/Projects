import os
print(f"Starting on port: {os.environ.get('PORT', 10000)}")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile,File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import state
from agents import agent_executor
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Request(BaseModel):
    question:str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    with open("temp.pdf","wb") as f:
        f.write(await file.read())

    pdf_loader = PyPDFLoader("temp.pdf")
    pages = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstores = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./pdf_chromaDb"
    )

    state.pdf_uploaded = True
    state.pdf_retriever = vectorstores.as_retriever(search_kwargs={"k":3})
    return {"message":"Documents Uploaded"}

@app.post("/ask")
def ask(request:Request):
    if state.pdf_uploaded:
        result = agent_executor.invoke({"input":request.question})
        return {"answer":result["output"]}
    else:
        result = agent_executor.invoke({"input": request.question})
        return {"answer": result["output"]}
    
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)






    
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
import os

from langchain_core.prompts import PromptTemplate




os.environ['HF_HOME'] = "./hf_cache"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

vectorstore = FAISS.load_local("vector_store", embeddings,allow_dangerous_deserialization=True)

llm= LlamaCpp(
    model_path=r"G:\model\tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
    temperature = 0.7,
    max_tokens = 512,
    top_p=0.9,
    n_ctx=2048,
    verbose=False
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful legal assistant. Use the following context to answer the question clearly and concisely.

Context: {context}
Question: {question}

Only give the **final answer** in one or two sentences. Do not label or repeat the question or the word 'Answer'. Just reply with the direct, helpful response.
"""
)

from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)




query="What is section 302 of IPC?"
response = qa_chain.invoke(query)

print("Answer:" ,response['result'])

for i,doc in enumerate(response['source_documents']):
    print(f"\nSource {i+1} : \n{doc.page_content}")


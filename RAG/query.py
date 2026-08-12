import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS

# Load env
load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')


# Load embedding model

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS database

vector_db = FAISS.load_local(
    'faiss_index',
    embeddings,
    allow_dangerous_deserialization=True
)


# Load LLM

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.3,
    max_new_tokens=512
)

chat_model = ChatHuggingFace(llm=llm)

# Query

question = input('Ask a question : ')


# Retrieve relevant chunks

documents = vector_db.similarity_search(
    question,
    k=5
)

# Build context

context = '\n\n'.join(
    document.page_content
    for document in documents
)


# Prompt


prompt = f"""
You are a helpful document assistant.

Answer the question using only the
information provided in the context.

If the answer cannot be found in the
context, say that you don't know.

Context:
----------------
{context}
----------------

Question:
{question}
"""

# Generate Answer

response = chat_model.invoke(prompt)

print("\nAnswer:")
print(response.content)
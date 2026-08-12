import pymupdf

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Read PDF

document = pymupdf.open('sample.pdf')

text = ''
for page in document:
    text += page.get_text()

document.close()


# Split Text

splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
chunks = splitter.create_documents([text])

print(f'Create {len(chunks)} chunks')


# Create Embeddings

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)


# Storing in FAISS

vector_db = FAISS.from_documents(
    chunks,
    embeddings
)


# Save vectore database

vector_db.save_local('faiss_index')
print('Vector database created successfullly')

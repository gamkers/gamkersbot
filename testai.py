import fitz  # PyMuPDF
import requests
from io import BytesIO
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyMuPDFLoader, CSVLoader, UnstructuredImageLoader

from langchain_community.vectorstores import FAISS
def extract_text_from_pdf_url(pdf_url):
    try:
        # Download the PDF file
        response = requests.get(pdf_url)
        response.raise_for_status()  # Check if the request was successful

        # Open the PDF from the downloaded content
        pdf_document = fitz.open(stream=BytesIO(response.content), filetype="pdf")
        text = ""

        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
pdf_url = "https://docs.aws.amazon.com/pdfs/AmazonS3/latest/userguide/s3-userguide.pdf"
extracted_text = extract_text_from_pdf_url(pdf_url)

from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 256,
    chunk_overlap  = 20
)
docs = text_splitter.create_documents([extracted_text])
print(docs)

from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
documents = [Document(page_content=chunk) for chunk in chunks]
embeddings = embedding_model.embed_documents(docs)
print(embeddings)


# Initialize the vector store and add embeddings
vector_store = FAISS.from_documents(docs, embedding_model)

# Save the vector store locally
vector_store.save_local("example_index")

# Load the vector store
vector_store = FAISS.load_local("example_index", embedding_model, allow_dangerous_deserialization=True)

def answer_question(question, vector_store, embedding_model):

    question_embedding = embedding_model.embed_query(question)
    # Perform similarity search using the vector store
    results = vector_store.similarity_search(question, top_k=3)
    return results

question = "What is the main topic of the document?"
answers = answer_question(question, vector_store, embedding_model)

print("Top 3 most relevant chunks for the question:")
for i, answer in enumerate(answers):
    print(f"Chunk {i+1}: {answer.page_content}")




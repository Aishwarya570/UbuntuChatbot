import os
import numpy as np
from markdown_it import MarkdownIt
import tiktoken
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document
from config import DATA_PATH, FAISS_FOLDER, EMBEDDING_MODEL
from tqdm import tqdm
# Initialize tokenizer for chunking
tokenizer = tiktoken.get_encoding("cl100k_base")
import logging
import time
logging.basicConfig()
logger = logging.getLogger('Embedder')
logger.setLevel(logging.INFO)

def count_tokens(text):
    """Returns the number of tokens in a text string."""
    return len(tokenizer.encode(text))

def chunk_text(text, max_tokens=512, overlap=50):
    """
    Splits text into smaller chunks based on token count.
    Uses a sliding window approach with overlap.
    """
    sentences = text.split(". ")
    chunks, current_chunk = [], []

    for sentence in sentences:
        if count_tokens(" ".join(current_chunk) + sentence) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:]  # Maintain overlap
        current_chunk.append(sentence)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def extract_markdown_sections(markdown_text):
    """
    Extracts sections from Markdown using headings as dividers.
    """
    parser = MarkdownIt()
    tokens = parser.parse(markdown_text)
    
    sections, current_section = [], []
    for token in tokens:
        if token.type.startswith("heading") and current_section:
            sections.append("\n".join(current_section))
            current_section = []
        if token.content:
            current_section.append(token.content)
    
    if current_section:
        sections.append("\n".join(current_section))

    return sections

def load_markdown_files(root_folder):
    """Recursively loads Markdown files and applies chunking."""
    docs = []
    
    for folder, _, files in os.walk(root_folder):  # Recursively traverse subfolders
        for file in files:
            logger.debug(f"File is {file}")
            if file.endswith(".md"):
                file_path = os.path.join(folder, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    sections = extract_markdown_sections(content)
                    for section in tqdm(sections):
                        chunks = chunk_text(section)
                        logger.debug(f'Chunks size: {len(chunks)}')
                        docs.extend([
                            Document(page_content=chunk, metadata={"source": file_path}) 
                            for chunk in chunks
                        ])
    
    return docs

def create_faiss_index():
    """Generates FAISS embeddings using LangChain and stores them in the specified folder."""
    docs = load_markdown_files(DATA_PATH)
    logger.info(f'Created file chunks')
    if not docs:
        logger.error("No Markdown files found!")
        return
    
    # Use BAAI/bge-large-en embeddings
    if EMBEDDING_MODEL in ['dunzhang/stella_en_400M_v5', 'jxm/cde-small-v2', 'infgrad/stella-base-en-v2', 'nomic-ai/nomic-embed-text-v1']:
        embeddings = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True).cuda()
        # embeddings.half()
    else:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Create FAISS index
    logger.info(f'Creating FAISS index')
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    logger.info(f'Successfully created vector database...')
    # Save FAISS index
    out_dir = os.path.join(FAISS_FOLDER, os.path.basename(EMBEDDING_MODEL))
    os.makedirs(out_dir, exist_ok=True)
    vectorstore.save_local(out_dir)
    logger.info(f"{len(docs)} chunks embedded and stored in {FAISS_FOLDER}!")

if __name__ == "__main__":
    st_time = time.time()
    create_faiss_index()
    end_time = time.time()
    logger.info(f'Time taken to create and save vector database: {end_time-st_time}')

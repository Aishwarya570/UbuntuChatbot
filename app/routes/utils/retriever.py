import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import FAISS_FOLDER, EMBEDDING_MODEL
import logging
logging.basicConfig()
logger = logging.getLogger('Retriever')
logger.setLevel(logging.DEBUG)
class Retriever:
    def __init__(self):
        """Loads the FAISS index from the correct folder."""
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        faiss_path = os.path.join(FAISS_FOLDER, os.path.basename(EMBEDDING_MODEL))  # Ensure correct path
        self.vectorstore = FAISS.load_local(faiss_path, self.embeddings, allow_dangerous_deserialization=True)

    def search(self, query, top_k=8):
        
        """Search FAISS for the most relevant Markdown content."""
        logger.info(f'Finding {top_k} similar search docs to query: {query}')
        docs = self.vectorstore.similarity_search(query, k=top_k)
        # print(f"Here is the docs  {docs}")
        return "\n\n".join([doc.page_content for doc in docs])

if __name__ == "__main__":
    retriever = Retriever()
    query = "Tell me about Snaps in Ubuntu Core?"
    results = retriever.search(query)
    print("Relevant Sections:\n", results)

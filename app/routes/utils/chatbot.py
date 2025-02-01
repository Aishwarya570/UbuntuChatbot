import os
from retriever import Retriever
from generator import Generator

class Chatbot:
    def __init__(self):
        """Initializes the retriever and generator."""
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, query):
        """Retrieves context and generates a response."""
        context = self.retriever.search(query, top_k=8)
        return self.generator.generate(query, context)

if __name__ == "__main__":
    bot = Chatbot()
    query = input("Ask a question: ")
    answer = bot.ask(query)
    answer = answer.dict()
    print(answer["content"])
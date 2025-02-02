import os
from retriever import Retriever
from generator import Generator


class Chatbot:
    def __init__(self):
        """Initializes the retriever and generator."""
        self.retriever = Retriever()
        self.generator = Generator()
        self.chat_history = []  # Stores previous Q&A for context

    def ask_in_api(self, query):
        """Retrieves context and generates a streamed response."""
        history_context = "\n\n".join(self.chat_history[-3:]) if self.chat_history else ""
        context = self.retriever.search(query)

        if history_context:
            context = f"{history_context}\n\n{context}"  # Add previous chat history
        
        response = ""
        for chunk in self.generator.generate(query, context):
            yield chunk  # Yield each chunk for streaming
            response += chunk

        self.chat_history.append(f"Q: {query}\nA: {response}")  # Store Q&A history


    def ask_in_terminal(self, query):
        """Retrieves context and generates a response with streaming."""
        # Append chat history to maintain conversation
        history_context = "\n\n".join(self.chat_history[-3:]) if self.chat_history else ""
        context = self.retriever.search(query)

        if history_context:
            context = f"{history_context}\n\n{context}"  # Add previous conversation

        print("\nAI: ", end="", flush=True)
        response = ""
        for chunk in self.generator.generate(query, context):
            print(chunk, end="", flush=True)  # Stream response
            response += chunk

        print("\n")  # New line after response completes
        self.chat_history.append(f"Q: {query}\nA: {response}")  # Store Q&A

    def chat_loop(self):
        """Runs a continuous chat loop with follow-up prompting."""
        print("\nUbuntu Docs Chatbot - Type 'exit' to stop\n")
        
        while True:
            query = input("You: ")
            if query.lower() in ["exit", "quit", "bye"]:
                print("\Bye!")
                break

            self.ask_in_terminal(query)

            # Ask if the user wants to continue
            while True:
                follow_up = input("\nDo you want to continue? (yes/no): ").strip().lower()
                if follow_up in ["yes", "y"]:
                    break  # Continue the conversation
                elif follow_up in ["no", "n", "exit", "quit", "bye"]:
                    print("\nBye!")
                    return  # Exit the loop and end conversation
                else:
                    print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    bot = Chatbot()
    bot.chat_loop()

    
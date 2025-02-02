from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

class Generator:
    def __init__(self):
        """Initializes the LLM model using LangChain."""
        self.llm = ChatOpenAI(model_name=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base = "https://api.mistral.ai/v1")

    def generate(self, query, context):
        """Generates a response using the retrieved Markdown documentation context."""
        prompt_v1 = (
            "You are an AI assistant answering questions based on technical Markdown documentation, "
            "specifically related to Ubuntu.\n"
            "Use the provided context to generate a concise and accurate answer.\n\n"
            "### Context:\n"
            f"{context}\n\n"
            "### Question:\n"
            f"{query}\n\n"
            "### Answer:"
        )
        prompt_v2 = (
                "You are an AI assistant answering questions based on technical Markdown documentation, "
                "specifically related to Ubuntu.\n\n"
                "Use the provided context to generate a concise and accurate answer.\n\n"
            
                "### Context:\n"
                f"{context}\n\n"

                "### Instructions:\n"
                "- Read the provided context carefully.\n"
                "- Respond with precise and relevant information.\n"
                "- If the context includes commands, format them properly using Markdown syntax.\n"
                "- Use bullet points for listing steps or key details.\n\n"

                "### Example Format:\n"
                
                "**Steps:**\n"
                "1. Open the terminal.\n"
                "2. Run the above command to update packages.\n"
                "3. Verify updates have been applied successfully.\n\n"

                "### Question:\n"
                f"{query}\n\n"

                "### Answer:"
            ) 
        
        
        for chunk in self.llm.stream(prompt_v2):
            if chunk.content:
                yield chunk.content
        

if __name__ == "__main__":
    generator = Generator()
    query = "How do I install a package using apt in Ubuntu?"
    context = "To install a package using `apt` in Ubuntu, use the command: `sudo apt install <package-name>`."
    for text in generator.generate(query, context):
        print(text, end = "", flush = True)

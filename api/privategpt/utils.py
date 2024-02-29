import threading
from langchain_openai import AzureChatOpenAI
from config.config import (OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION, 
                            OPENAI_DEPLOYMENT_NAME, OPENAI_API_TYPE, OPENAI_MODEL_NAME                           )
from langchain.schema import HumanMessage
from handlers.ChainStreamHandler import ChainStreamHandler
from utils.ThreadedGenerator import ThreadedGenerator

def llm_thread_privategpt(g, prompt):
    """
    A function to run the language model in a separate thread.

    Args:
        g (ThreadedGenerator): ThreadedGenerator instance for token generation.
        prompt (str): Prompt for the language model.

    """
    try:
        # Initialize AzureChatOpenAI instance for interaction with OpenAI model
        chat = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            openai_api_version=OPENAI_API_VERSION,
            deployment_name=OPENAI_DEPLOYMENT_NAME,
            openai_api_key=OPENAI_API_KEY,
            openai_api_type=OPENAI_API_TYPE,
            model_name=OPENAI_MODEL_NAME,
            streaming=True,
            callbacks=[ChainStreamHandler(g)],  # Set ChainStreamHandler as callback
            temperature=0)
        
        # Pass the prompt to the language model
        chat([HumanMessage(content=prompt)])
    finally:
        # Close the generator after use
        g.close()
        
def private_gpt_chain(prompt):
    """
    Start a new thread to generate tokens.

    Args:
        prompt (str): Prompt for the language model.

    Returns:
        ThreadedGenerator: ThreadedGenerator instance for token generation.

    """
    g = ThreadedGenerator()  # Initialize ThreadedGenerator
    # Start a new thread to run llm_thread_privategpt function
    threading.Thread(target=llm_thread_privategpt, args=(g, prompt)).start()
    return g  # Return the ThreadedGenerator instance

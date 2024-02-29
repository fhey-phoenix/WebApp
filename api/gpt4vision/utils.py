import threading
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from config.config import (OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION, 
                            OPENAI_DEPLOYMENT_NAME, OPENAI_API_TYPE, OPENAI_MODEL_NAME,
                            ANSWER_PROMPT, SEARCH_SERVICE_ADMIN_KEY, SEARCH_SERVICE_ENPOINT,
                            AZURE_SEARCH_INDEX_NAME, 
                            OPENAI_EMBEDDING_DEPLOYMENT_NAME, DOCUMENT_PROMPT)
from handlers.ChainStreamHandler import ChainStreamHandler
from utils.ThreadedGenerator import ThreadedGenerator
from langchain_core.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate,
                                         SystemMessagePromptTemplate)
from langchain.vectorstores import AzureSearch 
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


def llm_thread_gpt4vision(g, prompt, img_b64):
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
            deployment_name="gpt-4-vision-deployment",
            openai_api_key=OPENAI_API_KEY,
            openai_api_type=OPENAI_API_TYPE,
            model_name="gpt-4-vision-preview",
            streaming=True,
            callbacks=[ChainStreamHandler(g)],  # Set ChainStreamHandler as callback
            temperature=0,
            max_tokens=512)
        
        # Define system and human message prompts
        chat.invoke(
                                [
                                    HumanMessage(
                                        content=[
                                            {
                                                "type": "text", 
                                                "text": prompt
                                            },
                                            {
                                                "type": "image_url",
                                                "image_url": 
                                                {
                                                    "url": f"data:image/jpeg;base64,{img_b64}",
                                                    "detail": "auto"
                                                }
                                            },
                                        ]
                                    )
                                ]
                            )
    finally:
        # Close the generator after use
        g.close()
        

def gpt4vision(prompt, img64):
    """
    Start a new thread to generate tokens.

    Args:
        prompt (str): Prompt for the language model.

    Returns:
        ThreadedGenerator: ThreadedGenerator instance for token generation.

    """
    g = ThreadedGenerator()  # Initialize ThreadedGenerator
    # Start a new thread to run llm_thread_privategpt function
    threading.Thread(target=llm_thread_gpt4vision, args=(g, prompt, img64)).start()
    return g  # Return the ThreadedGenerator instance

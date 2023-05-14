from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent
from langchain.agents import AgentType


class ChatBot:
    def __init__(self, memory, agent_chain):
        self.memory = memory
        self.agent = agent_chain


def create_chatbot(model_name, seed_memory=None):
    search = DuckDuckGoSearchRun()
    tools = [
        Tool(
            name="Current Search",
            func=search.run,
            description="useful for all question that asks about live events",
        ),
        Tool(
            name="Topic Search",
            func=search.run,
            description="useful for all question that are related to a particular topic, product, concept, or service",
        )
    ]
    memory = seed_memory if seed_memory is not None else ConversationBufferMemory(memory_key="chat_history")
    chat = ChatOpenAI(temperature=0, model_name=model_name)
    agent_chain = initialize_agent(tools, chat, agent="conversational-react-description", verbose=True, memory=memory)

    return ChatBot(memory, agent_chain)
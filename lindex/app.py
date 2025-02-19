import os
import logging
import sys
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

api_key = os.getenv("API-KEY")
azure_endpoint = "https://apimeuw1.azure-api.net/sa-works-oai-1/"
api_version = "2024-10-21"

llm = AzureOpenAI(
    model="gpt-4o",
    deployment_name="saworks-gpt4o",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="saworks-ada2",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)


# from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model


# Create vectors directory if it doesn't exist
PERSIST_DIR = "./vectors"
if not os.path.exists(PERSIST_DIR):
    os.makedirs(PERSIST_DIR)

# Check if we have an existing index
if os.path.exists(os.path.join(PERSIST_DIR, "index.json")):
    # Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
else:
    # Create a new index
    documents = SimpleDirectoryReader("data/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Persist the index to disk
    index.storage_context.persist(persist_dir=PERSIST_DIR)

query = "What is this ebook about and two example questions + answers?"
query_engine = index.as_query_engine()
answer = query_engine.query(query)

print(answer.get_formatted_sources())
print("query was:", query)
print("answer was:", answer)

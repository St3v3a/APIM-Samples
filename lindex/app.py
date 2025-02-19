import os
import logging
import sys
import shutil
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
azure_endpoint = os.getenv("AZURE-APIM-URL")
api_version = os.getenv("API-VERSION")

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

Settings.llm = llm
Settings.embed_model = embed_model

# Create vectors directory if it doesn't exist
PERSIST_DIR = "./vectors"
if not os.path.exists(PERSIST_DIR):
    os.makedirs(PERSIST_DIR)

def initialize_index():
    # Ask user if they want to remove existing vectors
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        while True:
            response = input("Do you want to remove existing vector storage? (yes/no): ").lower()
            if response in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'")
        
        if response == 'yes':
            print("Removing existing vector storage...")
            shutil.rmtree(PERSIST_DIR)
            os.makedirs(PERSIST_DIR)
            return create_new_index()
    
    # Check if we have an existing index
    if os.path.exists(os.path.join(PERSIST_DIR, "index.json")):
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)
    else:
        return create_new_index()

def create_new_index():
    print("Creating new index from data...")
    documents = SimpleDirectoryReader("data/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Persist the index to disk
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index

def main():
    try:
        index = initialize_index()
        query_engine = index.as_query_engine()
        
        print("\nWelcome to the Local Index Search Application!")
        print("Enter your questions below. Press Ctrl+C to exit.")
        print("-" * 50)
        
        while True:
            try:
                query = input("\nEnter your question: ")
                if not query.strip():
                    print("Please enter a valid question.")
                    continue
                    
                answer = query_engine.query(query)
                print("\nSources:")
                print(answer.get_formatted_sources())
                print("\nAnswer:")
                print(answer)
                print("-" * 50)
                
            except Exception as e:
                print(f"Error processing question: {str(e)}")
                
    except KeyboardInterrupt:
        print("\n\nExiting application. Thank you for using Local Index Search!")
        sys.exit(0)

if __name__ == "__main__":
    main()

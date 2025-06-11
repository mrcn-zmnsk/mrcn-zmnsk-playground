import dotenv
import datasets
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader


def get_vector_store(path:str = './chroma_db', model_id:str = 'text-embedding-3-large') -> Chroma:
    """Initialize and return a Chroma vector store of TripAdvisor locations, with OpenAI embeddings."""
    
    print(f'Loading vector store from path: {path} with model: {model_id}')

    dotenv.load_dotenv()    
    vector_store = Chroma(
        collection_name = 'tripadvisor',
        embedding_function = OpenAIEmbeddings(model=model_id),
        persist_directory = path
    )
    
    documentCount = len(vector_store.get()['documents'])
    if documentCount == 0:
        print('No documents found in vector store')
        load_vector_store(vector_store)

    documentCount = len(vector_store.get()['documents'])        

    print(f'Loaded vector store with: {documentCount} documents')
    return vector_store


def load_vector_store(vector_store: Chroma): 
    
    hf_dataset_name = "itinerai/us_places"
    print(f'Loading vector store with TripAdvisor locations from HF: {hf_dataset_name}...')
    dataset = datasets.load_dataset(hf_dataset_name, split="train")
    
    for i, record in enumerate(dataset):
        name = record['NAME'].replace('/','').replace('"','')
        details = record['DESCRIPTION']

        page = f"""Name: {name}
Destination: {record['DESTINATION']}
URL: {record['URL']}
Categories: {",".join(details['categories'] or [])}
Description: {details['description']}
Rating: {record['RATING']}"""
    
        with open(f"data/{name}.txt", "w", encoding='utf8') as f:
            f.write(page)

    loader = DirectoryLoader(
        path="data",
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf8'}
    )

    documents = loader.load()
    vector_store.add_documents(documents)
    

    
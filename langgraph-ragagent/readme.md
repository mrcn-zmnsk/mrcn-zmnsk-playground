# langgraph-ragagent

A playground project for experimenting with Retrieval-Augmented Generation (RAG) agents using [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain).

Project take-aways:
- Function Calling optimized model like `gpt-4o` makes dramatic impact on agent's performance
- Learned semantic-search pipeline of encoding embeddings, vector database and similarity search
- Very good experience with LangGraph and LangFuse

## Features

- **OpenAI gpt-4o** model
- **Web Search Tool** based on SerpAPI
- **RAG Tool:** Semantic search in ChromaDB. TripAdvisor locations dataset (HF: [itinerai/us_places](https://huggingface.co/datasets/itinerai/us_places/viewer)) encoded with OpenAI `text-embedding-3-large`
- **LangGraph** for agent flow control
- **LangFuse** for observability
- **Streaming** agent output chunks

## High-level design

![LG RAG Design](../docs/LG%20RAG.png)

## Use

### Install dependencies:
```sh
pip install -r requirements.txt
```

### Configure environment variables
Create a `.env` file in the src folder with your API keys for OpenAI, SerpAPI and Langfuse:
```
OPENAI_API_KEY=
SERPAPI_API_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_HOST=
```

### Run

Run the agent script:

```sh
python src/app.py --prompt "I am going on a trip to France. We're considering to visit a museum. Can you recommend something?"
```

## Results 

### Execution example

```
Loading vector store from path: ./chroma_db with model: text-embedding-3-large
Loaded vector store with: 2662 documents

Executing agent for prompt: I am going on a trip to France. We're considering to visit a museum. Can you recommend something?

================================== Ai Message ==================================
Tool Calls:
  tripadvisor_tool (call_pTRHZGVHteShQFLWeiPIvo2A)
 Call ID: call_pTRHZGVHteShQFLWeiPIvo2A
  Args:
    query: museum in France
================================= Tool Message =================================
Name: tripadvisor_tool

Name: International Art Museum of America
Destination: San Francisco   <-- ⚠️ Our dataset is limitted to US locations
URL: https://www.tripadvisor.com/Attraction_Review-g60713-d2203953-Reviews-International_Art_Museum_of_America-San_Francisco_California.html   
Categories: Art Museums
Description: Since its founding in 2011, the International Art Museum...
Rating: 4.0

... ⚠️ 4 more examples cut out for brevity

================================== Ai Message ==================================

It seems there was a mix-up with the search results, as they are showing museums in San Francisco instead of France. Let me correct that and find some museums in France for you.   <-- ⚠️ Model reasons great although can improve system prompt to never call tool 2x with identical query
Tool Calls:
  tripadvisor_tool (call_cSRC5UjDldKzqtU0Pbf5PDKW)
 Call ID: call_cSRC5UjDldKzqtU0Pbf5PDKW
  Args:
    query: museum in France
================================= Tool Message =================================
Name: tripadvisor_tool

<⚠️same result as above, cut off for brevity>

================================== Ai Message ==================================
Tool Calls:
  websearch_tool (call_0jtD3VXvh0BmSak0UP2Jp9Vb)
 Call ID: call_0jtD3VXvh0BmSak0UP2Jp9Vb
  Args:
    query: top museums to visit in France  <-- ⚠️ Model uses the 2nd tool available - websearch
================================= Tool Message =================================
Name: websearch_tool

[
    {
        "title": "Louvre Museum", 
        "description": "Open", 
        "rating": 4.7, 
        "reviews": 344000, 
        "price": "$25.16", 
        ...
    },
    ... ⚠️ cut off for brevity
]
================================== Ai Message ==================================

Here are some top museums to visit in France:

1. **Louvre Museum**
   - Rating: 4.7
   - Reviews: 344,000
   - Price: $25.16
   - ![Louvre Museum](https://serpapi.com/searches/68497650f357f69e97e22486/images/dee45fc4fa9323e00729d973147a260e244f6183a30fb8edb9a8906f0f6c54a3.jpeg)

2. **Musée d'Orsay**
   - Rating: 4.8
   - Reviews: 103,000
   - Price: $18.30
   - ![Musée d'Orsay](https://serpapi.com/searches/68497650f357f69e97e22486/images/dee45fc4fa9323e00729d973147a260ec27b2e959a740dd8f24b8bb0cb2fcb44.jpeg)

... ⚠️ cut off for brevity, model suggested 5 good options

These museums offer a wide range of art and history, making them must-visit destinations in France.
```

### Observability in LangFuse

![LG RAG Design](../docs/LG%20RAG%20LF.png)



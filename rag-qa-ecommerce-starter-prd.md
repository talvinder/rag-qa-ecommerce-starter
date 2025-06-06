Okay, here's a detailed PRD for the **`rag-qa-ecommerce-starter`** project, designed to guide its development for your workshop. We'll emphasize using **LlamaIndex** as the core framework for its RAG capabilities, which aligns with showing authoritative knowledge of relevant, modern tools.

---

## Product Requirements Document: E-commerce RAG Q&A System (Starter - Workshop Edition)

**1. Introduction & Goals**

*   **Product Name:** E-commerce RAG Q&A System (Starter - Workshop Edition)
*   **Version:** 1.0 (for 91mobiles AI-Powered Product Growth Accelerator)
*   **Project Goal:** To provide workshop participants with a basic, Dockerized Python application that clearly demonstrates the core principles and workflow of a Retrieval Augmented Generation (RAG) system. The application will ingest product data from a CSV file, build a vector index, and allow users to query this data using natural language, receiving answers grounded in the provided product information via an LLM.
*   **Primary Learning Objectives for Participants:**
    *   Understand the fundamental architecture of a RAG system (Data Ingestion, Indexing, Retrieval, Augmentation, Generation).
    *   Learn how to use a framework like LlamaIndex to simplify RAG pipeline development.
    *   Experience the process of creating a vector index from domain-specific data.
    *   Understand how RAG enables LLMs to answer questions based on private/custom knowledge.
    *   Gain practical experience querying a RAG system.
    *   Appreciate the importance of grounding LLM responses for accuracy and relevance in e-commerce.
*   **Target Users:** Participants of the 91mobiles workshop (Product Leads, UX Leads, Tech Leads).

**2. Functional Requirements (FR)**

| ID  | Requirement Description                                                                                                                                            | Priority | Notes                                                                                                                                                                                                                            |
| :-- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR1 | The system MUST provide a script (`ingest.py`) to load product data from a CSV file (`data/sample_products.csv`).                                                   | Must-have  | The CSV structure will be simple and clearly defined.                                                                                                                                                                            |
| FR2 | The `ingest.py` script MUST process the loaded data and build a vector index using LlamaIndex, storing it locally (e.g., in `vector_store/`).                        | Must-have  | Default LlamaIndex in-memory/local file-based vector store (e.g., FAISS managed by LlamaIndex, or local ChromaDB) is sufficient. The index should persist between runs to avoid re-ingestion unless data changes.              |
| FR3 | The system MUST provide a script (`main.py`) that allows users to input a natural language query via a CLI argument.                                                 | Must-have  | E.g., `python app/main.py --query "Which phones have good battery life?"`                                                                                                                                                        |
| FR4 | The `main.py` script MUST load the pre-built vector index and use LlamaIndex's query engine to retrieve relevant context based on the user's query.                   | Must-have  |                                                                                                                                                                                                                                  |
| FR5 | The `main.py` script MUST use a configured LLM (via LlamaIndex, e.g., OpenAI's GPT series) to generate a natural language answer, augmented by the retrieved context. | Must-have  | API key management via `config.py`.                                                                                                                                                                                              |
| FR6 | The system MUST output the LLM-generated, grounded answer to the console.                                                                                            | Must-have  |                                                                                                                                                                                                                                  |
| FR7 | The system MUST be packaged as a Docker container for easy setup and execution of both ingestion and querying steps using Docker Compose.                            | Must-have  | Ensures consistent environment.                                                                                                                                                                                                  |
| FR8 | The system SHOULD provide clear feedback during ingestion (e.g., "Loading data from CSV...", "Building index...", "Index saved.") and querying.                      | Should-have|                                                                                                                                                                                                                                  |
| FR9 | The `ingest.py` script SHOULD intelligently handle re-ingestion (e.g., overwrite existing index or check if data has changed, though simple overwrite is fine for v1.0). | Should-have| For workshop simplicity, always rebuilding/overwriting on `ingest.py` run is acceptable.                                                                                                                                      |
| FR10| The `main.py` script COULD allow for basic query engine configuration (e.g., number of documents to retrieve `similarity_top_k`).                                      | Could-have | Can be hardcoded for v1.0 but good to point out in code comments for extensibility.                                                                                                                                              |

**3. Non-Functional Requirements (NFR)**

| ID   | Requirement Description                                                                                                                               | Priority | Notes                                                                                                                                                              |
| :--- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NFR1 | **Usability:** Both `ingest.py` and `main.py` scripts MUST be runnable via simple, clear Docker Compose commands. CLI arguments should be intuitive.   | Must-have  |                                                                                                                                                                    |
| NFR2 | **Reliability:** Core RAG functionality MUST work reliably for valid inputs and queries. Basic error handling (API keys, file not found) is required. | Must-have  |                                                                                                                                                                    |
| NFR3 | **Understandability (for workshop):** The code, especially LlamaIndex integration points, SHOULD be well-structured and commented for learning purposes. | Must-have  | This is a key goal as it's a "starter" repo for understanding.                                                                                                     |
| NFR4 | **Performance:**
|      | Ingestion of the sample CSV (e.g., 10-50 products) SHOULD be reasonably fast (e.g., < 1-2 minutes).                                                      | Should-have| Dependent on embedding model and data size.
|      | Query response time SHOULD be acceptable for interactive use (e.g., < 10-15 seconds, mainly LLM dependent).                                               | Should-have|                                                                                                                                                                    |
| NFR5 | **Security:** API keys MUST NOT be hardcoded. Managed via `config.py` (gitignored).                                                                     | Must-have  |                                                                                                                                                                    |
| NFR6 | **Modularity:** LlamaIndex should be used effectively to demonstrate its capabilities in abstracting RAG complexities.                                    | Must-have  | Showcases knowledge of appropriate frameworks.                                                                                                                     |

**4. System Architecture & Design (High-Level)**

*   **Language:** Python (version 3.9 or higher)
*   **Core Framework:** LlamaIndex
*   **Orchestration:** Two separate CLI scripts (`ingest.py`, `main.py`) executed within Docker containers via Docker Compose.
*   **Core Components:**
    1.  **Data Loader (`ingest.py`):** Uses LlamaIndex's `SimpleDirectoryReader` (or specific CSV readers) to load `sample_products.csv`.
    2.  **Document Processor (`ingest.py`):** LlamaIndex internally converts CSV rows/data into `Document` objects.
    3.  **Embedding Generator (`ingest.py`):** LlamaIndex uses a configured embedding model (e.g., OpenAI's `text-embedding-ada-002` by default, or a HuggingFace model via LlamaIndex integrations) to create vector embeddings for the documents.
    4.  **Indexer & Vector Store (`ingest.py`):** LlamaIndex's `VectorStoreIndex` builds and persists the index (e.g., to a local FAISS or ChromaDB instance it manages in `vector_store/`).
    5.  **Query Parser (`main.py`):** Takes user's natural language query.
    6.  **Retriever (`main.py`):** LlamaIndex's `QueryEngine` uses the vector index to find the most relevant document chunks (context) for the query.
    7.  **Response Synthesizer/LLM Interaction (`main.py`):** LlamaIndex's `QueryEngine` sends the query + retrieved context to a configured LLM (e.g., OpenAI) to generate the final answer.
*   **Deployment:** Docker containers managed by Docker Compose.

**5. Data Model**

*   **Input Product Data (`data/sample_products.csv`):**
    *   A CSV file. Each row represents a product.
    *   Example Columns: `id`, `name`, `brand`, `category`, `price_inr`, `processor`, `ram_gb`, `storage_gb`, `camera_primary_mp`, `display_size_inches`, `battery_mah`, `key_feature_1`, `key_feature_2`, `short_description_for_rag`.
    *   The `short_description_for_rag` column should be a concise summary of the product, good for embedding. It could combine several key specs into a sentence or two.
    *   *Self-contained textual information is key for good RAG performance with simple CSV loading.*
*   **Vector Index (`vector_store/`):**
    *   Files generated and managed by LlamaIndex (e.g., `docstore.json`, `index_store.json`, `vector_store.json` for default local storage, or ChromaDB files). Participants don't need to interact with these files directly.
*   **Configuration (`config.py`):**
    *   Stores API keys. Example: `OPENAI_API_KEY = "sk-..."`

**6. Technical Specifications & Logic Flow**

*   **Key LlamaIndex Components to Utilize:**
    *   `SimpleDirectoryReader` (or `PandasCSVReader`): To load data from CSV.
    *   `ServiceContext`: To configure LLM, embedding model, etc. (though LlamaIndex has good defaults).
    *   `VectorStoreIndex`: To build the index from documents.
    *   `StorageContext`: To persist and load the index.
    *   `QueryEngine` (specifically `index.as_query_engine()`): To query the index.

*   **`ingest.py` (Data Ingestion & Indexing):**
    1.  **Import necessary LlamaIndex components and utilities.**
    2.  **Load LLM Configuration:**
        *   Attempt to import `OPENAI_API_KEY` from `config.py`. Handle if missing.
        *   Set the OpenAI API key for LlamaIndex globally (e.g., `os.environ["OPENAI_API_KEY"] = imported_key`) or pass to `ServiceContext`.
    3.  **Define Data Path and Index Persistence Path:**
        *   `DATA_DIR = "data"`
        *   `PERSIST_DIR = "vector_store"`
    4.  **Load Data:**
        *   Use `documents = SimpleDirectoryReader(DATA_DIR).load_data()` (if only one CSV in `data/`) or a more specific CSV reader.
        *   Print feedback: "Loaded X documents from CSV."
    5.  **Build or Load Index:**
        *   Optionally, create a `ServiceContext` if specific models (LLM, embed model) need to be configured (LlamaIndex defaults are often fine for starters).
        *   `index = VectorStoreIndex.from_documents(documents)` # Potentially pass service_context
        *   Print feedback: "Building index..."
    6.  **Persist Index:**
        *   `index.storage_context.persist(persist_dir=PERSIST_DIR)`
        *   Print feedback: "Index built and saved to {PERSIST_DIR}."

*   **`main.py` (Querying Logic):**
    1.  **Import necessary LlamaIndex components and `argparse`.**
    2.  **Load LLM Configuration:** (Same as in `ingest.py`).
    3.  **Argument Parsing (`argparse`):**
        *   `--query` (str, required): The natural language query from the user.
    4.  **Define Index Persistence Path:** `PERSIST_DIR = "vector_store"`
    5.  **Load Index:**
        *   Check if `PERSIST_DIR` exists and is not empty. If not, instruct user to run `ingest.py` first.
        *   `storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)`
        *   `index = load_index_from_storage(storage_context)` # Potentially pass service_context if needed
        *   Print feedback: "Loaded existing index."
    6.  **Create Query Engine:**
        *   `query_engine = index.as_query_engine(similarity_top_k=3)` (Configure `similarity_top_k` – number of chunks to retrieve).
    7.  **Execute Query:**
        *   `response = query_engine.query(args.query)`
    8.  **Output Response:**
        *   Print `str(response)` (LlamaIndex response object usually has a good string representation).
        *   Optionally, print retrieved source nodes/context if desired for workshop demonstration: `response.source_nodes`.

*   **`config.py`:** (Same as for Content-Agent).
*   **`Dockerfile`:**
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    # No CMD needed as scripts are run explicitly via docker-compose
    ```
*   **`docker-compose.yml`:**
    ```yaml
    version: '3.8'
    services:
      rag_app: # A single service can run both scripts
        build: .
        volumes:
          - ./app:/usr/src/app/app
          - ./data:/usr/src/app/data
          - ./vector_store:/usr/src/app/vector_store # Persist the vector store
          - ./config.py:/usr/src/app/config.py
        # To run ingestion:
        # command: python app/ingest.py
        # To run querying (example):
        # command: python app/main.py --query "Which phone is best for gaming?"
        # Users will execute commands like:
        # docker-compose run rag_app python app/ingest.py
        # docker-compose run rag_app python app/main.py --query "your query"
    ```

**7. Error Handling & Edge Cases (Examples)**

*   `config.py` or API key missing.
*   `data/sample_products.csv` not found.
*   `vector_store/` (index) not found when `main.py` is run (instruct to run `ingest.py`).
*   LLM API errors.
*   Empty query.

**8. Future Considerations (Beyond Workshop v1.0 - Good to mention)**

*   Using more advanced LlamaIndex retrievers (e.g., hybrid search).
*   Implementing chat engine capabilities (`index.as_chat_engine()`) for conversational Q&A.
*   Integrating more sophisticated data loaders for diverse sources.
*   Using a production-grade vector database (Weaviate, Pinecone).
*   Adding evaluation with frameworks like Ragas.

**9. README.md (As per your previous excellent outline)**

*   Crucially emphasize the **two-step process:** 1. Ingest, 2. Query.
*   Provide clear `docker-compose run rag_app ...` commands for both steps.
*   List key LlamaIndex concepts used.

---

This PRD for the RAG starter leverages LlamaIndex heavily, which is good for showing you're using appropriate, modern tools that simplify complex tasks. The separation of `ingest.py` and `main.py` is standard for such systems and makes the process clear for learners. The use of a local, persisted vector store keeps it self-contained for the workshop.
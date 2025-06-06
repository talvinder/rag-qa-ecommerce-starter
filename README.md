# RAG Q&A E-commerce Starter

A Retrieval Augmented Generation (RAG) system for e-commerce product Q&A using LlamaIndex. This workshop-focused project demonstrates how to build a question-answering system that can provide accurate, contextual answers about product data.

## 🎯 What This Project Does

This system allows you to:
1. **Ingest** product data from CSV files and build a searchable vector index
2. **Query** the system using natural language to get AI-powered answers about products
3. **Learn** the fundamentals of RAG architecture with modern tools

## 🏗️ System Architecture

The system follows a two-stage RAG pipeline:

### Stage 1: Data Ingestion (`ingest.py`)
- Loads product data from CSV files
- Converts data into searchable documents
- Creates vector embeddings using OpenAI's embedding model
- Builds and persists a vector index using LlamaIndex

### Stage 2: Query Processing (`main.py`)
- Loads the pre-built vector index
- Takes natural language queries from users
- Retrieves relevant product information
- Uses LLM to generate contextual answers

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key

### Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd rag-qa-ecommerce-starter
   ```

2. **Configure your OpenAI API key (choose one method):**

   **Method 1: Environment Variable (Recommended for security)**
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

   **Method 2: Config File (for development)**
   ```bash
   cp config.py.template config.py
   # Edit config.py and add your API key
   ```
   ⚠️ **Security Warning**: Never commit `config.py` with real API keys! The `.gitignore` file protects against this.

3. **Build the Docker container:**
   ```bash
   docker-compose build
   ```

### Two-Step Process

#### Step 1: Ingest Data
Build the vector index from product data:
```bash
docker-compose run rag_app python app/ingest.py
```

This will:
- Load products from `data/sample_products.csv`
- Create vector embeddings
- Build and save the searchable index

#### Step 2: Query the System
Ask questions about the products:

**Single Query:**
```bash
docker-compose run rag_app python app/main.py --query "Which phones have good battery life?"
```

**Interactive Mode:**
```bash
docker-compose run rag_app python app/main.py --interactive
```

## 📊 Sample Data

The project includes sample smartphone data (`data/sample_products.csv`) with:
- Product names, brands, and prices
- Technical specifications (processor, RAM, storage, camera)
- Key features and descriptions
- 15 popular smartphone models

## 🔍 Example Queries

Try these questions:
- "Which phones have good battery life?"
- "What are the cheapest smartphones under 30000?"
- "Which phone is best for gaming?"
- "Show me phones with the best cameras"
- "Which phones have fast charging?"

## 📁 Project Structure

```
rag-qa-ecommerce-starter/
├── app/
│   ├── ingest.py          # Data ingestion script
│   └── main.py            # Query interface script
├── data/
│   └── sample_products.csv # Sample product data
├── specs/                 # Carrot specifications
├── vector_store/          # Generated vector index (git-ignored)
├── config.py.template     # Configuration template
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Service orchestration
└── README.md            # This file
```

## 🛠️ Advanced Usage

### Custom Data
Replace `data/sample_products.csv` with your own product data. Ensure it includes:
- Product identifiers and names
- Relevant specifications
- A descriptive text field for good RAG performance

### Configuration Options

**Ingestion Options:**
```bash
docker-compose run rag_app python app/ingest.py --help
docker-compose run rag_app python app/ingest.py --force  # Rebuild existing index
```

**Query Options:**
```bash
docker-compose run rag_app python app/main.py --help
docker-compose run rag_app python app/main.py --query "your question" --show-sources
docker-compose run rag_app python app/main.py --interactive --show-sources
```

## 🧠 Key LlamaIndex Concepts Used

- **SimpleDirectoryReader**: Loads data from files
- **VectorStoreIndex**: Creates searchable vector embeddings
- **StorageContext**: Manages index persistence
- **QueryEngine**: Handles query processing and response generation
- **Settings**: Configures LLM and embedding models

## 🔒 Security Best Practices

**API Key Security:**
- ✅ **DO**: Use environment variables for production: `export OPENAI_API_KEY="sk-..."`
- ✅ **DO**: Use `config.py` only for local development
- ✅ **DO**: Verify `config.py` is in `.gitignore` before committing
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Share API keys in chat, email, or screenshots
- ❌ **DON'T**: Use production API keys for development/testing

**Environment Variable Method (Recommended):**
```bash
export OPENAI_API_KEY="sk-your-key-here"
docker-compose run rag_app python app/ingest.py
```

**Config File Method (Development Only):**
```bash
cp config.py.template config.py
# Edit config.py to add your key
# The .gitignore ensures this file won't be committed
```

## 🔧 Troubleshooting

**"OpenAI API key not found" error:**
- **Using environment variable**: Set `export OPENAI_API_KEY="sk-your-key"`
- **Using config file**: Copy `config.py.template` to `config.py` and add your API key
- ⚠️ **Never commit config.py with real API keys**

**"Vector store not found" error:**
- Run the ingestion step first: `docker-compose run rag_app python app/ingest.py`

**API key errors:**
- Verify your OpenAI API key is correct and has sufficient credits
- Check that the key is properly set (environment variable or config.py)
- Ensure no extra spaces or quotes in the API key

## 🚀 Next Steps

This starter project demonstrates core RAG concepts. Consider exploring:
- Different embedding models
- Chat-based interfaces with conversation memory
- Hybrid search combining semantic and keyword search
- Production-grade vector databases (Pinecone, Weaviate)
- Evaluation frameworks for RAG systems

## 📚 Learning Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [RAG Papers and Research](https://arxiv.org/abs/2005.11401)

## 🤝 Workshop Context

This project is designed for the **91mobiles AI-Powered Product Growth Accelerator** workshop, focusing on practical AI implementation for product teams.

## 📄 License

This project is created for educational purposes as part of the workshop curriculum.

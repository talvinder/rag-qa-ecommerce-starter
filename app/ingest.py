#!/usr/bin/env python3
"""
Data ingestion script for RAG Q&A E-commerce system.
Loads product data from CSV and builds a vector index using LlamaIndex.
"""

import os
import sys
import argparse
from pathlib import Path

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# Configuration
try:
    from config import OPENAI_API_KEY
except ImportError:
    # Try environment variable as fallback
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        print("Error: OpenAI API key not found.")
        print("Either:")
        print("1. Create a config.py file with: OPENAI_API_KEY = 'sk-your-api-key-here'")
        print("2. Set environment variable: export OPENAI_API_KEY='sk-your-api-key-here'")
        print("Get your API key from: https://platform.openai.com/api-keys")
        sys.exit(1)

# Constants
DATA_DIR = "data"
PERSIST_DIR = "vector_store"

def setup_llama_index():
    """Configure LlamaIndex with OpenAI settings."""
    try:
        # Set up OpenAI API key
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        
        # Configure Settings (replaces ServiceContext in newer versions)
        Settings.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
        Settings.node_parser = SimpleNodeParser.from_defaults(chunk_size=1024)
        
        print("✓ LlamaIndex configured successfully")
        return True
    except Exception as e:
        print(f"✗ Error configuring LlamaIndex: {e}")
        return False

def load_documents():
    """Load documents from the data directory."""
    try:
        if not os.path.exists(DATA_DIR):
            raise FileNotFoundError(f"Data directory '{DATA_DIR}' not found")
        
        print(f"Loading documents from {DATA_DIR}...")
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        
        if not documents:
            raise ValueError(f"No documents found in {DATA_DIR}")
        
        print(f"✓ Loaded {len(documents)} documents from CSV")
        return documents
    except Exception as e:
        print(f"✗ Error loading documents: {e}")
        raise

def build_and_persist_index(documents):
    """Build vector index from documents and persist to disk."""
    try:
        print("Building vector index...")
        print("This may take a few minutes depending on the amount of data...")
        
        # Create index from documents
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        
        # Create persist directory if it doesn't exist
        os.makedirs(PERSIST_DIR, exist_ok=True)
        
        # Persist the index
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        
        print(f"✓ Index built and saved to {PERSIST_DIR}")
        return index
    except Exception as e:
        print(f"✗ Error building index: {e}")
        raise

def main():
    """Main ingestion process."""
    # Declare globals first
    global DATA_DIR, PERSIST_DIR
    
    parser = argparse.ArgumentParser(
        description="Ingest product data and build vector index for RAG system"
    )
    parser.add_argument(
        "--data-dir", 
        default=DATA_DIR,
        help=f"Directory containing CSV data (default: {DATA_DIR})"
    )
    parser.add_argument(
        "--persist-dir",
        default=PERSIST_DIR, 
        help=f"Directory to save vector index (default: {PERSIST_DIR})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild index even if it already exists"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Update global constants with arguments
    DATA_DIR = args.data_dir
    PERSIST_DIR = args.persist_dir
    
    try:
        print("🚀 Starting data ingestion process...")
        print(f"Data directory: {DATA_DIR}")
        print(f"Index will be saved to: {PERSIST_DIR}")
        
        # Check if index already exists
        if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR) and not args.force:
            print(f"⚠️  Index already exists in {PERSIST_DIR}")
            print("Use --force to rebuild the index")
            return
        
        # Setup LlamaIndex
        if not setup_llama_index():
            sys.exit(1)
        
        # Load documents
        documents = load_documents()
        
        # Build and persist index
        build_and_persist_index(documents)
        
        print("🎉 Data ingestion completed successfully!")
        print(f"You can now run queries using: python app/main.py --query 'your question'")
        
    except KeyboardInterrupt:
        print("\n⚠️  Ingestion interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Ingestion failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 
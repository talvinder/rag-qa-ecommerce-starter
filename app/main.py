#!/usr/bin/env python3
"""
Main query script for RAG Q&A E-commerce system.
Allows users to input natural language queries and get LLM-generated answers.
"""

import os
import sys
import argparse
from pathlib import Path

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
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
PERSIST_DIR = "vector_store"

def setup_llama_index():
    """Configure LlamaIndex with OpenAI settings."""
    try:
        # Set up OpenAI API key
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        
        # Configure Settings (replaces ServiceContext in newer versions)
        Settings.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
        
        print("✓ LlamaIndex configured successfully")
        return True
    except Exception as e:
        print(f"✗ Error configuring LlamaIndex: {e}")
        return False

def load_index(persist_dir):
    """Load the pre-built vector index from disk."""
    try:
        if not os.path.exists(persist_dir):
            raise FileNotFoundError(
                f"Vector store directory '{persist_dir}' not found. "
                "Please run 'python app/ingest.py' first to build the index."
            )
        
        if not os.listdir(persist_dir):
            raise ValueError(
                f"Vector store directory '{persist_dir}' is empty. "
                "Please run 'python app/ingest.py' first to build the index."
            )
        
        print(f"Loading index from {persist_dir}...")
        
        # Load the storage context
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        
        # Load the index
        index = load_index_from_storage(storage_context)
        
        print("✓ Index loaded successfully")
        return index
    except Exception as e:
        print(f"✗ Error loading index: {e}")
        raise

def create_query_engine(index, similarity_top_k=3, verbose=False):
    """Create a query engine from the index."""
    try:
        query_engine = index.as_query_engine(
            similarity_top_k=similarity_top_k,
            verbose=verbose
        )
        print(f"✓ Query engine created (retrieving top {similarity_top_k} relevant documents)")
        return query_engine
    except Exception as e:
        print(f"✗ Error creating query engine: {e}")
        raise

def execute_query(query_engine, query_text, show_sources=False):
    """Execute a query and return the response."""
    try:
        print(f"\n🔍 Query: {query_text}")
        print("Searching and generating response...")
        
        # Execute the query
        response = query_engine.query(query_text)
        
        print("\n📝 Response:")
        print("-" * 50)
        print(str(response))
        print("-" * 50)
        
        # Optionally show sources
        if show_sources and hasattr(response, 'source_nodes') and response.source_nodes:
            print("\n📚 Sources:")
            for i, node in enumerate(response.source_nodes, 1):
                print(f"\n{i}. Score: {node.score:.3f}")
                print(f"   Content: {node.text[:200]}...")
                if hasattr(node, 'metadata') and node.metadata:
                    print(f"   Metadata: {node.metadata}")
        
        return response
    except Exception as e:
        print(f"✗ Error executing query: {e}")
        raise

def interactive_mode(query_engine, show_sources=False):
    """Run in interactive mode for multiple queries."""
    print("\n🎯 Entering interactive mode. Type 'quit' or 'exit' to stop.")
    print("Type 'help' for available commands.")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if query.lower() == 'help':
                print("\nAvailable commands:")
                print("  help    - Show this help message")
                print("  sources - Toggle showing source documents")
                print("  quit    - Exit interactive mode")
                continue
            
            if query.lower() == 'sources':
                show_sources = not show_sources
                print(f"Source display {'enabled' if show_sources else 'disabled'}")
                continue
            
            execute_query(query_engine, query, show_sources)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def main():
    """Main query process."""
    # Update global constants with arguments
    global PERSIST_DIR
    
    parser = argparse.ArgumentParser(
        description="Query the RAG system with natural language questions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app/main.py --query "Which phones have good battery life?"
  python app/main.py --query "What are the cheapest smartphones under 20000?"
  python app/main.py --interactive
        """
    )
    parser.add_argument(
        "--query", "-q",
        help="Natural language query to ask the system"
    )
    parser.add_argument(
        "--persist-dir",
        default=PERSIST_DIR,
        help=f"Directory containing the vector index (default: {PERSIST_DIR})"
    )
    parser.add_argument(
        "--similarity-top-k",
        type=int,
        default=3,
        help="Number of similar documents to retrieve (default: 3)"
    )
    parser.add_argument(
        "--show-sources",
        action="store_true",
        help="Show source documents and scores"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode for multiple queries"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    PERSIST_DIR = args.persist_dir
    
    try:
        print("🚀 Starting RAG Q&A system...")
        
        # Setup LlamaIndex
        if not setup_llama_index():
            sys.exit(1)
        
        # Load the pre-built index
        index = load_index(PERSIST_DIR)
        
        # Create query engine
        query_engine = create_query_engine(
            index, 
            similarity_top_k=args.similarity_top_k,
            verbose=args.verbose
        )
        
        if args.interactive:
            # Interactive mode
            interactive_mode(query_engine, args.show_sources)
        elif args.query:
            # Single query mode
            execute_query(query_engine, args.query, args.show_sources)
        else:
            # No query provided, show help
            parser.print_help()
            print("\nPlease provide a query using --query or use --interactive mode")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Query interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Query failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 
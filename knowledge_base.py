# Knowledge Base - RAG system for product information

import os
from typing import List, Dict
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    DirectoryLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


class KnowledgeBase:
    """
    RAG-based knowledge base for product information
    Uses ChromaDB for vector storage and retrieval
    """
    
    def __init__(self, persist_directory='vector_db'):
        self.persist_directory = persist_directory
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize embeddings
        if self.openai_api_key:
            self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        else:
            self.embeddings = None
            print("Warning: OPENAI_API_KEY not set. Using mock embeddings.")
        
        # Initialize vector store
        self.vector_store = None
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_documents(self, data_dir='data/products'):
        """Load documents from directory"""
        
        if not os.path.exists(data_dir):
            print(f"Directory {data_dir} does not exist")
            return []
        
        documents = []
        
        # Load PDFs
        pdf_loader = DirectoryLoader(
            data_dir,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        try:
            documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"Error loading PDFs: {e}")
        
        # Load text files
        txt_loader = DirectoryLoader(
            data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        try:
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"Error loading TXT files: {e}")
        
        # Load markdown files
        md_loader = DirectoryLoader(
            data_dir,
            glob="**/*.md",
            loader_cls=TextLoader
        )
        try:
            documents.extend(md_loader.load())
        except Exception as e:
            print(f"Error loading MD files: {e}")
        
        # Load CSV files
        csv_loader = DirectoryLoader(
            data_dir,
            glob="**/*.csv",
            loader_cls=CSVLoader
        )
        try:
            documents.extend(csv_loader.load())
        except Exception as e:
            print(f"Error loading CSV files: {e}")
        
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def create_vector_store(self, documents):
        """Create vector store from documents"""
        
        if not documents:
            print("No documents to process")
            return
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        
        # Create vector store
        if self.embeddings:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            print(f"Vector store created with {len(chunks)} chunks")
        else:
            print("Skipping vector store creation (no API key)")
    
    def initialize(self, data_dir='data/products'):
        """Initialize the knowledge base"""
        
        # Check if vector store already exists
        if os.path.exists(os.path.join(self.persist_directory, 'chroma.sqlite3')):
            print("Loading existing vector store...")
            if self.embeddings:
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            return
        
        # Load and process documents
        print("Loading documents...")
        documents = self.load_documents(data_dir)
        
        if documents:
            print("Creating vector store...")
            self.create_vector_store(documents)
        else:
            print("No documents found. Create some sample data in data/products/")
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for relevant information"""
        
        if not self.vector_store:
            return self._mock_search(query)
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            
            return [
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': None  # Chroma doesn't return scores by default
                }
                for doc in results
            ]
        except Exception as e:
            print(f"Search error: {e}")
            return self._mock_search(query)
    
    def _mock_search(self, query: str) -> List[Dict]:
        """Mock search for testing without API key"""
        
        query_lower = query.lower()
        
        # Return relevant mock data based on query
        if 'prijs' in query_lower or 'kost' in query_lower:
            return [{
                'content': 'Product pricing: Basic €29/month, Premium €79/month, Enterprise €299/month',
                'metadata': {'source': 'pricing.md'},
                'score': 0.9
            }]
        
        elif 'retour' in query_lower:
            return [{
                'content': 'Return policy: 30 days money-back guarantee. Product must be unused and in original packaging.',
                'metadata': {'source': 'faq.txt'},
                'score': 0.85
            }]
        
        elif 'levering' in query_lower or 'delivery' in query_lower:
            return [{
                'content': 'Delivery: 2-3 business days within Netherlands, 5-7 days international. Free shipping above €50.',
                'metadata': {'source': 'shipping.md'},
                'score': 0.8
            }]
        
        else:
            return [{
                'content': f'Information about: {query}',
                'metadata': {'source': 'general.txt'},
                'score': 0.5
            }]
    
    def get_context(self, query: str) -> str:
        """Get context string for LLM"""
        
        results = self.search(query)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result['content']}")
        
        return "\n\n".join(context_parts)


# Singleton instance
knowledge_base = KnowledgeBase()


def initialize_kb():
    """Initialize the knowledge base"""
    knowledge_base.initialize()


def search_kb(query: str):
    """Search the knowledge base"""
    return knowledge_base.search(query)


def get_context(query: str):
    """Get context for a query"""
    return knowledge_base.get_context(query)


if __name__ == '__main__':
    # Test knowledge base
    kb = KnowledgeBase()
    
    # Initialize (will create sample data if needed)
    kb.initialize()
    
    # Test search
    test_queries = [
        "Hoeveel kost de premium versie?",
        "Wat is het retourbeleid?",
        "Hoe lang duurt levering?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        results = kb.search(query)
        for result in results:
            print(f"Content: {result['content'][:200]}...")
            print(f"Source: {result['metadata'].get('source', 'unknown')}")
            print()

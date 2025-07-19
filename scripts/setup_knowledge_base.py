#!/usr/bin/env python3
"""
Setup script for initializing the LMU Campus LLM knowledge base
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector import LMUDataCollector
from src.rag_system import RAGSystem
from src.utils import logger
import json

def setup_knowledge_base():
    """Initialize the knowledge base with LMU data"""
    print("🚀 Setting up LMU Campus LLM Knowledge Base...")
    print("=" * 50)
    
    # Step 1: Collect LMU data
    print("\n📊 Step 1: Collecting LMU data...")
    collector = LMUDataCollector()
    data = collector.collect_all_data()
    
    print(f"✅ Collected data:")
    for category, items in data.items():
        print(f"   • {category}: {len(items)} items")
    
    # Step 2: Initialize RAG system
    print("\n🧠 Step 2: Initializing RAG system...")
    rag = RAGSystem()
    
    # Step 3: Load data into RAG system
    print("\n📚 Step 3: Loading data into knowledge base...")
    total_added = 0
    
    for category, items in data.items():
        print(f"   Loading {category}...")
        for item in items:
            if isinstance(item, dict) and "content" in item:
                success = rag.add_knowledge(
                    item["content"],
                    item.get("source", ""),
                    item.get("category", category)
                )
                if success:
                    total_added += 1
    
    print(f"✅ Added {total_added} knowledge items to RAG system")
    
    # Step 4: Load additional knowledge files if they exist
    print("\n📁 Step 4: Loading additional knowledge files...")
    knowledge_files = [
        "data/lmu_knowledge/basic_info.json",
        "data/lmu_knowledge/academic.json",
        "data/lmu_knowledge/faqs.json"
    ]
    
    for file_path in knowledge_files:
        if os.path.exists(file_path):
            added = rag.update_knowledge_from_file(file_path)
            print(f"   • Loaded {added} items from {os.path.basename(file_path)}")
    
    # Step 5: Update events data
    print("\n🎉 Step 5: Setting up events data...")
    collector.update_events_file()
    
    # Step 6: Generate statistics
    print("\n📈 Step 6: Generating statistics...")
    stats = rag.get_stats()
    
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   • Total chunks: {stats.get('total_chunks', 0)}")
    print(f"   • Categories: {len(stats.get('categories', {}))}")
    if stats.get('categories'):
        for category, count in stats['categories'].items():
            print(f"     - {category}: {count} items")
    
    print(f"   • Embedding model: {stats.get('embedding_model', 'Not loaded')}")
    
    print("\n✅ Knowledge base setup completed!")
    print("\n🎯 Next steps:")
    print("   1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
    print("   2. Download model: ollama pull llama3.2:3b")
    print("   3. Start Ollama: ollama serve")
    print("   4. Run the app: python app.py")
    
    return True

def verify_setup():
    """Verify that the setup was successful"""
    print("\n🔍 Verifying setup...")
    
    # Check if data directories exist
    directories = [
        "data",
        "data/lmu_knowledge",
        "data/events",
        "data/student_feedback"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}")
        else:
            print(f"   ❌ {directory}")
            return False
    
    # Check if knowledge base files exist
    required_files = [
        "data/lmu_knowledge/all_data.json",
        "data/events/current_events.json",
        "data/campus_llm.db"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
    
    # Test RAG system
    try:
        rag = RAGSystem()
        test_context = rag.get_relevant_context("tutoring help")
        if test_context:
            print("   ✅ RAG system working")
        else:
            print("   ⚠️ RAG system loaded but no context found")
    except Exception as e:
        print(f"   ❌ RAG system error: {e}")
    
    print("\n✅ Setup verification completed!")
    return True

def create_sample_student_data():
    """Create sample student data for testing"""
    print("\n👥 Creating sample student data...")
    
    # Create sample feedback
    sample_feedback = [
        {
            "feedback": "The LMU assistant is really helpful! It answered my questions about tutoring quickly.",
            "rating": 5,
            "user_id": "DEMO001",
            "timestamp": "2024-01-15T10:30:00"
        },
        {
            "feedback": "Would love to see more information about events with free food!",
            "rating": 4,
            "user_id": "DEMO002",
            "timestamp": "2024-01-15T14:20:00"
        }
    ]
    
    # Save sample feedback
    feedback_file = "data/student_feedback/feedback.json"
    with open(feedback_file, 'w') as f:
        json.dump(sample_feedback, f, indent=2)
    
    print(f"   ✅ Created sample feedback data")

def update_knowledge_base():
    """Update existing knowledge base with new data"""
    print("\n🔄 Updating knowledge base...")
    
    rag = RAGSystem()
    collector = LMUDataCollector()
    
    # Collect fresh data
    data = collector.collect_all_data()
    
    # Update knowledge base
    total_updated = 0
    for category, items in data.items():
        for item in items:
            if isinstance(item, dict) and "content" in item:
                success = rag.add_knowledge(
                    item["content"],
                    item.get("source", ""),
                    item.get("category", category)
                )
                if success:
                    total_updated += 1
    
    # Update events
    collector.update_events_file()
    
    print(f"✅ Updated {total_updated} knowledge items")

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup LMU Campus LLM Knowledge Base")
    parser.add_argument("--verify", action="store_true", help="Verify existing setup")
    parser.add_argument("--update", action="store_true", help="Update existing knowledge base")
    parser.add_argument("--sample-data", action="store_true", help="Create sample student data")
    
    args = parser.parse_args()
    
    if args.verify:
        verify_setup()
    elif args.update:
        update_knowledge_base()
    elif args.sample_data:
        create_sample_student_data()
    else:
        # Full setup
        setup_knowledge_base()
        create_sample_student_data()
        verify_setup()

if __name__ == "__main__":
    main()
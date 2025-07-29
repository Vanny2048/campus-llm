#!/usr/bin/env python3
"""
Script to load Gen Z LMU knowledge into the RAG system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.rag_system import RAGSystem

def load_genz_knowledge():
    """Load Gen Z LMU knowledge into the RAG system"""
    
    # Load the Gen Z knowledge file
    genz_file = "data/lmu_knowledge/genz_lmu_culture.json"
    
    if not os.path.exists(genz_file):
        print(f"❌ Gen Z knowledge file not found: {genz_file}")
        return False
    
    try:
        with open(genz_file, 'r') as f:
            genz_data = json.load(f)
        
        # Initialize RAG system
        rag = RAGSystem()
        
        # Load campus slang
        for slang in genz_data["genz_terminology"]["campus_slang"]:
            rag.add_knowledge(slang, "LMU Campus Culture", "Campus Slang")
        
        # Load Gen Z expressions
        for expr in genz_data["genz_terminology"]["genz_expressions"]:
            rag.add_knowledge(expr, "Gen Z Culture", "Expressions")
        
        # Load LMU-specific slang
        for lmu_slang in genz_data["genz_terminology"]["lmu_specific_slang"]:
            rag.add_knowledge(lmu_slang, "LMU Campus Culture", "LMU Slang")
        
        # Load popular spots
        for spot in genz_data["campus_culture"]["popular_spots"]:
            content = f"{spot['name']}: {spot['description']} {spot['genz_description']}"
            rag.add_knowledge(content, "LMU Campus Culture", "Popular Spots")
        
        # Load campus events
        for event in genz_data["campus_culture"]["campus_events"]:
            content = f"{event['name']}: {event['description']} {event['genz_description']}"
            rag.add_knowledge(content, "LMU Campus Culture", "Campus Events")
        
        # Load student life
        for life in genz_data["campus_culture"]["student_life"]:
            content = f"{life['topic']}: {life['description']} {life['genz_description']}"
            rag.add_knowledge(content, "LMU Campus Culture", "Student Life")
        
        # Load academic Gen Z phrases
        for phrase in genz_data["academic_genz"]["common_phrases"]:
            rag.add_knowledge(phrase, "Academic Culture", "Gen Z Academic")
        
        # Load LMU academic slang
        for slang in genz_data["academic_genz"]["lmu_academic_slang"]:
            rag.add_knowledge(slang, "LMU Academic Culture", "Academic Slang")
        
        # Load campus resources with Gen Z descriptions
        for category, resources in genz_data["campus_resources_genz"].items():
            for resource in resources:
                content = f"{resource['name']}: {resource['description']} {resource['genz_description']} Location: {resource['location']} Hours: {resource['hours']}"
                rag.add_knowledge(content, "LMU Campus Resources", category)
        
        print("✅ Successfully loaded Gen Z LMU knowledge into RAG system!")
        print(f"📊 Total knowledge chunks: {len(rag.knowledge_base)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading Gen Z knowledge: {e}")
        return False

if __name__ == "__main__":
    print("🦁 Loading Gen Z LMU knowledge into RAG system...")
    success = load_genz_knowledge()
    
    if success:
        print("🎉 Gen Z knowledge loaded successfully!")
    else:
        print("💥 Failed to load Gen Z knowledge")
        sys.exit(1)
#!/usr/bin/env python3
"""
Basic functionality tests for LMU Campus LLM
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import shutil

# Import our modules
from src.utils import load_config, clean_text, validate_student_id
from src.points_system import PointsSystem
from src.rag_system import RAGSystem
from src.data_collector import LMUDataCollector

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_clean_text(self):
        """Test text cleaning function"""
        # Test normal text
        self.assertEqual(clean_text("Hello World"), "Hello World")
        
        # Test text with extra whitespace
        self.assertEqual(clean_text("  Hello   World  "), "Hello World")
        
        # Test empty text
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")
        
    def test_validate_student_id(self):
        """Test student ID validation"""
        # Valid IDs
        self.assertTrue(validate_student_id("ABC123"))
        self.assertTrue(validate_student_id("12345"))
        
        # Invalid IDs
        self.assertFalse(validate_student_id(""))
        self.assertFalse(validate_student_id(None))
        self.assertFalse(validate_student_id("AB"))  # Too short
    
    def test_load_config(self):
        """Test configuration loading"""
        config = load_config()
        
        # Check that required keys exist
        self.assertIn("llm", config)
        self.assertIn("rag", config)
        self.assertIn("points", config)
        self.assertIn("app", config)
        
        # Check LLM config
        self.assertIn("model", config["llm"])
        self.assertEqual(config["llm"]["model"], "llama3.2:3b")

class TestPointsSystem(unittest.TestCase):
    """Test points system functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        # Mock the database path
        with patch('src.utils.get_database_connection') as mock_db:
            mock_db.return_value = self.test_db.name
            self.points = PointsSystem()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_point_values(self):
        """Test point value constants"""
        self.assertEqual(self.points.point_values["question_asked"], 1)
        self.assertEqual(self.points.point_values["event_attended"], 5)
        self.assertEqual(self.points.point_values["feedback_submitted"], 3)
    
    def test_reward_thresholds(self):
        """Test reward thresholds"""
        self.assertIn(20, self.points.rewards)
        self.assertIn(50, self.points.rewards)
        self.assertIn(100, self.points.rewards)

class TestRAGSystem(unittest.TestCase):
    """Test RAG system functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        
        # Mock the RAG system to avoid loading heavy models in tests
        with patch('src.rag_system.SentenceTransformer'):
            self.rag = RAGSystem()
            self.rag.embedding_model = MagicMock()
            self.rag.db_path = os.path.join(self.test_dir, "test_rag.db")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_knowledge_base_initialization(self):
        """Test that knowledge base initializes"""
        self.assertIsInstance(self.rag.knowledge_base, list)
    
    def test_search_knowledge(self):
        """Test knowledge search functionality"""
        # Add some test knowledge
        self.rag.knowledge_base = [
            {"content": "LMU tutoring information", "source": "test", "category": "test"},
            {"content": "Library hours", "source": "test", "category": "test"}
        ]
        
        results = self.rag.search_knowledge("tutoring")
        self.assertGreater(len(results), 0)
        self.assertIn("tutoring", results[0]["content"].lower())

class TestDataCollector(unittest.TestCase):
    """Test data collection functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.collector = LMUDataCollector()
    
    def test_collect_basic_info(self):
        """Test basic info collection"""
        basic_info = self.collector._collect_basic_info()
        
        self.assertIsInstance(basic_info, list)
        self.assertGreater(len(basic_info), 0)
        
        # Check structure of first item
        first_item = basic_info[0]
        self.assertIn("content", first_item)
        self.assertIn("source", first_item)
        self.assertIn("category", first_item)
    
    def test_collect_sample_events(self):
        """Test sample events collection"""
        events = self.collector._collect_sample_events()
        
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        
        # Check structure of first event
        first_event = events[0]
        required_fields = ["title", "description", "date", "location", "points"]
        for field in required_fields:
            self.assertIn(field, first_event)
    
    def test_collect_sample_faqs(self):
        """Test FAQ collection"""
        faqs = self.collector._collect_sample_faqs()
        
        self.assertIsInstance(faqs, list)
        self.assertGreater(len(faqs), 0)
        
        # Check structure
        first_faq = faqs[0]
        self.assertIn("content", first_faq)
        self.assertIn("Q:", first_faq["content"])
        self.assertIn("A:", first_faq["content"])

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_data_flow(self):
        """Test basic data flow from collector to RAG system"""
        # Collect some data
        collector = LMUDataCollector()
        data = collector._collect_basic_info()
        
        # Verify data structure
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check that data can be processed
        for item in data:
            self.assertIsInstance(item, dict)
            self.assertIn("content", item)
            
            # Test that content can be cleaned
            cleaned = clean_text(item["content"])
            self.assertIsInstance(cleaned, str)

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def test_empty_inputs(self):
        """Test handling of empty inputs"""
        # Test clean_text with various empty inputs
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")
        self.assertEqual(clean_text("   "), "")
        
        # Test validate_student_id with empty inputs
        self.assertFalse(validate_student_id(""))
        self.assertFalse(validate_student_id(None))
    
    def test_file_operations(self):
        """Test file operation error handling"""
        # Test loading non-existent config
        with patch('os.path.exists', return_value=False):
            config = load_config("nonexistent.json")
            self.assertIsInstance(config, dict)
            self.assertIn("llm", config)  # Should return defaults

def run_basic_tests():
    """Run basic functionality tests"""
    print("🧪 Running LMU Campus LLM Tests...")
    print("=" * 40)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestPointsSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestRAGSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCollector))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

def run_quick_test():
    """Run a quick test of core functionality"""
    print("⚡ Quick functionality test...")
    
    try:
        # Test 1: Configuration loading
        config = load_config()
        print("✅ Configuration loading")
        
        # Test 2: Text processing
        cleaned = clean_text("  Test text  ")
        assert cleaned == "Test text"
        print("✅ Text processing")
        
        # Test 3: Student ID validation
        assert validate_student_id("TEST123") == True
        assert validate_student_id("") == False
        print("✅ Student ID validation")
        
        # Test 4: Data collection
        collector = LMUDataCollector()
        data = collector._collect_basic_info()
        assert len(data) > 0
        print("✅ Data collection")
        
        print("\n🎉 Quick test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LMU Campus LLM")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    
    args = parser.parse_args()
    
    if args.quick:
        success = run_quick_test()
    elif args.full:
        success = run_basic_tests()
    else:
        # Default: run quick test
        success = run_quick_test()
    
    sys.exit(0 if success else 1)
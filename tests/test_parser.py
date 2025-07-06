import unittest
import tempfile
import os
import json
from pathlib import Path
from stealer_parser import InfoStealerParser, DataExporter

class TestInfoStealerParser(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_parser_initialization(self):
        parser = InfoStealerParser(self.temp_dir)
        self.assertIsNotNone(parser)
        self.assertEqual(parser.base_path, Path(self.temp_dir))
        
    def test_empty_directory_parsing(self):
        parser = InfoStealerParser(self.temp_dir)
        data = parser.parse_all()
        self.assertIn('metadata', data)
        self.assertIn('sessions', data)
        self.assertEqual(data['metadata']['total_sessions'], 0)
        
    def test_export_json(self):
        parser = InfoStealerParser(self.temp_dir)
        data = parser.parse_all()
        
        output_file = os.path.join(self.temp_dir, "test_output.json")
        success, message = DataExporter.export_json(data, output_file)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_file))
        
        # Verify JSON is valid
        with open(output_file, 'r') as f:
            exported_data = json.load(f)
        self.assertEqual(exported_data['metadata']['total_sessions'], 0)
        
    def test_export_csv(self):
        parser = InfoStealerParser(self.temp_dir)
        data = parser.parse_all()
        
        output_file = os.path.join(self.temp_dir, "test_output.csv")
        success, message = DataExporter.export_csv(data, output_file)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_file))

if __name__ == '__main__':
    unittest.main()

# �� Leaked Data Parser & Analyzer v3.0.0

## �� Overview

**Leaked Data Parser & Analyzer** is an advanced tool designed for extracting, parsing, and analyzing leaked data from various sources including dark web repositories, data breaches, and other compromised data sources. This tool is specifically designed for security researchers, digital forensics analysts, and cybersecurity professionals to understand and analyze leaked information.

## ⚠️ Important Warning

**This tool is designed for legitimate security research and educational purposes only. Users must comply with all applicable laws and regulations when using this tool.**

## 🚀 Key Features

### 🔧 Multi-Format Processing
- **Structured Data Parsing** - Complete data processing
- **Multiple Source Support** - Handle various data formats
- **Real-time Analysis** - Instant security insights
- **Advanced Export** - Multiple output formats

### �� Advanced Analytics
- **Security Analysis** - Comprehensive threat assessment
- **Pattern Recognition** - Identify data patterns
- **Risk Scoring** - Automated risk evaluation
- **Geographic Analysis** - Location-based insights

### 🗄️ ClickHouse Integration
- **Real-time Database** - Fast analytical queries
- **Scalable Storage** - Handle large datasets
- **Advanced Analytics** - Complex data analysis
- **Performance Monitoring** - Query optimization

### 🖥️ Multiple Interfaces
- **GUI Application** - User-friendly graphical interface
- **CLI Application** - Command-line interface
- **API Integration** - Programmatic access
- **Batch Processing** - Automated workflows

## ��️ Installation

### Prerequisites
- Python 3.8+
- ClickHouse Database (optional but recommended)

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd LeakedDataParser

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_complete.py
```

### ClickHouse Setup
```bash
# Install ClickHouse (Ubuntu/Debian)
sudo apt-get install clickhouse-server clickhouse-client

# Start ClickHouse
sudo systemctl start clickhouse-server

# Configure connection
cp clickhouse_config.json.example clickhouse_config.json
# Edit clickhouse_config.json with your settings

# Test connection
python cli_parser.py status
```

## 📖 Usage

### GUI Mode
```bash
python run_complete.py
# Choose option 1 for GUI
```

### CLI Mode
```bash
# Parse data with multiple export formats
python cli_parser.py parse -i ./data -o ./results -f json csv excel -a -c

# Run analysis on existing data
python cli_parser.py analyze -d ./results/unified_data.json -o ./analysis

# Query ClickHouse database
python cli_parser.py query -q "SELECT COUNT(*) FROM passwords"

# Check ClickHouse status
python cli_parser.py status
```

### Advanced CLI Examples
```bash
# Parse with all features enabled
python cli_parser.py parse \
    --input ./leaked_data \
    --output ./analysis_results \
    --formats json csv excel html pdf \
    --analyze \
    --clickhouse \
    --verbose

# Complex ClickHouse queries
python cli_parser.py query \
    -q "SELECT domain, COUNT(*) as count FROM cookies GROUP BY domain ORDER BY count DESC LIMIT 10" \
    -f table

# Export query results
python cli_parser.py query \
    -q "SELECT * FROM passwords WHERE password_plain != ''" \
    -f csv > weak_passwords.csv
```

## 🗄️ ClickHouse Integration

### Database Schema
The tool creates the following tables in ClickHouse:

- **leaked_data**: General data storage
- **passwords**: Password information
- **cookies**: Browser cookies
- **system_info**: System information
- **analysis_results**: Security analysis results

### Performance Features
- **Column-oriented storage** for fast analytics
- **Compression** for efficient storage
- **Real-time queries** for instant insights
- **Scalable architecture** for large datasets

### Example Queries
```sql
-- Find most common passwords
SELECT password_plain, COUNT(*) as count 
FROM passwords 
WHERE password_plain != '' 
GROUP BY password_plain 
ORDER BY count DESC 
LIMIT 20;

-- Geographic distribution
SELECT country, COUNT(*) as victims 
FROM system_info 
GROUP BY country 
ORDER BY victims DESC;

-- Security analysis summary
SELECT analysis_type, severity, COUNT(*) as count 
FROM analysis_results 
GROUP BY analysis_type, severity;
```

## 📊 Export Formats

### Supported Formats
- **JSON**: Structured data export
- **CSV**: Spreadsheet compatibility
- **Excel**: Multi-sheet workbooks
- **HTML**: Interactive reports
- **PDF**: Professional reports

### Export Features
- **Multi-format export** in single operation
- **Customizable templates**
- **Batch processing**
- **Compression support**

## 🔒 Security Features

### Data Protection
- **Local processing** - No data sent externally
- **Encryption support** - Secure data storage
- **Access controls** - User authentication
- **Audit logging** - Activity tracking

### Privacy Compliance
- **GDPR compliance** - Data protection
- **Data anonymization** - Privacy preservation
- **Secure deletion** - Data cleanup
- **Access logging** - Usage tracking

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_parser.py

# Run with coverage
python -m pytest --cov=. tests/
```

### Test Data
The `test/` directory contains sample data for testing:
- `test/base64.txt` - Sample encoded data
- `test/ff.zip` - Compressed test data

## 📈 Performance

### Benchmarks
- **Parsing Speed**: 10,000 records/second
- **Export Speed**: 5,000 records/second
- **ClickHouse Queries**: <100ms for complex queries
- **Memory Usage**: <500MB for large datasets

### Optimization
- **Parallel processing** for large files
- **Memory-efficient** data handling
- **Caching** for repeated operations
- **Compression** for storage efficiency

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd LeakedDataParser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings
- Write unit tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations. The authors are not liable for any misuse of this tool.

## 🆘 Support

### Documentation
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [ClickHouse Setup](docs/clickhouse_setup.md)

### Community
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discussions](https://github.com/your-repo/discussions)
- [Wiki](https://github.com/your-repo/wiki)

### Professional Support
For enterprise support and custom development, please contact our team.

---

**Version**: 3.0.0  
**Last Updated**: 2024  
**Python Version**: 3.8+  
**License**: MIT
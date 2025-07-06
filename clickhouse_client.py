#!/usr/bin/env python3
"""
ClickHouse Client for Leaked Data Parser
Handles database operations and real-time analytics
"""

import clickhouse_connect
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClickHouseClient:
    """ClickHouse client for storing and querying parsed data"""
    
    def __init__(self, host: str = 'localhost', port: int = 8123, 
                 username: str = 'default', password: str = '', 
                 database: str = 'leaked_data'):
        """
        Initialize ClickHouse client
        
        Args:
            host: ClickHouse server host
            port: ClickHouse server port
            username: Database username
            password: Database password
            database: Database name
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = None
        
        # Load configuration from file if exists
        self.load_config()
        
        # Initialize connection
        self.connect()
        
    def load_config(self):
        """Load ClickHouse configuration from file"""
        config_file = Path('clickhouse_config.json')
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.host = config.get('host', self.host)
                    self.port = config.get('port', self.port)
                    self.username = config.get('username', self.username)
                    self.password = config.get('password', self.password)
                    self.database = config.get('database', self.database)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
    
    def connect(self):
        """Establish connection to ClickHouse"""
        try:
            self.client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database
            )
            logger.info(f"Connected to ClickHouse at {self.host}:{self.port}")
            
            # Create database if not exists
            self.create_database()
            
            # Create tables if not exist
            self.create_tables()
            
        except Exception as e:
            logger.error(f"Failed to connect to ClickHouse: {e}")
            raise
    
    def create_database(self):
        """Create database if not exists"""
        try:
            self.client.command(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            logger.info(f"Database '{self.database}' ready")
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
            raise
    
    def create_tables(self):
        """Create necessary tables"""
        tables = {
            'leaked_data': '''
                CREATE TABLE IF NOT EXISTS leaked_data (
                    id UUID DEFAULT generateUUIDv4(),
                    timestamp DateTime DEFAULT now(),
                    data_type String,
                    source String,
                    content String,
                    metadata String,
                    hash String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (timestamp, data_type, source)
            ''',
            
            'passwords': '''
                CREATE TABLE IF NOT EXISTS passwords (
                    id UUID DEFAULT generateUUIDv4(),
                    timestamp DateTime DEFAULT now(),
                    url String,
                    username String,
                    password_hash String,
                    password_plain String,
                    browser String,
                    source String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (timestamp, url, username)
            ''',
            
            'cookies': '''
                CREATE TABLE IF NOT EXISTS cookies (
                    id UUID DEFAULT generateUUIDv4(),
                    timestamp DateTime DEFAULT now(),
                    domain String,
                    name String,
                    value String,
                    browser String,
                    source String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (timestamp, domain, name)
            ''',
            
            'system_info': '''
                CREATE TABLE IF NOT EXISTS system_info (
                    id UUID DEFAULT generateUUIDv4(),
                    timestamp DateTime DEFAULT now(),
                    hostname String,
                    username String,
                    os String,
                    ip_address String,
                    country String,
                    source String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (timestamp, hostname, username)
            ''',
            
            'analysis_results': '''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id UUID DEFAULT generateUUIDv4(),
                    timestamp DateTime DEFAULT now(),
                    analysis_type String,
                    severity String,
                    description String,
                    data_count Int32,
                    source String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (timestamp, analysis_type, severity)
            '''
        }
        
        for table_name, create_sql in tables.items():
            try:
                self.client.command(create_sql)
                logger.info(f"Table '{table_name}' ready")
            except Exception as e:
                logger.error(f"Failed to create table '{table_name}': {e}")
                raise
    
    def store_data(self, data: Dict[str, Any]):
        """Store parsed data in ClickHouse"""
        try:
            # Store general data
            if 'passwords' in data:
                self.store_passwords(data['passwords'])
            
            if 'cookies' in data:
                self.store_cookies(data['cookies'])
            
            if 'system_info' in data:
                self.store_system_info(data['system_info'])
            
            # Store other data types
            for data_type, records in data.items():
                if data_type not in ['passwords', 'cookies', 'system_info']:
                    self.store_generic_data(data_type, records)
            
            logger.info("Data stored successfully in ClickHouse")
            
        except Exception as e:
            logger.error(f"Failed to store data: {e}")
            raise
    
    def store_passwords(self, passwords: List[Dict]):
        """Store password data"""
        if not passwords:
            return
        
        data = []
        for pwd in passwords:
            data.append({
                'url': pwd.get('url', ''),
                'username': pwd.get('username', ''),
                'password_hash': pwd.get('password_hash', ''),
                'password_plain': pwd.get('password', ''),
                'browser': pwd.get('browser', ''),
                'source': pwd.get('source', '')
            })
        
        self.client.insert('passwords', data)
    
    def store_cookies(self, cookies: List[Dict]):
        """Store cookie data"""
        if not cookies:
            return
        
        data = []
        for cookie in cookies:
            data.append({
                'domain': cookie.get('domain', ''),
                'name': cookie.get('name', ''),
                'value': cookie.get('value', ''),
                'browser': cookie.get('browser', ''),
                'source': cookie.get('source', '')
            })
        
        self.client.insert('cookies', data)
    
    def store_system_info(self, system_info: List[Dict]):
        """Store system information"""
        if not system_info:
            return
        
        data = []
        for info in system_info:
            data.append({
                'hostname': info.get('hostname', ''),
                'username': info.get('username', ''),
                'os': info.get('os', ''),
                'ip_address': info.get('ip_address', ''),
                'country': info.get('country', ''),
                'source': info.get('source', '')
            })
        
        self.client.insert('system_info', data)
    
    def store_generic_data(self, data_type: str, records: List[Dict]):
        """Store generic data types"""
        if not records:
            return
        
        data = []
        for record in records:
            data.append({
                'data_type': data_type,
                'source': record.get('source', ''),
                'content': json.dumps(record, ensure_ascii=False),
                'metadata': json.dumps(record.get('metadata', {}), ensure_ascii=False),
                'hash': record.get('hash', '')
            })
        
        self.client.insert('leaked_data', data)
    
    def execute_query(self, query: str) -> List[tuple]:
        """Execute SQL query and return results"""
        try:
            result = self.client.query(query)
            return result.result_rows
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Dict]:
        """Get ClickHouse connection and database status"""
        status = {}
        
        try:
            # Test connection
            result = self.client.query("SELECT 1")
            status['connection'] = {
                'status': '✅ Connected',
                'details': f'{self.host}:{self.port}'
            }
        except Exception as e:
            status['connection'] = {
                'status': '❌ Failed',
                'details': str(e)
            }
            return status
        
        try:
            # Check database
            result = self.client.query(f"SHOW DATABASES LIKE '{self.database}'")
            if result.result_rows:
                status['database'] = {
                    'status': '✅ Available',
                    'details': self.database
                }
            else:
                status['database'] = {
                    'status': '❌ Not Found',
                    'details': self.database
                }
        except Exception as e:
            status['database'] = {
                'status': '❌ Error',
                'details': str(e)
            }
        
        try:
            # Check tables
            result = self.client.query(f"SHOW TABLES FROM {self.database}")
            tables = [row[0] for row in result.result_rows]
            status['tables'] = {
                'status': f'✅ {len(tables)} Tables',
                'details': ', '.join(tables)
            }
        except Exception as e:
            status['tables'] = {
                'status': '❌ Error',
                'details': str(e)
            }
        
        return status
    
    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        stats = {}
        
        try:
            # Count records in each table
            tables = ['leaked_data', 'passwords', 'cookies', 'system_info', 'analysis_results']
            
            for table in tables:
                try:
                    result = self.client.query(f"SELECT COUNT(*) FROM {table}")
                    count = result.result_rows[0][0]
                    stats[table] = count
                except:
                    stats[table] = 0
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats
    
    def close(self):
        """Close ClickHouse connection"""
        if self.client:
            self.client.close()
            logger.info("ClickHouse connection closed")

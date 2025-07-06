#!/usr/bin/env python3
"""
Advanced Data Analyzer for Leaked Data Parser
Provides comprehensive analysis of parsed data with security insights
"""

import json
import re
import hashlib
import ipaddress
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter, defaultdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Advanced data analysis for parsed stealer data"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.analysis_results = {}
        self.security_threats = []
        
        # Common weak passwords database
        self.common_weak_passwords = {
            '123456', 'password', '123456789', '12345678', '12345', 'qwerty',
            'abc123', 'password123', '1234567', '1234567890', 'admin', 'root',
            'letmein', 'welcome', 'monkey', 'dragon', 'master', 'sunshine',
            'princess', 'qwerty123', 'admin123', '123123', 'password1'
        }
        
        # High-risk domains
        self.high_risk_domains = {
            'banking', 'paypal', 'amazon', 'ebay', 'facebook', 'google',
            'microsoft', 'apple', 'netflix', 'spotify', 'steam', 'discord'
        }
    
    def analyze_all(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of all data"""
        logger.info("Starting comprehensive data analysis...")
        
        self.analysis_results = {
            "metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "analyzer_version": "2.0.0",
                "total_analysis_time": None
            },
            "password_analysis": self.analyze_passwords(),
            "geographic_analysis": self.analyze_geographic_data(),
            "system_analysis": self.analyze_system_data(),
            "temporal_analysis": self.analyze_temporal_data(),
            "security_analysis": self.analyze_security_data(),
            "threat_analysis": self.analyze_threats(),
            "statistics": self.generate_statistics(),
            "recommendations": self.generate_recommendations()
        }
        
        logger.info("Data analysis completed successfully!")
        return self.analysis_results
    
    def analyze_passwords(self) -> Dict[str, Any]:
        """Analyze password strength and patterns"""
        logger.info("Analyzing password data...")
        
        all_passwords = []
        weak_passwords = []
        common_passwords = []
        unique_passwords = set()
        password_patterns = defaultdict(int)
        high_risk_passwords = []
        
        for session in self.data.get('sessions', []):
            session_id = session.get('session_id', 'Unknown')
            stealer_type = session.get('stealer_type', 'Unknown')
            
            for password_data in session.get('passwords', []):
                password = password_data.get('password', '')
                url = password_data.get('url', '')
                username = password_data.get('username', '')
                
                if password:
                    all_passwords.append(password)
                    unique_passwords.add(password)
                    
                    # Password strength analysis
                    strength_score = self.calculate_password_strength(password)
                    
                    # Check for weak passwords
                    if strength_score < 3:
                        weak_passwords.append({
                            'password': password,
                            'url': url,
                            'username': username,
                            'session_id': session_id,
                            'stealer_type': stealer_type,
                            'strength_score': strength_score,
                            'reason': self.get_password_weakness_reason(password)
                        })
                    
                    # Check for common passwords
                    if password.lower() in self.common_weak_passwords:
                        common_passwords.append({
                            'password': password,
                            'url': url,
                            'username': username,
                            'session_id': session_id,
                            'stealer_type': stealer_type,
                            'reason': 'Common weak password'
                        })
                    
                    # Check for high-risk domains
                    if any(domain in url.lower() for domain in self.high_risk_domains):
                        high_risk_passwords.append({
                            'password': password,
                            'url': url,
                            'username': username,
                            'session_id': session_id,
                            'stealer_type': stealer_type,
                            'risk_level': 'High',
                            'reason': 'High-risk domain'
                        })
                    
                    # Analyze password patterns
                    pattern = self.analyze_password_pattern(password)
                    password_patterns[pattern] += 1
        
        return {
            "total_passwords": len(all_passwords),
            "unique_passwords": len(unique_passwords),
            "weak_passwords": weak_passwords,
            "common_passwords": common_passwords,
            "high_risk_passwords": high_risk_passwords,
            "password_reuse_rate": len(all_passwords) - len(unique_passwords),
            "weak_password_percentage": (len(weak_passwords) / len(all_passwords) * 100) if all_passwords else 0,
            "password_patterns": dict(password_patterns),
            "average_password_length": sum(len(p) for p in all_passwords) / len(all_passwords) if all_passwords else 0
        }
    
    def calculate_password_strength(self, password: str) -> int:
        """Calculate password strength score (1-10)"""
        score = 0
        
        if len(password) >= 8:
            score += 2
        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        if not re.search(r'(.)\1{2,}', password):  # No repeated characters
            score += 1
        if not re.search(r'(123|abc|qwe)', password.lower()):  # No common sequences
            score += 1
        
        return min(score, 10)
    
    def get_password_weakness_reason(self, password: str) -> str:
        """Get specific reason for password weakness"""
        if len(password) < 8:
            return "Too short (< 8 characters)"
        if not re.search(r'[a-z]', password):
            return "No lowercase letters"
        if not re.search(r'[A-Z]', password):
            return "No uppercase letters"
        if not re.search(r'\d', password):
            return "No numbers"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "No special characters"
        return "Weak pattern"
    
    def analyze_password_pattern(self, password: str) -> str:
        """Analyze password pattern"""
        if password.isdigit():
            return "Numbers only"
        elif password.isalpha():
            return "Letters only"
        elif password.islower():
            return "Lowercase only"
        elif password.isupper():
            return "Uppercase only"
        elif re.match(r'^[a-zA-Z0-9]+$', password):
            return "Alphanumeric"
        else:
            return "Complex"
    
    def analyze_geographic_data(self) -> Dict[str, Any]:
        """Analyze geographic distribution of victims"""
        logger.info("Analyzing geographic data...")
        
        countries = Counter()
        cities = Counter()
        ips = []
        timezones = Counter()
        
        for session in self.data.get('sessions', []):
            system_info = session.get('system_info', {})
            
            if system_info.get('country'):
                countries[system_info['country']] += 1
            
            if system_info.get('location'):
                cities[system_info['location']] += 1
            
            if system_info.get('ip'):
                ips.append(system_info['ip'])
            
            if system_info.get('timezone'):
                timezones[system_info['timezone']] += 1
        
        # Analyze IP addresses
        ip_analysis = self.analyze_ip_addresses(ips)
        
        return {
            "total_countries": len(countries),
            "total_cities": len(cities),
            "total_timezones": len(timezones),
            "country_distribution": dict(countries.most_common(10)),
            "city_distribution": dict(cities.most_common(10)),
            "timezone_distribution": dict(timezones.most_common(5)),
            "unique_ips": len(set(ips)),
            "ip_analysis": ip_analysis,
            "most_affected_country": countries.most_common(1)[0] if countries else None,
            "most_affected_city": cities.most_common(1)[0] if cities else None
        }
    
    def analyze_ip_addresses(self, ips: List[str]) -> Dict[str, Any]:
        """Analyze IP address patterns"""
        private_ips = []
        public_ips = []
        ip_ranges = defaultdict(int)
        
        for ip in ips:
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.is_private:
                    private_ips.append(ip)
                else:
                    public_ips.append(ip)
                    # Group by /24 subnet
                    subnet = str(ip_obj).rsplit('.', 1)[0] + '.0/24'
                    ip_ranges[subnet] += 1
            except:
                pass
        
        return {
            "private_ips": len(private_ips),
            "public_ips": len(public_ips),
            "ip_ranges": dict(ip_ranges.most_common(5)),
            "sample_private_ips": private_ips[:5],
            "sample_public_ips": public_ips[:5]
        }
    
    def analyze_system_data(self) -> Dict[str, Any]:
        """Analyze system information"""
        logger.info("Analyzing system data...")
        
        operating_systems = Counter()
        languages = Counter()
        screen_sizes = Counter()
        hwids = Counter()
        antivirus_software = Counter()
        
        for session in self.data.get('sessions', []):
            system_info = session.get('system_info', {})
            
            if system_info.get('os'):
                operating_systems[system_info['os']] += 1
            
            if system_info.get('language'):
                languages[system_info['language']] += 1
            
            if system_info.get('screen_size'):
                screen_sizes[system_info['screen_size']] += 1
            
            if system_info.get('hwid'):
                hwids[system_info['hwid']] += 1
            
            if system_info.get('antivirus'):
                for av in system_info['antivirus']:
                    antivirus_software[av] += 1
        
        return {
            "operating_systems": dict(operating_systems),
            "languages": dict(languages),
            "screen_sizes": dict(screen_sizes),
            "hwid_analysis": {
                "unique_hwids": len(hwids),
                "duplicate_hwids": len([h for h in hwids.values() if h > 1]),
                "most_common_hwid": hwids.most_common(1)[0] if hwids else None
            },
            "antivirus_analysis": {
                "total_antivirus_instances": sum(antivirus_software.values()),
                "unique_antivirus_software": len(antivirus_software),
                "most_common_antivirus": dict(antivirus_software.most_common(5)),
                "systems_with_antivirus": len([s for s in self.data.get('sessions', []) 
                                             if s.get('system_info', {}).get('antivirus')])
            },
            "most_common_os": operating_systems.most_common(1)[0] if operating_systems else None,
            "most_common_language": languages.most_common(1)[0] if languages else None
        }
    
    def analyze_temporal_data(self) -> Dict[str, Any]:
        """Analyze temporal patterns"""
        logger.info("Analyzing temporal data...")
        
        dates = []
        time_patterns = defaultdict(int)
        
        for session in self.data.get('sessions', []):
            system_info = session.get('system_info', {})
            if system_info.get('log_date'):
                try:
                    # Parse various date formats
                    date_str = system_info['log_date']
                    # Add date parsing logic here
                    dates.append(date_str)
                    
                    # Analyze time patterns
                    if ':' in date_str:
                        hour = date_str.split(':')[0]
                        time_patterns[hour] += 1
                except:
                    pass
        
        return {
            "total_dates": len(dates),
            "unique_dates": len(set(dates)),
            "time_patterns": dict(time_patterns.most_common(5)),
            "date_range": {
                "earliest": min(dates) if dates else None,
                "latest": max(dates) if dates else None
            }
        }
    
    def analyze_security_data(self) -> Dict[str, Any]:
        """Analyze security-related information"""
        logger.info("Analyzing security data...")
        
        antivirus_info = []
        hwids = []
        exposed_credentials = []
        
        for session in self.data.get('sessions', []):
            system_info = session.get('system_info', {})
            
            if system_info.get('antivirus'):
                antivirus_info.extend(system_info['antivirus'])
            
            if system_info.get('hwid'):
                hwids.append(system_info['hwid'])
            
            # Check for exposed credentials
            for password_data in session.get('passwords', []):
                if password_data.get('url') and password_data.get('username') and password_data.get('password'):
                    exposed_credentials.append({
                        'url': password_data['url'],
                        'username': password_data['username'],
                        'session_id': session.get('session_id', 'Unknown'),
                        'stealer_type': session.get('stealer_type', 'Unknown')
                    })
        
        return {
            "antivirus_software": list(set(antivirus_info)),
            "unique_hwids": len(set(hwids)),
            "hwid_list": list(set(hwids)),
            "exposed_credentials": exposed_credentials,
            "total_exposed_credentials": len(exposed_credentials),
            "systems_with_antivirus": len([s for s in self.data.get('sessions', []) 
                                         if s.get('system_info', {}).get('antivirus')])
        }
    
    def analyze_threats(self) -> Dict[str, Any]:
        """Analyze security threats and risks"""
        logger.info("Analyzing security threats...")
        
        threats = []
        risk_score = 0
        
        # Analyze password threats
        password_analysis = self.analyze_passwords()
        if password_analysis['weak_password_percentage'] > 50:
            threats.append({
                'type': 'Weak Passwords',
                'severity': 'High',
                'description': f"{password_analysis['weak_password_percentage']:.1f}% of passwords are weak",
                'recommendation': 'Implement strong password policies'
            })
            risk_score += 30
        
        # Analyze high-risk passwords
        if password_analysis['high_risk_passwords']:
            threats.append({
                'type': 'High-Risk Credentials',
                'severity': 'Critical',
                'description': f"{len(password_analysis['high_risk_passwords'])} high-risk credentials exposed",
                'recommendation': 'Immediate password reset required'
            })
            risk_score += 50
        
        # Analyze geographic concentration
        geo_analysis = self.analyze_geographic_data()
        if geo_analysis['total_countries'] < 5:
            threats.append({
                'type': 'Geographic Concentration',
                'severity': 'Medium',
                'description': f"Attack concentrated in {geo_analysis['total_countries']} countries",
                'recommendation': 'Implement geo-blocking if necessary'
            })
            risk_score += 15
        
        return {
            "total_threats": len(threats),
            "risk_score": min(risk_score, 100),
            "threats": threats,
            "risk_level": self.get_risk_level(risk_score)
        }
    
    def get_risk_level(self, score: int) -> str:
        """Get risk level based on score"""
        if score >= 80:
            return "Critical"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Low"
        else:
            return "Minimal"
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive statistics"""
        logger.info("Generating statistics...")
        
        sessions = self.data.get('sessions', [])
        
        total_passwords = sum(len(s.get('passwords', [])) for s in sessions)
        total_cookies = sum(len(s.get('cookies', [])) for s in sessions)
        total_autofills = sum(len(s.get('autofills', [])) for s in sessions)
        total_files = sum(len(s.get('files', [])) for s in sessions)
        total_screenshots = sum(len(s.get('screenshots', [])) for s in sessions)
        
        stealer_types = Counter(s.get('stealer_type', 'Unknown') for s in sessions)
        
        return {
            "total_sessions": len(sessions),
            "total_passwords": total_passwords,
            "total_cookies": total_cookies,
            "total_autofills": total_autofills,
            "total_files": total_files,
            "total_screenshots": total_screenshots,
            "stealer_type_distribution": dict(stealer_types),
            "average_passwords_per_session": total_passwords / len(sessions) if sessions else 0,
            "average_cookies_per_session": total_cookies / len(sessions) if sessions else 0,
            "most_active_stealer": stealer_types.most_common(1)[0] if stealer_types else None
        }
    
    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate security recommendations"""
        recommendations = []
        
        # Password recommendations
        password_analysis = self.analyze_passwords()
        if password_analysis['weak_password_percentage'] > 30:
            recommendations.append({
                'category': 'Password Security',
                'priority': 'High',
                'recommendation': 'Implement strong password policies and multi-factor authentication',
                'details': f"{password_analysis['weak_password_percentage']:.1f}% of passwords are weak"
            })
        
        # Geographic recommendations
        geo_analysis = self.analyze_geographic_data()
        if geo_analysis['total_countries'] < 10:
            recommendations.append({
                'category': 'Geographic Security',
                'priority': 'Medium',
                'recommendation': 'Consider implementing geo-blocking for sensitive operations',
                'details': f"Attack concentrated in {geo_analysis['total_countries']} countries"
            })
        
        # System recommendations
        system_analysis = self.analyze_system_data()
        if system_analysis['antivirus_analysis']['systems_with_antivirus'] < len(self.data.get('sessions', [])) * 0.8:
            recommendations.append({
                'category': 'System Security',
                'priority': 'High',
                'recommendation': 'Ensure all systems have updated antivirus software',
                'details': f"Only {system_analysis['antivirus_analysis']['systems_with_antivirus']} systems have antivirus"
            })
        
        return recommendations
    
    def export_analysis_report(self, output_path: str) -> bool:
        """Export analysis report to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
            logger.info(f"Analysis report exported to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting analysis report: {e}")
            return False
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        stats = self.analysis_results.get('statistics', {})
        threats = self.analysis_results.get('threat_analysis', {})
        recommendations = self.analysis_results.get('recommendations', [])
        
        summary = f"""
=== LEAKED DATA ANALYSIS SUMMARY ===

📊 STATISTICS:
- Total Sessions Analyzed: {stats.get('total_sessions', 0)}
- Total Passwords Found: {stats.get('total_passwords', 0)}
- Total Cookies Found: {stats.get('total_cookies', 0)}
- Most Active Stealer: {stats.get('most_active_stealer', ['Unknown', 0])[0]}

🔒 SECURITY ANALYSIS:
- Risk Level: {threats.get('risk_level', 'Unknown')}
- Risk Score: {threats.get('risk_score', 0)}/100
- Total Threats Identified: {threats.get('total_threats', 0)}

�� RECOMMENDATIONS ({len(recommendations)}):
"""
        
        for i, rec in enumerate(recommendations, 1):
            summary += f"{i}. [{rec['priority']}] {rec['recommendation']}\n"
        
        return summary

def main():
    """Test the analyzer"""
    try:
        # Load sample data
        with open('unified_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create analyzer
        analyzer = DataAnalyzer(data)
        
        # Perform analysis
        results = analyzer.analyze_all()
        
        # Export results
        analyzer.export_analysis_report('analysis_report.json')
        
        # Generate summary
        summary = analyzer.generate_summary_report()
        print(summary)
        
        print("\n✅ Analysis completed successfully!")
        print(f"📄 Detailed report saved to: analysis_report.json")
        
    except FileNotFoundError:
        print("❌ Error: unified_data.json not found. Please run the parser first.")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()

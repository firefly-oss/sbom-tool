"""Security auditors - Copyright 2024 Firefly OSS"""
from typing import List, Dict, Any
import requests

class SecurityAuditor:
    def __init__(self, config):
        self.config = config
    
    def audit(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        vulnerabilities = []
        for component in components:
            # Simple vulnerability check using OSV API
            purl = component.get('purl')
            if purl:
                try:
                    response = requests.post(
                        'https://api.osv.dev/v1/query',
                        json={'package': {'purl': purl}},
                        timeout=5
                    )
                    if response.status_code == 200:
                        data = response.json()
                        for vuln in data.get('vulns', []):
                            vulnerabilities.append({
                                'id': vuln.get('id'),
                                'component': component['name'],
                                'severity': 'medium',
                                'description': vuln.get('summary', '')
                            })
                except Exception:
                    pass
        return vulnerabilities

__all__ = ['SecurityAuditor']

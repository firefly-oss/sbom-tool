#!/usr/bin/env python3
"""
Example script showing how to scan entire Firefly OSS organization

Copyright 2024 Firefly OSS
Licensed under the Apache License, Version 2.0
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from firefly_sbom import SBOMGenerator, Config
from firefly_sbom.utils import setup_logger

def main():
    """Main function to demonstrate SBOM scanning"""
    
    # Setup logging
    logger = setup_logger()
    
    # Create configuration
    config = Config({
        'scan': {
            'include_dev_dependencies': False,
            'parallel_workers': 4
        },
        'audit': {
            'vulnerability_databases': ['nvd', 'osv'],
            'fail_on_critical': True
        },
        'output': {
            'formats': ['cyclonedx-json', 'html'],
            'include_metadata': True
        }
    })
    
    # Initialize SBOM generator
    generator = SBOMGenerator(config)
    
    # Example 1: Scan a single repository
    print("\n=== Scanning Single Repository ===")
    repo_path = Path.cwd()
    
    sbom_data = generator.scan_repository(
        path=repo_path,
        include_dev=False,
        audit=True
    )
    
    # Generate reports
    for format_type in ['cyclonedx-json', 'html']:
        output_path = generator.generate_report(
            sbom_data=sbom_data,
            format=format_type,
            output_path=Path(f"example-sbom.{format_type.split('-')[-1]}")
        )
        print(f"Generated {format_type} report: {output_path}")
    
    # Display summary
    print(f"\nTotal components found: {len(sbom_data['components'])}")
    print(f"Technologies detected: {', '.join(sbom_data['metadata']['technologies'])}")
    
    if 'vulnerabilities' in sbom_data:
        print(f"Vulnerabilities found: {len(sbom_data['vulnerabilities'])}")
    
    # Example 2: Scan organization (requires GitHub token)
    if os.getenv('GITHUB_TOKEN'):
        print("\n=== Scanning Firefly OSS Organization ===")
        
        try:
            repos = generator.list_org_repositories('firefly-oss')
            print(f"Found {len(repos)} repositories")
            
            # Scan first 3 repositories as example
            for repo in repos[:3]:
                print(f"\nScanning: {repo['name']}")
                sbom_data = generator.scan_repository_url(
                    repo_url=repo['url'],
                    audit=True
                )
                print(f"  Components: {len(sbom_data['components'])}")
                
        except Exception as e:
            print(f"Error scanning organization: {e}")
    else:
        print("\n[INFO] Set GITHUB_TOKEN environment variable to scan GitHub organizations")
    
    # Example 3: Detect technology stack
    print("\n=== Technology Stack Detection ===")
    tech_stack = generator.detect_technology_stack(repo_path)
    
    for tech in tech_stack:
        print(f"\n{tech['name']}:")
        print(f"  Type: {tech['type']}")
        print(f"  Files: {', '.join(tech['files'][:3])}")


if __name__ == "__main__":
    main()

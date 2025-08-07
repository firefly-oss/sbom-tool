"""Report generators - Copyright 2024 Firefly OSS"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import OutputFormat, make_outputter
from cyclonedx.schema import SchemaVersion


class CycloneDXGenerator:
    def __init__(self, format_type):
        self.format_type = format_type

    def generate(self, sbom_data: Dict[str, Any], output_path: Path):
        bom = Bom()
        for comp in sbom_data.get("components", []):
            component = Component(name=comp["name"], version=comp.get("version"))
            bom.components.add(component)

        output_format = (
            OutputFormat.JSON if self.format_type == "json" else OutputFormat.XML
        )
        outputter = make_outputter(
            bom, output_format=output_format, schema_version=SchemaVersion.V1_6
        )
        with open(output_path, "w") as f:
            f.write(outputter.output_as_string())


class SPDXGenerator:
    def __init__(self, format_type):
        self.format_type = format_type

    def generate(self, sbom_data: Dict[str, Any], output_path: Path):
        spdx_doc = {
            "spdxVersion": "SPDX-2.3",
            "name": "SBOM Document",
            "packages": [
                {"name": c["name"], "version": c.get("version", "")}
                for c in sbom_data.get("components", [])
            ],
        }

        with open(output_path, "w") as f:
            if self.format_type == "json":
                json.dump(spdx_doc, f, indent=2)
            else:
                yaml.dump(spdx_doc, f)


class HTMLGenerator:
    def generate(self, sbom_data: Dict[str, Any], output_path: Path):
        """Generate pretty HTML report"""
        html = self._generate_html_report(sbom_data)
        with open(output_path, "w") as f:
            f.write(html)

    def generate_org_summary(self, org_summary: Dict[str, Any], output_path: Path):
        """Generate organization summary HTML report"""
        html = self._generate_org_html_report(org_summary)
        with open(output_path, "w") as f:
            f.write(html)

    def _generate_html_report(self, sbom_data: Dict[str, Any]) -> str:
        """Generate HTML content for SBOM report"""
        metadata = sbom_data.get("metadata", {})
        components = sbom_data.get("components", [])
        stats = sbom_data.get("stats", {})
        vulnerabilities = sbom_data.get("vulnerabilities", [])

        # Group components by type
        components_by_type = {}
        for comp in components:
            comp_type = comp.get("type", "library")
            if comp_type not in components_by_type:
                components_by_type[comp_type] = []
            components_by_type[comp_type].append(comp)

        # Generate vulnerability section if present
        vuln_html = ""
        if vulnerabilities:
            vuln_html = f"""
            <div class="vulnerabilities">
                <h2>🔒 Security Vulnerabilities ({len(vulnerabilities)})</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Component</th>
                            <th>Vulnerability ID</th>
                            <th>Severity</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'''
                        <tr class="severity-{v.get('severity', 'unknown')}">
                            <td>{v.get('component', 'Unknown')}</td>
                            <td>{v.get('id', 'Unknown')}</td>
                            <td><span class="badge severity-{v.get('severity', 'unknown')}">{v.get('severity', 'Unknown').upper()}</span></td>
                            <td>{v.get('description', '')}</td>
                        </tr>''' for v in vulnerabilities)}
                    </tbody>
                </table>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SBOM Report - {metadata.get('repository_name', 'Unknown')}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📦 Software Bill of Materials</h1>
            <div class="metadata">
                <p><strong>Repository:</strong> {metadata.get('repository_name', metadata.get('repository', 'Unknown'))}</p>
                <p><strong>Generated:</strong> {metadata.get('timestamp', datetime.now().isoformat())}</p>
                <p><strong>Technologies:</strong> {', '.join(metadata.get('technologies', ['None detected']))}</p>
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Components</h3>
                <div class="stat-number">{stats.get('total_components', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>Direct Dependencies</h3>
                <div class="stat-number">{stats.get('direct_deps', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>Transitive Dependencies</h3>
                <div class="stat-number">{stats.get('transitive_deps', 0)}</div>
            </div>
            {f'''
            <div class="stat-card warning">
                <h3>Vulnerabilities</h3>
                <div class="stat-number">{stats.get('vulnerabilities', 0)}</div>
            </div>''' if 'vulnerabilities' in stats else ''}
        </div>
        
        {vuln_html}
        
        <div class="components">
            <h2>📚 Components by Type</h2>
            {self._generate_component_tables(components_by_type)}
        </div>
        
        <footer>
            <p>Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0</p>
        </footer>
    </div>
</body>
</html>"""

    def _generate_component_tables(self, components_by_type: Dict[str, List]) -> str:
        """Generate HTML tables for components grouped by type"""
        html = ""
        for comp_type, components in sorted(components_by_type.items()):
            html += f"""
            <div class="component-group">
                <h3>{comp_type.title()} ({len(components)})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Version</th>
                            <th>License</th>
                            <th>Scope</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'''
                        <tr>
                            <td>{comp.get('name', 'Unknown')}</td>
                            <td>{comp.get('version', 'Unknown')}</td>
                            <td>{comp.get('license', 'Unknown')}</td>
                            <td><span class="badge scope-{comp.get('scope', 'unknown')}">{comp.get('scope', 'Unknown')}</span></td>
                        </tr>''' for comp in sorted(components, key=lambda x: x.get('name', '')))}
                    </tbody>
                </table>
            </div>
            """
        return html

    def _generate_org_html_report(self, org_summary: Dict[str, Any]) -> str:
        """Generate HTML content for organization summary"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organization SBOM Report - {org_summary.get('organization', 'Unknown')}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏢 Organization SBOM Summary</h1>
            <div class="metadata">
                <p><strong>Organization:</strong> {org_summary.get('organization', 'Unknown')}</p>
                <p><strong>Scan Date:</strong> {org_summary.get('scan_date', datetime.now().isoformat())}</p>
                <p><strong>Total Repositories:</strong> {org_summary.get('total_repositories', 0)}</p>
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Successful Scans</h3>
                <div class="stat-number">{org_summary.get('successful_scans', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>Total Components</h3>
                <div class="stat-number">{org_summary.get('total_components', 0)}</div>
            </div>
            <div class="stat-card warning">
                <h3>Total Vulnerabilities</h3>
                <div class="stat-number">{org_summary.get('total_vulnerabilities', 0)}</div>
            </div>
        </div>
        
        <div class="repositories">
            <h2>📂 Repository Summary</h2>
            <table>
                <thead>
                    <tr>
                        <th>Repository</th>
                        <th>Status</th>
                        <th>Components</th>
                        <th>Vulnerabilities</th>
                        <th>Technologies</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''
                    <tr>
                        <td>{repo.get('name', 'Unknown')}</td>
                        <td><span class="badge status-{repo.get('status', 'unknown')}">{repo.get('status', 'Unknown').upper()}</span></td>
                        <td>{repo.get('components', 0)}</td>
                        <td>{repo.get('vulnerabilities', 0)}</td>
                        <td>{', '.join(repo.get('technologies', []))}</td>
                    </tr>''' for repo in org_summary.get('repositories', []))}
                </tbody>
            </table>
        </div>
        
        <footer>
            <p>Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0</p>
        </footer>
    </div>
</body>
</html>"""

    def _get_css_styles(self) -> str:
        """Get CSS styles for HTML reports"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 20px; }
        h2 { color: #34495e; margin: 30px 0 20px; }
        h3 { color: #546e7a; margin: 20px 0 10px; }
        .metadata p { margin: 5px 0; color: #666; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-card h3 { font-size: 14px; color: #666; margin-bottom: 10px; }
        .stat-number { font-size: 32px; font-weight: bold; color: #2c3e50; }
        .stat-card.warning .stat-number { color: #e74c3c; }
        table { width: 100%; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0; }
        th { background: #34495e; color: white; padding: 12px; text-align: left; font-weight: 600; }
        td { padding: 12px; border-top: 1px solid #ecf0f1; }
        tr:hover { background: #f8f9fa; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
        .badge.scope-direct { background: #3498db; color: white; }
        .badge.scope-transitive { background: #95a5a6; color: white; }
        .badge.scope-dev { background: #9b59b6; color: white; }
        .badge.status-success { background: #27ae60; color: white; }
        .badge.status-failed { background: #e74c3c; color: white; }
        .badge.severity-critical { background: #c0392b; color: white; }
        .badge.severity-high { background: #e74c3c; color: white; }
        .badge.severity-medium { background: #f39c12; color: white; }
        .badge.severity-low { background: #3498db; color: white; }
        footer { text-align: center; margin-top: 50px; padding: 20px; color: #666; }
        .vulnerabilities { background: white; padding: 30px; border-radius: 10px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .component-group { margin: 20px 0; }
        """


class MarkdownGenerator:
    """Generate Markdown format reports"""

    def generate(self, sbom_data: Dict[str, Any], output_path: Path):
        """Generate Markdown SBOM report"""
        content = self._generate_markdown_report(sbom_data)
        with open(output_path, "w") as f:
            f.write(content)

    def generate_org_summary(self, org_summary: Dict[str, Any], output_path: Path):
        """Generate organization summary Markdown report"""
        content = self._generate_org_markdown_report(org_summary)
        with open(output_path, "w") as f:
            f.write(content)

    def _generate_markdown_report(self, sbom_data: Dict[str, Any]) -> str:
        """Generate Markdown content for SBOM report"""
        metadata = sbom_data.get("metadata", {})
        components = sbom_data.get("components", [])
        stats = sbom_data.get("stats", {})
        vulnerabilities = sbom_data.get("vulnerabilities", [])

        content = f"""# Software Bill of Materials

## 📋 Metadata

- **Repository**: {metadata.get('repository_name', metadata.get('repository', 'Unknown'))}
- **Generated**: {metadata.get('timestamp', datetime.now().isoformat())}
- **Technologies**: {', '.join(metadata.get('technologies', ['None detected']))}
- **Tool**: {metadata.get('tool', {}).get('name', 'Unknown')} v{metadata.get('tool', {}).get('version', 'Unknown')}

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Components | {stats.get('total_components', 0)} |
| Direct Dependencies | {stats.get('direct_deps', 0)} |
| Transitive Dependencies | {stats.get('transitive_deps', 0)} |
{f"| Vulnerabilities | {stats.get('vulnerabilities', 0)} |" if 'vulnerabilities' in stats else ''}

"""

        # Add vulnerabilities section if present
        if vulnerabilities:
            content += """## 🔒 Security Vulnerabilities

| Component | ID | Severity | Description |
|-----------|-------|----------|-------------|
"""
            for vuln in vulnerabilities:
                content += f"| {vuln.get('component', 'Unknown')} | {vuln.get('id', 'Unknown')} | {vuln.get('severity', 'Unknown').upper()} | {vuln.get('description', '')} |\n"
            content += "\n"

        # Add components section
        content += """## 📦 Components

| Name | Version | Type | License | Scope |
|------|---------|------|---------|-------|
"""
        for comp in sorted(components, key=lambda x: x.get("name", "")):
            content += f"| {comp.get('name', 'Unknown')} | {comp.get('version', 'Unknown')} | {comp.get('type', 'library')} | {comp.get('license', 'Unknown')} | {comp.get('scope', 'Unknown')} |\n"

        content += """\n---
*Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0*
"""

        return content

    def _generate_org_markdown_report(self, org_summary: Dict[str, Any]) -> str:
        """Generate Markdown content for organization summary"""
        content = f"""# Organization SBOM Summary

## 🏢 {org_summary.get('organization', 'Unknown')}

- **Scan Date**: {org_summary.get('scan_date', datetime.now().isoformat())}
- **Total Repositories**: {org_summary.get('total_repositories', 0)}
- **Successful Scans**: {org_summary.get('successful_scans', 0)}
- **Failed Scans**: {org_summary.get('failed_scans', 0)}

## 📊 Overall Statistics

| Metric | Value |
|--------|-------|
| Total Components | {org_summary.get('total_components', 0)} |
| Total Vulnerabilities | {org_summary.get('total_vulnerabilities', 0)} |

## 📂 Repository Summary

| Repository | Status | Components | Vulnerabilities | Technologies |
|------------|--------|------------|-----------------|-------------|
"""

        for repo in org_summary.get("repositories", []):
            content += f"| {repo.get('name', 'Unknown')} | {repo.get('status', 'Unknown').upper()} | {repo.get('components', 0)} | {repo.get('vulnerabilities', 0)} | {', '.join(repo.get('technologies', []))} |\n"

        content += """\n---
*Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0*
"""

        return content


class TextGenerator:
    """Generate plain text format reports"""

    def generate(self, sbom_data: Dict[str, Any], output_path: Path):
        """Generate text SBOM report"""
        content = self._generate_text_report(sbom_data)
        with open(output_path, "w") as f:
            f.write(content)

    def generate_org_summary(self, org_summary: Dict[str, Any], output_path: Path):
        """Generate organization summary text report"""
        content = self._generate_org_text_report(org_summary)
        with open(output_path, "w") as f:
            f.write(content)

    def _generate_text_report(self, sbom_data: Dict[str, Any]) -> str:
        """Generate plain text content for SBOM report"""
        metadata = sbom_data.get("metadata", {})
        components = sbom_data.get("components", [])
        stats = sbom_data.get("stats", {})

        content = f"""SOFTWARE BILL OF MATERIALS
{'=' * 60}

REPOSITORY: {metadata.get('repository_name', metadata.get('repository', 'Unknown'))}
GENERATED: {metadata.get('timestamp', datetime.now().isoformat())}
TECHNOLOGIES: {', '.join(metadata.get('technologies', ['None detected']))}

STATISTICS:
-----------
Total Components: {stats.get('total_components', 0)}
Direct Dependencies: {stats.get('direct_deps', 0)}
Transitive Dependencies: {stats.get('transitive_deps', 0)}
{f"Vulnerabilities: {stats.get('vulnerabilities', 0)}" if 'vulnerabilities' in stats else ''}

COMPONENTS:
-----------
"""

        for comp in sorted(components, key=lambda x: x.get("name", "")):
            content += f"{comp.get('name', 'Unknown')} @ {comp.get('version', 'Unknown')} [{comp.get('type', 'library')}] - {comp.get('license', 'Unknown')} ({comp.get('scope', 'Unknown')})\n"

        content += f"""\n{'=' * 60}
Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0
"""

        return content

    def _generate_org_text_report(self, org_summary: Dict[str, Any]) -> str:
        """Generate plain text content for organization summary"""
        content = f"""ORGANIZATION SBOM SUMMARY
{'=' * 60}

ORGANIZATION: {org_summary.get('organization', 'Unknown')}
SCAN DATE: {org_summary.get('scan_date', datetime.now().isoformat())}
TOTAL REPOSITORIES: {org_summary.get('total_repositories', 0)}

STATISTICS:
-----------
Successful Scans: {org_summary.get('successful_scans', 0)}
Failed Scans: {org_summary.get('failed_scans', 0)}
Total Components: {org_summary.get('total_components', 0)}
Total Vulnerabilities: {org_summary.get('total_vulnerabilities', 0)}

REPOSITORIES:
-------------
"""

        for repo in org_summary.get("repositories", []):
            content += f"{repo.get('name', 'Unknown')}: {repo.get('status', 'Unknown').upper()} - {repo.get('components', 0)} components, {repo.get('vulnerabilities', 0)} vulnerabilities\n"

        content += f"""\n{'=' * 60}
Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0
"""

        return content


__all__ = [
    "CycloneDXGenerator",
    "SPDXGenerator",
    "HTMLGenerator",
    "MarkdownGenerator",
    "TextGenerator",
]

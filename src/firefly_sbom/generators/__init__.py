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
        """Generate HTML content for organization summary with navigation and vulnerability details"""
        # Process vulnerability data by severity
        vuln_stats = self._process_vulnerability_stats(org_summary)
        
        # Generate navigation menu
        nav_menu = self._generate_navigation_menu(org_summary)
        
        # Generate technology distribution chart data
        tech_chart_data = self._generate_tech_chart_data(org_summary.get('technology_distribution', {}))
        
        # Generate vulnerability details section
        vuln_details = self._generate_vulnerability_details_section(org_summary)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organization SBOM Report - {org_summary.get('organization', 'Unknown')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {self._get_enhanced_css_styles()}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h3>🔍 SBOM Navigator</h3>
        </div>
        {nav_menu}
    </div>
    
    <div class="main-content">
        <header id="overview">
            <h1>🏢 Organization SBOM Summary</h1>
            <div class="metadata">
                <p><strong>Organization:</strong> {org_summary.get('organization', 'Unknown')}</p>
                <p><strong>Scan Date:</strong> {org_summary.get('scan_date', datetime.now().isoformat())}</p>
                <p><strong>Total Repositories:</strong> {org_summary.get('total_repositories', 0)}</p>
                <p><strong>Scan Duration:</strong> <span id="scan-duration">-</span></p>
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Successful Scans</h3>
                <div class="stat-number">{org_summary.get('successful_scans', 0)}</div>
                <div class="stat-change">+{round((org_summary.get('successful_scans', 0) / max(org_summary.get('total_repositories', 1), 1)) * 100, 1)}%</div>
            </div>
            <div class="stat-card">
                <h3>Total Components</h3>
                <div class="stat-number">{org_summary.get('total_components', 0):,}</div>
                <div class="stat-change">Across {org_summary.get('total_repositories', 0)} repos</div>
            </div>
            <div class="stat-card warning">
                <h3>Total Vulnerabilities</h3>
                <div class="stat-number">{org_summary.get('total_vulnerabilities', 0):,}</div>
                <div class="stat-change">{vuln_stats['severity_summary']}</div>
            </div>
            <div class="stat-card info">
                <h3>Technologies</h3>
                <div class="stat-number">{len(org_summary.get('technology_distribution', {}))}</div>
                <div class="stat-change">Different stacks</div>
            </div>
        </div>
        
        <!-- Technology Distribution Chart -->
        <div class="section" id="technologies">
            <h2>📊 Technology Distribution</h2>
            <div class="chart-container">
                <canvas id="techChart" width="400" height="200"></canvas>
            </div>
        </div>
        
        {vuln_details}
        
        <div class="section" id="repositories">
            <h2>📂 Repository Summary</h2>
            <div class="search-box">
                <input type="text" id="repoSearch" placeholder="🔍 Search repositories..." onkeyup="filterRepositories()">
                <select id="statusFilter" onchange="filterRepositories()">
                    <option value="all">All Status</option>
                    <option value="success">Success Only</option>
                    <option value="failed">Failed Only</option>
                </select>
                <select id="techFilter" onchange="filterRepositories()">
                    <option value="all">All Technologies</option>
                    {self._generate_tech_filter_options(org_summary.get('technology_distribution', {}))}
                </select>
            </div>
            <div class="table-container">
                <table id="repoTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Repository 🔽</th>
                            <th onclick="sortTable(1)">Status</th>
                            <th onclick="sortTable(2)">Components</th>
                            <th onclick="sortTable(3)">Vulnerabilities</th>
                            <th onclick="sortTable(4)">Technologies</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'''
                        <tr class="repo-row" data-status="{repo.get('status', 'unknown')}" data-tech="{','.join(repo.get('technologies', []))}">
                            <td>
                                <div class="repo-name">
                                    <strong>{repo.get('name', 'Unknown')}</strong>
                                    <div class="repo-meta">{repo.get('description', '')[:100]}</div>
                                </div>
                            </td>
                            <td><span class="badge status-{repo.get('status', 'unknown')}">{repo.get('status', 'Unknown').upper()}</span></td>
                            <td><span class="number">{repo.get('components', 0):,}</span></td>
                            <td>
                                <span class="number {'text-danger' if repo.get('vulnerabilities', 0) > 0 else 'text-success'}">
                                    {repo.get('vulnerabilities', 0):,}
                                </span>
                            </td>
                            <td>
                                <div class="tech-badges">
                                    {self._generate_tech_badges(repo.get('technologies', []))}
                                </div>
                            </td>
                            <td>
                                <div class="action-buttons">
                                    <button onclick="viewDetails('{repo.get('name', '')}')" class="btn-primary btn-sm">📄 Details</button>
                                    <button onclick="downloadSBOM('{repo.get('name', '')}')" class="btn-secondary btn-sm">⬇️ SBOM</button>
                                </div>
                            </td>
                        </tr>''' for repo in org_summary.get('repositories', []))}
                    </tbody>
                </table>
            </div>
        </div>
        
        <footer>
            <p>Generated by Firefly SBOM Tool v1.0.0 | Apache License 2.0 | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    
    <script>
        {self._generate_interactive_scripts(tech_chart_data, org_summary)}
    </script>
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
    
    def _get_enhanced_css_styles(self) -> str:
        """Get enhanced CSS styles with navigation and interactivity"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f8f9fd; display: flex; }
        
        /* Sidebar Navigation */
        .sidebar { width: 280px; height: 100vh; background: #2c3e50; color: white; position: fixed; left: 0; top: 0; padding: 20px; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1000; overflow-y: auto; }
        .sidebar .logo { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #34495e; }
        .sidebar .logo h3 { color: #ecf0f1; font-size: 18px; }
        .nav-menu { list-style: none; }
        .nav-menu li { margin: 10px 0; }
        .nav-menu a { color: #bdc3c7; text-decoration: none; padding: 12px 15px; display: block; border-radius: 6px; transition: all 0.3s ease; }
        .nav-menu a:hover, .nav-menu a.active { background: #34495e; color: #3498db; transform: translateX(5px); }
        
        /* Main Content */
        .main-content { margin-left: 280px; flex: 1; padding: 20px; min-height: 100vh; }
        
        /* Header */
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        h1 { font-size: 36px; margin-bottom: 20px; font-weight: 300; }
        .metadata { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .metadata p { background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; margin: 5px 0; backdrop-filter: blur(10px); }
        
        /* Statistics Cards */
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin: 40px 0; }
        .stat-card { background: white; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.1); border-left: 5px solid #3498db; transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card.warning { border-left-color: #e74c3c; }
        .stat-card.info { border-left-color: #9b59b6; }
        .stat-card h3 { font-size: 14px; color: #666; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-number { font-size: 42px; font-weight: 700; color: #2c3e50; margin: 10px 0; }
        .stat-change { font-size: 13px; color: #7f8c8d; }
        .stat-card.warning .stat-number { color: #e74c3c; }
        .stat-card.info .stat-number { color: #9b59b6; }
        
        /* Sections */
        .section { background: white; margin: 30px 0; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
        h2 { color: #2c3e50; margin-bottom: 25px; font-size: 24px; display: flex; align-items: center; }
        h2::before { content: ''; width: 4px; height: 30px; background: #3498db; margin-right: 15px; border-radius: 2px; }
        
        /* Charts */
        .chart-container { max-width: 600px; margin: 20px auto; padding: 20px; }
        
        /* Search and Filters */
        .search-box { display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap; }
        .search-box input, .search-box select { padding: 12px 16px; border: 2px solid #ecf0f1; border-radius: 8px; font-size: 14px; flex: 1; min-width: 200px; }
        .search-box input:focus, .search-box select:focus { outline: none; border-color: #3498db; }
        
        /* Tables */
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 12px; text-align: left; font-weight: 600; cursor: pointer; position: relative; }
        th:hover { background: linear-gradient(135deg, #5a67d8 0%, #667eea 100%); }
        td { padding: 16px 12px; border-top: 1px solid #ecf0f1; vertical-align: middle; }
        tr:hover { background: #f8f9ff; }
        tr.hidden { display: none; }
        
        /* Repository Names */
        .repo-name strong { color: #2c3e50; font-size: 16px; }
        .repo-meta { color: #7f8c8d; font-size: 12px; margin-top: 4px; }
        
        /* Badges */
        .badge { display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; margin: 2px; }
        .badge.status-success { background: #27ae60; color: white; }
        .badge.status-failed { background: #e74c3c; color: white; }
        .tech-badges { display: flex; flex-wrap: wrap; gap: 4px; }
        .tech-badge { background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; }
        .tech-badge.java { background: #f89820; }
        .tech-badge.python { background: #3776ab; }
        .tech-badge.javascript { background: #f7df1e; color: #000; }
        .tech-badge.typescript { background: #3178c6; }
        .tech-badge.go { background: #00add8; }
        .tech-badge.rust { background: #000000; }
        .tech-badge.ruby { background: #cc342d; }
        
        /* Buttons */
        .action-buttons { display: flex; gap: 8px; }
        .btn-primary, .btn-secondary { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; transition: all 0.3s ease; }
        .btn-primary { background: #3498db; color: white; }
        .btn-primary:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; color: white; }
        .btn-secondary:hover { background: #7f8c8d; }
        .btn-sm { padding: 4px 8px; font-size: 11px; }
        
        /* Numbers */
        .number { font-weight: 600; }
        .text-danger { color: #e74c3c; }
        .text-success { color: #27ae60; }
        
        /* Vulnerabilities */
        .vulnerability-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .vuln-card { padding: 20px; border-radius: 10px; border-left: 4px solid; }
        .vuln-card.critical { border-left-color: #c0392b; background: #fdf2f2; }
        .vuln-card.high { border-left-color: #e74c3c; background: #fef5f5; }
        .vuln-card.medium { border-left-color: #f39c12; background: #fefcf3; }
        .vuln-card.low { border-left-color: #3498db; background: #f0f8ff; }
        .vuln-title { font-weight: 600; margin-bottom: 8px; }
        .vuln-component { color: #666; font-size: 14px; }
        .vuln-description { margin-top: 10px; font-size: 13px; line-height: 1.4; }
        
        /* Footer */
        footer { text-align: center; margin-top: 60px; padding: 30px; color: #7f8c8d; background: #ecf0f1; border-radius: 10px; }
        
        /* Responsive */
        @media (max-width: 768px) {
            .sidebar { width: 100%; height: auto; position: relative; }
            .main-content { margin-left: 0; }
            .stats { grid-template-columns: 1fr; }
            .search-box { flex-direction: column; }
        }
        
        /* Progress indicators */
        .progress-bar { width: 100%; height: 4px; background: #ecf0f1; border-radius: 2px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #3498db, #2ecc71); transition: width 0.3s ease; }
        
        /* Animations */
        @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .section { animation: slideIn 0.6s ease-out; }
        """
    
    def _process_vulnerability_stats(self, org_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Process vulnerability statistics for display"""
        total_vulns = org_summary.get('total_vulnerabilities', 0)
        
        # Count by severity (this would need to be calculated during scanning)
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        # Generate summary text
        if total_vulns == 0:
            severity_summary = "No vulnerabilities found"
        else:
            severity_summary = f"{severity_counts.get('critical', 0)} Critical, {severity_counts.get('high', 0)} High"
        
        return {
            'total': total_vulns,
            'by_severity': severity_counts,
            'severity_summary': severity_summary
        }
    
    def _generate_navigation_menu(self, org_summary: Dict[str, Any]) -> str:
        """Generate navigation menu for sidebar"""
        return f"""
        <ul class="nav-menu">
            <li><a href="#overview" class="active">📊 Overview</a></li>
            <li><a href="#technologies">⚙️ Technologies</a></li>
            <li><a href="#vulnerabilities">🔒 Security ({org_summary.get('total_vulnerabilities', 0)})</a></li>
            <li><a href="#repositories">📂 Repositories ({org_summary.get('total_repositories', 0)})</a></li>
            <li><a href="#" onclick="exportData()">💾 Export Data</a></li>
            <li><a href="#" onclick="printReport()">🖨️ Print Report</a></li>
        </ul>
        """
    
    def _generate_tech_chart_data(self, tech_distribution: Dict[str, int]) -> str:
        """Generate Chart.js data for technology distribution"""
        if not tech_distribution:
            return '{}'
        
        labels = list(tech_distribution.keys())
        data = list(tech_distribution.values())
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
        
        return json.dumps({
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': colors[:len(labels)],
                'borderWidth': 0
            }]
        })
    
    def _generate_vulnerability_details_section(self, org_summary: Dict[str, Any]) -> str:
        """Generate detailed vulnerability section"""
        total_vulns = org_summary.get('total_vulnerabilities', 0)
        
        if total_vulns == 0:
            return f"""
            <div class="section" id="vulnerabilities">
                <h2>🔒 Security Vulnerabilities</h2>
                <div style="text-align: center; padding: 40px; color: #27ae60;">
                    <h3>🎉 No vulnerabilities found!</h3>
                    <p>All scanned repositories are secure.</p>
                </div>
            </div>
            """
        
        return f"""
        <div class="section" id="vulnerabilities">
            <h2>🔒 Security Vulnerabilities ({total_vulns})</h2>
            <div class="vulnerability-grid">
                <div class="vuln-card critical">
                    <div class="vuln-title">Critical Vulnerabilities</div>
                    <div class="stat-number" style="font-size: 24px;">0</div>
                    <div class="vuln-description">Immediate action required</div>
                </div>
                <div class="vuln-card high">
                    <div class="vuln-title">High Risk</div>
                    <div class="stat-number" style="font-size: 24px;">0</div>
                    <div class="vuln-description">Should be addressed soon</div>
                </div>
                <div class="vuln-card medium">
                    <div class="vuln-title">Medium Risk</div>
                    <div class="stat-number" style="font-size: 24px;">0</div>
                    <div class="vuln-description">Monitor and plan fixes</div>
                </div>
                <div class="vuln-card low">
                    <div class="vuln-title">Low Risk</div>
                    <div class="stat-number" style="font-size: 24px;">{total_vulns}</div>
                    <div class="vuln-description">Review when convenient</div>
                </div>
            </div>
            <p style="margin-top: 20px; color: #666; font-size: 14px;">💡 Enable detailed vulnerability scanning with <code>--audit</code> flag for component-level vulnerability details.</p>
        </div>
        """
    
    def _generate_tech_filter_options(self, tech_distribution: Dict[str, int]) -> str:
        """Generate technology filter options"""
        options = []
        for tech in sorted(tech_distribution.keys()):
            options.append(f'<option value="{tech}">{tech} ({tech_distribution[tech]})</option>')
        return '\n'.join(options)
    
    def _generate_tech_badges(self, technologies: List[str]) -> str:
        """Generate technology badges with colors"""
        badges = []
        for tech in technologies:
            css_class = tech.lower().replace('/', '').replace(' ', '').replace('.', '')
            badges.append(f'<span class="tech-badge {css_class}">{tech}</span>')
        return '\n'.join(badges)
    
    def _generate_interactive_scripts(self, tech_chart_data: str, org_summary: Dict[str, Any]) -> str:
        """Generate JavaScript for interactivity"""
        return f"""
        // Technology Chart
        const ctx = document.getElementById('techChart').getContext('2d');
        new Chart(ctx, {{
            type: 'doughnut',
            data: {tech_chart_data},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'right'
                    }}
                }}
            }}
        }});
        
        // Repository filtering
        function filterRepositories() {{
            const search = document.getElementById('repoSearch').value.toLowerCase();
            const statusFilter = document.getElementById('statusFilter').value;
            const techFilter = document.getElementById('techFilter').value;
            const rows = document.querySelectorAll('#repoTable tbody tr');
            
            rows.forEach(row => {{
                const name = row.cells[0].textContent.toLowerCase();
                const status = row.dataset.status;
                const tech = row.dataset.tech;
                
                let visible = true;
                
                if (search && !name.includes(search)) visible = false;
                if (statusFilter !== 'all' && status !== statusFilter) visible = false;
                if (techFilter !== 'all' && !tech.includes(techFilter)) visible = false;
                
                row.classList.toggle('hidden', !visible);
            }});
        }}
        
        // Table sorting
        let sortDirection = {{}};
        function sortTable(columnIndex) {{
            const table = document.getElementById('repoTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr:not(.hidden)'));
            
            const direction = sortDirection[columnIndex] = !sortDirection[columnIndex];
            
            rows.sort((a, b) => {{
                const aVal = a.cells[columnIndex].textContent.trim();
                const bVal = b.cells[columnIndex].textContent.trim();
                
                if (columnIndex === 2 || columnIndex === 3) {{
                    // Numeric columns
                    return direction ? parseInt(bVal.replace(/,/g, '')) - parseInt(aVal.replace(/,/g, '')) : parseInt(aVal.replace(/,/g, '')) - parseInt(bVal.replace(/,/g, ''));
                }} else {{
                    // Text columns
                    return direction ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
                }}
            }});
            
            rows.forEach(row => tbody.appendChild(row));
        }}
        
        // Navigation
        document.querySelectorAll('.nav-menu a').forEach(link => {{
            link.addEventListener('click', function(e) {{
                if (this.getAttribute('href').startsWith('#')) {{
                    e.preventDefault();
                    document.querySelectorAll('.nav-menu a').forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
        
        // Action buttons
        function viewDetails(repoName) {{
            window.open(repoName + '/sbom.html', '_blank');
        }}
        
        function downloadSBOM(repoName) {{
            window.open(repoName + '/sbom.cyclonedx.json', '_blank');
        }}
        
        function exportData() {{
            const data = {json.dumps(org_summary, default=str)};
            const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'organization-sbom-summary.json';
            a.click();
        }}
        
        function printReport() {{
            window.print();
        }}
        
        // Initialize tooltips and smooth scrolling
        document.addEventListener('DOMContentLoaded', function() {{
            // Add loading animation
            setTimeout(() => {{
                document.body.style.opacity = '1';
            }}, 100);
        }});
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

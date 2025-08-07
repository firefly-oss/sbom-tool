"""
Maven scanner for Java/Spring Boot projects

Copyright 2024 Firefly OSS
Licensed under the Apache License, Version 2.0
"""

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.logger import get_logger
from .base import Scanner

logger = get_logger(__name__)


class MavenScanner(Scanner):
    """Scanner for Maven-based Java projects including multi-module projects"""

    def detect(self, path: Path) -> bool:
        """Detect if this is a Maven project"""
        return (path / "pom.xml").exists()

    def scan(self, path: Path, include_dev: bool = False) -> List[Dict[str, Any]]:
        """Scan Maven project for dependencies"""
        components = []

        # Check if Maven is available
        if not self._is_maven_available():
            logger.warning("Maven not found, falling back to POM parsing")
            return self._parse_pom_files(path, include_dev)

        # Try to use Maven dependency tree
        try:
            components = self._scan_with_maven(path, include_dev)
        except Exception as e:
            logger.warning(f"Maven scan failed: {e}, falling back to POM parsing")
            components = self._parse_pom_files(path, include_dev)

        return components

    def _is_maven_available(self) -> bool:
        """Check if Maven is available in the system"""
        try:
            result = subprocess.run(
                ["mvn", "--version"], capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _scan_with_maven(self, path: Path, include_dev: bool) -> List[Dict[str, Any]]:
        """Scan using Maven dependency:tree command"""
        components = []

        # Build Maven command
        cmd = [
            "mvn",
            "dependency:tree",
            "-DoutputType=json",
            "-DoutputFile=dependency-tree.json",
        ]

        if not include_dev:
            cmd.append("-Dscope=compile,runtime")

        # Run Maven command
        logger.info(f"Running Maven dependency analysis in {path}")
        result = subprocess.run(
            cmd,
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=self.config.timeout,
        )

        if result.returncode != 0:
            raise Exception(f"Maven command failed: {result.stderr}")

        # Parse dependency tree
        dep_file = path / "dependency-tree.json"
        if dep_file.exists():
            try:
                with open(dep_file, "r") as f:
                    dep_data = json.load(f)

                components = self._parse_maven_tree(dep_data, include_dev)

                # Clean up
                dep_file.unlink()
            except Exception as e:
                logger.error(f"Error parsing Maven dependency tree: {e}")

        # If no JSON output, try text parsing
        if not components:
            components = self._parse_maven_text_tree(path, include_dev)

        return components

    def _parse_maven_tree(
        self, tree_data: Dict, include_dev: bool
    ) -> List[Dict[str, Any]]:
        """Parse Maven dependency tree JSON"""
        components = []

        if isinstance(tree_data, dict):
            # Process main artifact
            self._process_maven_artifact(tree_data, components, include_dev)
        elif isinstance(tree_data, list):
            for artifact in tree_data:
                self._process_maven_artifact(artifact, components, include_dev)

        return components

    def _process_maven_artifact(
        self, artifact: Dict, components: List, include_dev: bool, scope: str = "direct"
    ):
        """Process a single Maven artifact"""
        group_id = artifact.get("groupId", "")
        artifact_id = artifact.get("artifactId", "")
        version = artifact.get("version", "")
        artifact_scope = artifact.get("scope", "compile")

        # Skip if development dependency and not included
        if not include_dev and self._is_dev_dependency(artifact_scope):
            return

        # Create component
        component = self.create_component(
            name=artifact_id,
            version=version,
            type="library",
            scope=scope,
            group=group_id,
            purl=f"pkg:maven/{group_id}/{artifact_id}@{version}",
        )

        components.append(component)

        # Process children (transitive dependencies)
        if "children" in artifact:
            for child in artifact["children"]:
                self._process_maven_artifact(
                    child, components, include_dev, "transitive"
                )

    def _parse_maven_text_tree(
        self, path: Path, include_dev: bool
    ) -> List[Dict[str, Any]]:
        """Parse Maven dependency tree text output"""
        components = []

        # Run Maven dependency:tree in text mode
        cmd = ["mvn", "dependency:tree"]
        if not include_dev:
            cmd.extend(["-Dscope=compile,runtime"])

        result = subprocess.run(
            cmd,
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=self.config.timeout,
        )

        if result.returncode == 0:
            components = self._parse_dependency_tree_text(result.stdout, include_dev)

        return components

    def _parse_dependency_tree_text(
        self, tree_text: str, include_dev: bool
    ) -> List[Dict[str, Any]]:
        """Parse Maven dependency tree text format"""
        components = []

        # Pattern to match Maven coordinates
        pattern = r"([a-zA-Z0-9\.\-_]+):([a-zA-Z0-9\.\-_]+):([a-zA-Z0-9\.\-_]+):([a-zA-Z0-9\.\-_]+):([a-zA-Z0-9\.\-_]+)"

        for line in tree_text.split("\n"):
            match = re.search(pattern, line)
            if match:
                group_id = match.group(1)
                artifact_id = match.group(2)
                packaging = match.group(3)
                version = match.group(4)
                scope = match.group(5)

                # Skip if development dependency and not included
                if not include_dev and self._is_dev_dependency(scope):
                    continue

                # Determine if direct or transitive
                dep_scope = "direct" if line.startswith("[INFO] +-") else "transitive"

                component = self.create_component(
                    name=artifact_id,
                    version=version,
                    type="library",
                    scope=dep_scope,
                    group=group_id,
                    purl=f"pkg:maven/{group_id}/{artifact_id}@{version}",
                )

                components.append(component)

        return components

    def _parse_pom_files(self, path: Path, include_dev: bool) -> List[Dict[str, Any]]:
        """Parse POM files directly when Maven is not available"""
        components = []

        # Find all POM files (for multi-module projects)
        pom_files = list(path.rglob("pom.xml"))

        for pom_file in pom_files:
            try:
                components.extend(self._parse_single_pom(pom_file, include_dev))
            except Exception as e:
                logger.error(f"Error parsing POM file {pom_file}: {e}")

        return components

    def _parse_single_pom(
        self, pom_file: Path, include_dev: bool
    ) -> List[Dict[str, Any]]:
        """Parse a single POM file"""
        components = []

        try:
            tree = ET.parse(pom_file)
            root = tree.getroot()

            # Handle namespace
            ns = {"m": "http://maven.apache.org/POM/4.0.0"}

            # Parse dependencies
            dependencies = root.findall(".//m:dependencies/m:dependency", ns)
            if not dependencies:
                # Try without namespace
                dependencies = root.findall(".//dependencies/dependency")

            for dep in dependencies:
                group_id = self._get_element_text(dep, "groupId", ns)
                artifact_id = self._get_element_text(dep, "artifactId", ns)
                version = self._get_element_text(dep, "version", ns)
                scope = self._get_element_text(dep, "scope", ns) or "compile"

                # Skip if development dependency and not included
                if not include_dev and self._is_dev_dependency(scope):
                    continue

                # Skip if version contains property placeholder
                if version and not version.startswith("${"):
                    component = self.create_component(
                        name=artifact_id,
                        version=version,
                        type="library",
                        scope="direct",
                        group=group_id,
                        purl=f"pkg:maven/{group_id}/{artifact_id}@{version}",
                    )

                    components.append(component)

        except ET.ParseError as e:
            logger.error(f"Error parsing XML in {pom_file}: {e}")

        return components

    def _get_element_text(self, parent, tag: str, ns: Dict) -> Optional[str]:
        """Get text from XML element with namespace handling"""
        elem = parent.find(f"m:{tag}", ns)
        if elem is None:
            elem = parent.find(tag)

        return elem.text if elem is not None else None

    def _generate_purl(
        self, name: str, version: str, group: Optional[str] = None
    ) -> str:
        """Generate Maven-specific Package URL"""
        if group:
            return f"pkg:maven/{group}/{name}@{version}"
        return f"pkg:maven/{name}@{version}"

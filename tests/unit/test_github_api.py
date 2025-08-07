"""
Unit tests for GitHub API utility module

Copyright 2024 Firefly OSS
Licensed under the Apache License, Version 2.0
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import RequestException

from firefly_sbom.utils.github import GitHubAPI, GitHubAPIError


class TestGitHubAPI:
    """Test GitHub API client functionality"""

    def test_init_with_token(self):
        """Test GitHub API initialization with token"""
        api = GitHubAPI(token="test-token")
        assert api.token == "test-token"
        assert "Authorization" in api.session.headers
        assert api.session.headers["Authorization"] == "token test-token"

    def test_init_without_token(self):
        """Test GitHub API initialization without token"""
        with patch.dict("os.environ", {}, clear=True):
            api = GitHubAPI()
            assert api.token is None
            assert "Authorization" not in api.session.headers

    @patch.dict("os.environ", {"GITHUB_TOKEN": "env-token"})
    def test_init_with_env_token(self):
        """Test GitHub API initialization with environment token"""
        api = GitHubAPI()
        assert api.token == "env-token"

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_make_request_success(self, mock_get):
        """Test successful API request"""
        api = GitHubAPI(token="test-token")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        result = api._make_request("https://api.github.com/test")
        
        assert result == {"test": "data"}
        mock_get.assert_called_once()

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_make_request_401_error(self, mock_get):
        """Test API request with authentication error"""
        api = GitHubAPI(token="invalid-token")
        
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Bad credentials"
        mock_get.return_value = mock_response
        
        with pytest.raises(GitHubAPIError, match="Authentication failed"):
            api._make_request("https://api.github.com/test")

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_make_request_403_error(self, mock_get):
        """Test API request with forbidden error"""
        api = GitHubAPI(token="test-token")
        
        # Mock 403 response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = mock_response
        
        with pytest.raises(GitHubAPIError, match="Access forbidden"):
            api._make_request("https://api.github.com/test")

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_make_request_404_error(self, mock_get):
        """Test API request with not found error"""
        api = GitHubAPI(token="test-token")
        
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        with pytest.raises(GitHubAPIError, match="Resource not found"):
            api._make_request("https://api.github.com/test")

    @patch('firefly_sbom.utils.github.requests.Session.get')
    @patch('firefly_sbom.utils.github.time.sleep')
    @patch('firefly_sbom.utils.github.time.time')
    def test_make_request_rate_limit(self, mock_time, mock_sleep, mock_get):
        """Test API request with rate limiting"""
        api = GitHubAPI(token="test-token")
        
        # Mock current time to control rate limit calculation
        mock_time.return_value = 1234567800  # 90 seconds before reset time
        
        # Mock rate limit response followed by success
        rate_limit_response = Mock()
        rate_limit_response.status_code = 403
        rate_limit_response.text = "rate limit exceeded"
        rate_limit_response.headers = {"X-RateLimit-Reset": "1234567890"}  # Reset in 90 seconds
        
        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = {"test": "data"}
        
        mock_get.side_effect = [rate_limit_response, success_response]
        
        result = api._make_request("https://api.github.com/test")
        
        assert result == {"test": "data"}
        assert mock_get.call_count == 2
        mock_sleep.assert_called_once_with(91)  # 90 + 1 seconds

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_get_organization_repositories(self, mock_get):
        """Test getting organization repositories"""
        api = GitHubAPI(token="test-token")
        
        # Mock API responses for pagination - first page has data, second page is empty
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = [
            {
                "name": "repo1",
                "full_name": "org/repo1",
                "private": False,
                "fork": False,
                "archived": False,
                "clone_url": "https://github.com/org/repo1.git",
                "ssh_url": "git@github.com:org/repo1.git",
                "html_url": "https://github.com/org/repo1",
                "description": "Test repository 1",
                "language": "Python",
                "size": 1024,
                "updated_at": "2024-01-01T00:00:00Z",
                "topics": ["test", "python"],
                "default_branch": "main"
            },
            {
                "name": "repo2",
                "full_name": "org/repo2",
                "private": True,
                "fork": True,
                "archived": True,
                "clone_url": "https://github.com/org/repo2.git",
                "ssh_url": "git@github.com:org/repo2.git",
                "html_url": "https://github.com/org/repo2",
                "description": "Test repository 2",
                "language": "JavaScript",
                "size": 2048,
                "updated_at": "2024-01-02T00:00:00Z",
                "topics": ["test", "js"],
                "default_branch": "master"
            }
        ]
        
        # Second response is empty to break pagination loop
        empty_response = Mock()
        empty_response.status_code = 200
        empty_response.json.return_value = []
        
        mock_get.side_effect = [first_response, empty_response]
        
        repos = api.get_organization_repositories("test-org")
        
        assert len(repos) == 1  # Only repo1 is included (repo2 is filtered out due to being private=True, fork=True, archived=True)
        assert repos[0]["name"] == "repo1"
        assert repos[0]["private"] is False

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_get_organization_repositories_with_filters(self, mock_get):
        """Test getting organization repositories with filters applied"""
        api = GitHubAPI(token="test-token")
        
        # Mock API response with mixed repositories - first page
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = [
            {
                "name": "public-repo",
                "full_name": "test-org/public-repo",
                "private": False,
                "fork": False,
                "archived": False,
                "language": "Python",
                "clone_url": "https://github.com/test-org/public-repo.git",
                "ssh_url": "git@github.com:test-org/public-repo.git",
                "html_url": "https://github.com/test-org/public-repo",
                "description": "Public repository",
                "size": 1024,
                "updated_at": "2024-01-01T00:00:00Z",
                "topics": ["public"],
                "default_branch": "main"
            },
            {
                "name": "private-repo",
                "full_name": "test-org/private-repo",
                "private": True,
                "fork": False,
                "archived": False,
                "language": "Python",
                "clone_url": "https://github.com/test-org/private-repo.git",
                "ssh_url": "git@github.com:test-org/private-repo.git",
                "html_url": "https://github.com/test-org/private-repo",
                "description": "Private repository",
                "size": 2048,
                "updated_at": "2024-01-02T00:00:00Z",
                "topics": ["private"],
                "default_branch": "main"
            },
            {
                "name": "fork-repo",
                "full_name": "test-org/fork-repo",
                "private": False,
                "fork": True,
                "archived": False,
                "language": "JavaScript",
                "clone_url": "https://github.com/test-org/fork-repo.git",
                "ssh_url": "git@github.com:test-org/fork-repo.git",
                "html_url": "https://github.com/test-org/fork-repo",
                "description": "Forked repository",
                "size": 512,
                "updated_at": "2024-01-03T00:00:00Z",
                "topics": ["fork"],
                "default_branch": "main"
            },
            {
                "name": "archived-repo",
                "full_name": "test-org/archived-repo",
                "private": False,
                "fork": False,
                "archived": True,
                "language": "Python",
                "clone_url": "https://github.com/test-org/archived-repo.git",
                "ssh_url": "git@github.com:test-org/archived-repo.git",
                "html_url": "https://github.com/test-org/archived-repo",
                "description": "Archived repository",
                "size": 256,
                "updated_at": "2024-01-04T00:00:00Z",
                "topics": ["archived"],
                "default_branch": "main"
            }
        ]
        
        # Empty second page to break pagination
        empty_response = Mock()
        empty_response.status_code = 200
        empty_response.json.return_value = []
        
        mock_get.side_effect = [first_response, empty_response]
        
        # Test with filters
        repos = api.get_organization_repositories(
            "test-org",
            include_private=False,
            include_forks=False,
            include_archived=False
        )
        
        # Should only include public-repo
        assert len(repos) == 1
        assert repos[0]["name"] == "public-repo"

    def test_filter_repositories(self):
        """Test repository filtering functionality"""
        api = GitHubAPI()
        
        repos = [
            {
                "name": "python-app",
                "language": "Python",
                "topics": ["web", "api"],
                "size": 1024
            },
            {
                "name": "js-frontend",
                "language": "JavaScript",
                "topics": ["frontend", "react"],
                "size": 2048
            },
            {
                "name": "go-service",
                "language": "Go",
                "topics": ["microservice", "api"],
                "size": 512
            }
        ]
        
        # Test language filter
        filtered = api.filter_repositories(repos, languages=["Python"])
        assert len(filtered) == 1
        assert filtered[0]["name"] == "python-app"
        
        # Test topics filter
        filtered = api.filter_repositories(repos, topics=["api"])
        assert len(filtered) == 2
        assert {r["name"] for r in filtered} == {"python-app", "go-service"}
        
        # Test size filter
        filtered = api.filter_repositories(repos, min_size_kb=1000)
        assert len(filtered) == 2
        assert {r["name"] for r in filtered} == {"python-app", "js-frontend"}
        
        # Test include patterns
        filtered = api.filter_repositories(repos, include_patterns=["python-*", "*-service"])
        assert len(filtered) == 2
        assert {r["name"] for r in filtered} == {"python-app", "go-service"}
        
        # Test exclude patterns  
        filtered = api.filter_repositories(repos, exclude_patterns=["*-frontend"])
        assert len(filtered) == 2
        assert {r["name"] for r in filtered} == {"python-app", "go-service"}

    def test_get_clone_url_public_repo(self):
        """Test getting clone URL for public repository"""
        api = GitHubAPI()
        
        repo = {
            "private": False,
            "clone_url": "https://github.com/org/repo.git",
            "ssh_url": "git@github.com:org/repo.git"
        }
        
        # HTTPS URL for public repo
        url = api.get_clone_url(repo, use_ssh=False)
        assert url == "https://github.com/org/repo.git"
        
        # SSH URL
        url = api.get_clone_url(repo, use_ssh=True)
        assert url == "git@github.com:org/repo.git"

    def test_get_clone_url_private_repo_with_token(self):
        """Test getting clone URL for private repository with token"""
        api = GitHubAPI(token="test-token")
        
        repo = {
            "private": True,
            "clone_url": "https://github.com/org/repo.git",
            "ssh_url": "git@github.com:org/repo.git"
        }
        
        # Should inject token into HTTPS URL
        url = api.get_clone_url(repo, use_ssh=False)
        assert url == "https://test-token@github.com/org/repo.git"

    def test_get_clone_url_private_repo_without_token(self):
        """Test getting clone URL for private repository without token"""
        api = GitHubAPI()
        
        repo = {
            "private": True,
            "clone_url": "https://github.com/org/repo.git",
            "ssh_url": "git@github.com:org/repo.git"
        }
        
        # Should return original URL (will likely fail during clone)
        url = api.get_clone_url(repo, use_ssh=False)
        assert url == "https://github.com/org/repo.git"

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_validate_access_success(self, mock_get):
        """Test successful access validation"""
        api = GitHubAPI(token="test-token")
        
        # Mock organization access
        org_response = Mock()
        org_response.status_code = 200
        org_response.json.return_value = {"login": "test-org"}
        
        # Mock private repos access
        private_response = Mock()
        private_response.status_code = 200
        private_response.json.return_value = [{"name": "private-repo"}]
        
        mock_get.side_effect = [org_response, private_response, private_response]
        
        capabilities = api.validate_access("test-org")
        
        assert capabilities["org_access"] is True
        assert capabilities["private_repos"] is True

    @patch('firefly_sbom.utils.github.requests.Session.get')
    def test_validate_access_no_org_access(self, mock_get):
        """Test access validation with no organization access"""
        api = GitHubAPI()
        
        # Mock 404 organization response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        capabilities = api.validate_access("nonexistent-org")
        
        assert capabilities["org_access"] is False
        assert capabilities["private_repos"] is False

    def test_github_api_error(self):
        """Test custom GitHubAPIError exception"""
        with pytest.raises(GitHubAPIError):
            raise GitHubAPIError("Test error message")
        
        try:
            raise GitHubAPIError("Test error message")
        except GitHubAPIError as e:
            assert str(e) == "Test error message"

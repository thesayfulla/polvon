"""Tests for the TUI search functionality."""

import unittest
from unittest.mock import MagicMock, patch
from polvon.tui import PolvonApp
from polvon.service import Service, ServiceState, ServiceLoadState


class TestTUISearch(unittest.TestCase):
    """Test cases for TUI search functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = PolvonApp(use_sudo=False)
        
        # Create test services
        self.test_services = [
            Service(
                name="nginx.service",
                load_state=ServiceLoadState.LOADED,
                active_state=ServiceState.ACTIVE,
                sub_state="running",
                description="A high performance web server",
                enabled=True
            ),
            Service(
                name="apache2.service",
                load_state=ServiceLoadState.LOADED,
                active_state=ServiceState.INACTIVE,
                sub_state="dead",
                description="The Apache HTTP Server",
                enabled=False
            ),
            Service(
                name="ssh.service",
                load_state=ServiceLoadState.LOADED,
                active_state=ServiceState.ACTIVE,
                sub_state="running",
                description="OpenSSH server daemon",
                enabled=True
            ),
            Service(
                name="mysql.service",
                load_state=ServiceLoadState.LOADED,
                active_state=ServiceState.FAILED,
                sub_state="failed",
                description="MySQL Database Server",
                enabled=True
            ),
        ]

    def test_filter_services_empty_query(self):
        """Test filtering services with empty query returns all services."""
        self.app.services = self.test_services
        self.app.search_query = ""
        self.app.filter_services()
        
        self.assertEqual(len(self.app.filtered_services), 4)
        self.assertEqual(self.app.filtered_services, self.test_services)

    def test_filter_services_by_name(self):
        """Test filtering services by name."""
        self.app.services = self.test_services
        self.app.search_query = "nginx"
        self.app.filter_services()
        
        self.assertEqual(len(self.app.filtered_services), 1)
        self.assertEqual(self.app.filtered_services[0].name, "nginx.service")

    def test_filter_services_by_description(self):
        """Test filtering services by description."""
        self.app.services = self.test_services
        self.app.search_query = "server"
        self.app.filter_services()
        
        # Should match nginx (web server), apache (HTTP Server), ssh (server daemon), mysql (Server)
        self.assertEqual(len(self.app.filtered_services), 4)

    def test_filter_services_case_insensitive(self):
        """Test filtering is case insensitive."""
        self.app.services = self.test_services
        self.app.search_query = "NGINX"
        self.app.filter_services()
        
        self.assertEqual(len(self.app.filtered_services), 1)
        self.assertEqual(self.app.filtered_services[0].name, "nginx.service")

    def test_filter_services_partial_match(self):
        """Test filtering with partial match."""
        self.app.services = self.test_services
        self.app.search_query = "apach"
        self.app.filter_services()
        
        self.assertEqual(len(self.app.filtered_services), 1)
        self.assertEqual(self.app.filtered_services[0].name, "apache2.service")

    def test_filter_services_no_match(self):
        """Test filtering with no matching services."""
        self.app.services = self.test_services
        self.app.search_query = "nonexistent"
        self.app.filter_services()
        
        self.assertEqual(len(self.app.filtered_services), 0)

    def test_filter_services_multiple_matches(self):
        """Test filtering with multiple matches."""
        self.app.services = self.test_services
        self.app.search_query = "http"
        self.app.filter_services()
        
        # Should match apache2 (HTTP Server)
        self.assertEqual(len(self.app.filtered_services), 1)
        self.assertEqual(self.app.filtered_services[0].name, "apache2.service")

    def test_filter_services_with_none_description(self):
        """Test filtering services when description is None."""
        service_with_none = Service(
            name="test.service",
            load_state=ServiceLoadState.LOADED,
            active_state=ServiceState.ACTIVE,
            sub_state="running",
            description=None,
            enabled=True
        )
        self.app.services = [service_with_none]
        self.app.search_query = "test"
        self.app.filter_services()
        
        # Should match by name even though description is None
        self.assertEqual(len(self.app.filtered_services), 1)
        self.assertEqual(self.app.filtered_services[0].name, "test.service")


if __name__ == '__main__':
    unittest.main()

"""Tests for the service management module."""

import unittest
from unittest.mock import patch, MagicMock
from polvon.service import ServiceManager, Service, ServiceState, ServiceLoadState


class TestServiceManager(unittest.TestCase):
    """Test cases for ServiceManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = ServiceManager(use_sudo=False)

    def test_init(self):
        """Test ServiceManager initialization."""
        manager = ServiceManager(use_sudo=False)
        self.assertFalse(manager.use_sudo)
        
        manager_with_sudo = ServiceManager(use_sudo=True)
        self.assertTrue(manager_with_sudo.use_sudo)

    @patch('subprocess.run')
    def test_list_services_success(self, mock_run):
        """Test listing services successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test.service loaded active running Test Service\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock is_enabled
        with patch.object(self.manager, 'is_enabled', return_value=True):
            services = self.manager.list_services()
        
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].name, "test.service")
        self.assertEqual(services[0].active_state, ServiceState.ACTIVE)

    @patch('subprocess.run')
    def test_start_service_success(self, mock_run):
        """Test starting a service successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, message = self.manager.start_service("test.service")
        
        self.assertTrue(success)
        self.assertIn("started successfully", message)

    @patch('subprocess.run')
    def test_start_service_failure(self, mock_run):
        """Test starting a service with failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Failed to start test.service"
        mock_run.return_value = mock_result
        
        success, message = self.manager.start_service("test.service")
        
        self.assertFalse(success)
        self.assertIn("Failed", message)

    @patch('subprocess.run')
    def test_stop_service_success(self, mock_run):
        """Test stopping a service successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, message = self.manager.stop_service("test.service")
        
        self.assertTrue(success)
        self.assertIn("stopped successfully", message)

    @patch('subprocess.run')
    def test_restart_service_success(self, mock_run):
        """Test restarting a service successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, message = self.manager.restart_service("test.service")
        
        self.assertTrue(success)
        self.assertIn("restarted successfully", message)

    @patch('subprocess.run')
    def test_enable_service_success(self, mock_run):
        """Test enabling a service successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, message = self.manager.enable_service("test.service")
        
        self.assertTrue(success)
        self.assertIn("enabled successfully", message)

    @patch('subprocess.run')
    def test_disable_service_success(self, mock_run):
        """Test disabling a service successfully."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, message = self.manager.disable_service("test.service")
        
        self.assertTrue(success)
        self.assertIn("disabled successfully", message)

    @patch('subprocess.run')
    def test_is_enabled_true(self, mock_run):
        """Test checking if service is enabled."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "enabled\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.manager.is_enabled("test.service")
        
        self.assertTrue(result)

    @patch('subprocess.run')
    def test_is_enabled_false(self, mock_run):
        """Test checking if service is not enabled."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "disabled\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.manager.is_enabled("test.service")
        
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_command_timeout(self, mock_run):
        """Test command timeout handling."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 30)
        
        returncode, stdout, stderr = self.manager._run_command(["status", "test.service"])
        
        self.assertEqual(returncode, 1)
        self.assertEqual(stdout, "")
        self.assertIn("timed out", stderr)

    def test_parse_load_state(self):
        """Test parsing load state."""
        self.assertEqual(
            self.manager._parse_load_state("loaded"),
            ServiceLoadState.LOADED
        )
        self.assertEqual(
            self.manager._parse_load_state("not-found"),
            ServiceLoadState.NOT_FOUND
        )
        self.assertEqual(
            self.manager._parse_load_state("invalid"),
            ServiceLoadState.UNKNOWN
        )

    def test_parse_active_state(self):
        """Test parsing active state."""
        self.assertEqual(
            self.manager._parse_active_state("active"),
            ServiceState.ACTIVE
        )
        self.assertEqual(
            self.manager._parse_active_state("inactive"),
            ServiceState.INACTIVE
        )
        self.assertEqual(
            self.manager._parse_active_state("failed"),
            ServiceState.FAILED
        )
        self.assertEqual(
            self.manager._parse_active_state("invalid"),
            ServiceState.UNKNOWN
        )


if __name__ == '__main__':
    unittest.main()

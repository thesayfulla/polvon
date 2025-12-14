"""Service management module for interacting with systemd."""

import subprocess
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ServiceState(Enum):
    """Enum for service states."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    ACTIVATING = "activating"
    DEACTIVATING = "deactivating"
    UNKNOWN = "unknown"


class ServiceLoadState(Enum):
    """Enum for service load states."""
    LOADED = "loaded"
    NOT_FOUND = "not-found"
    ERROR = "error"
    MASKED = "masked"
    UNKNOWN = "unknown"


@dataclass
class Service:
    """Data class representing a systemd service."""
    name: str
    load_state: ServiceLoadState
    active_state: ServiceState
    sub_state: str
    description: str
    enabled: bool = False


class ServiceManager:
    """Manager class for systemd service operations."""

    def __init__(self, use_sudo: bool = False):
        """Initialize the service manager.
        
        Args:
            use_sudo: Whether to use sudo for systemctl commands
        """
        self.use_sudo = use_sudo

    def _run_command(self, args: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """Safely run a systemctl command.
        
        Args:
            args: Command arguments to pass to systemctl
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        cmd = []
        if self.use_sudo:
            cmd.append("sudo")
        cmd.extend(["systemctl"] + args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out"
        except Exception as e:
            return 1, "", str(e)

    def list_services(self, show_all: bool = False) -> List[Service]:
        """List all systemd services.
        
        Args:
            show_all: If True, show all services including inactive ones
            
        Returns:
            List of Service objects
        """
        args = ["list-units", "--type=service", "--no-pager", "--plain", "--no-legend"]
        if show_all:
            args.append("--all")
        
        returncode, stdout, stderr = self._run_command(args)
        
        if returncode != 0:
            return []
        
        services = []
        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue
            
            parts = line.split(None, 4)
            if len(parts) >= 5:
                name = parts[0]
                load_state = self._parse_load_state(parts[1])
                active_state = self._parse_active_state(parts[2])
                sub_state = parts[3]
                description = parts[4]
                
                # Check if service is enabled
                enabled = self.is_enabled(name)
                
                services.append(Service(
                    name=name,
                    load_state=load_state,
                    active_state=active_state,
                    sub_state=sub_state,
                    description=description,
                    enabled=enabled
                ))
        
        return services

    def _parse_load_state(self, state: str) -> ServiceLoadState:
        """Parse load state string to enum."""
        try:
            return ServiceLoadState(state.lower())
        except ValueError:
            return ServiceLoadState.UNKNOWN

    def _parse_active_state(self, state: str) -> ServiceState:
        """Parse active state string to enum."""
        try:
            return ServiceState(state.lower())
        except ValueError:
            return ServiceState.UNKNOWN

    def get_service_status(self, service_name: str) -> Optional[Dict[str, str]]:
        """Get detailed status of a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Dictionary with service status information or None if failed
        """
        returncode, stdout, stderr = self._run_command(["status", service_name])
        
        if returncode > 3:  # systemctl returns 0-3 for various states
            return None
        
        status_info = {
            "output": stdout,
            "name": service_name
        }
        
        return status_info

    def get_service_logs(self, service_name: str, lines: int = 50) -> Optional[str]:
        """Get logs for a service using journalctl.
        
        Args:
            service_name: Name of the service
            lines: Number of lines to retrieve
            
        Returns:
            Log output as string or None if failed
        """
        cmd = []
        if self.use_sudo:
            cmd.append("sudo")
        cmd.extend(["journalctl", "-u", service_name, "-n", str(lines), "--no-pager"])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            return None
        except Exception:
            return None

    def start_service(self, service_name: str) -> Tuple[bool, str]:
        """Start a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["start", service_name])
        
        if returncode == 0:
            return True, f"Service {service_name} started successfully"
        else:
            return False, stderr or "Failed to start service"

    def stop_service(self, service_name: str) -> Tuple[bool, str]:
        """Stop a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["stop", service_name])
        
        if returncode == 0:
            return True, f"Service {service_name} stopped successfully"
        else:
            return False, stderr or "Failed to stop service"

    def restart_service(self, service_name: str) -> Tuple[bool, str]:
        """Restart a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["restart", service_name])
        
        if returncode == 0:
            return True, f"Service {service_name} restarted successfully"
        else:
            return False, stderr or "Failed to restart service"

    def enable_service(self, service_name: str) -> Tuple[bool, str]:
        """Enable a service to start on boot.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["enable", service_name])
        
        if returncode == 0:
            return True, f"Service {service_name} enabled successfully"
        else:
            return False, stderr or "Failed to enable service"

    def disable_service(self, service_name: str) -> Tuple[bool, str]:
        """Disable a service from starting on boot.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["disable", service_name])
        
        if returncode == 0:
            return True, f"Service {service_name} disabled successfully"
        else:
            return False, stderr or "Failed to disable service"

    def is_enabled(self, service_name: str) -> bool:
        """Check if a service is enabled.
        
        Args:
            service_name: Name of the service
            
        Returns:
            True if enabled, False otherwise
        """
        returncode, stdout, stderr = self._run_command(["is-enabled", service_name])
        
        return returncode == 0 and stdout.strip() == "enabled"

    def reload_daemon(self) -> Tuple[bool, str]:
        """Reload systemd daemon configuration.
        
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self._run_command(["daemon-reload"])
        
        if returncode == 0:
            return True, "Daemon reloaded successfully"
        else:
            return False, stderr or "Failed to reload daemon"

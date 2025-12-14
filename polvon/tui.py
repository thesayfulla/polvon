from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, DataTable, Static, Button, Label, Input
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import on
from textual.reactive import reactive
from rich.text import Text

from .service import ServiceManager, ServiceState


class ConfirmDialog(ModalScreen):
    """A confirmation dialog screen."""

    CSS = """
    ConfirmDialog {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: 11;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #question {
        width: 100%;
        height: 3;
        content-align: center middle;
    }

    #buttons {
        width: 100%;
        height: auto;
        align: center middle;
    }

    Button {
        margin: 0 2;
    }
    """

    def __init__(self, message: str, action_callback=None):
        super().__init__()
        self.message = message
        self.action_callback = action_callback

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.message, id="question"),
            Horizontal(
                Button("Yes", variant="primary", id="yes"),
                Button("No", variant="default", id="no"),
                id="buttons",
            ),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            if self.action_callback:
                self.action_callback()
        self.dismiss(event.button.id == "yes")


class StatusScreen(ModalScreen):
    """Screen to display service status."""

    CSS = """
    StatusScreen {
        align: center middle;
    }

    #status_container {
        width: 90%;
        height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #status_content {
        width: 100%;
        height: 1fr;
    }

    #close_button {
        dock: bottom;
        width: 100%;
        margin-top: 1;
    }
    """

    def __init__(self, status_text: str):
        super().__init__()
        self.status_text = status_text

    def compose(self) -> ComposeResult:
        yield Container(
            ScrollableContainer(
                Static(self.status_text, id="status_content"),
            ),
            Button("Close", variant="primary", id="close_button"),
            id="status_container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()


class LogScreen(ModalScreen):
    """Screen to display service logs."""

    CSS = """
    LogScreen {
        align: center middle;
    }

    #log_container {
        width: 90%;
        height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #log_content {
        width: 100%;
        height: 1fr;
    }

    #close_button {
        dock: bottom;
        width: 100%;
        margin-top: 1;
    }
    """

    def __init__(self, log_text: str):
        super().__init__()
        self.log_text = log_text

    def compose(self) -> ComposeResult:
        yield Container(
            ScrollableContainer(
                Static(self.log_text, id="log_content"),
            ),
            Button("Close", variant="primary", id="close_button"),
            id="log_container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()


class PolvonApp(App):
    """Main Polvon TUI application."""

    CSS = """
    Screen {
        background: $surface;
    }

    #info_bar {
        dock: top;
        height: 3;
        background: $primary;
        color: $text;
        padding: 1 2;
    }

    #search_container {
        dock: top;
        height: 3;
        padding: 0 2;
    }

    #search_input {
        width: 100%;
    }

    #service_table {
        height: 1fr;
    }

    DataTable {
        height: 100%;
    }

    .active {
        color: $success;
    }

    .inactive {
        color: $warning;
    }

    .failed {
        color: $error;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("s", "start", "Start", show=True),
        Binding("S", "stop", "Stop", show=True),
        Binding("R", "restart", "Restart", show=True),
        Binding("e", "enable", "Enable", show=True),
        Binding("d", "disable", "Disable", show=True),
        Binding("v", "status", "Status", show=True),
        Binding("l", "logs", "Logs", show=True),
        Binding("a", "toggle_all", "Toggle All", show=True),
        Binding("/", "focus_search", "Search", show=True),
        Binding("escape", "clear_search", "Clear Search", show=False),
    ]

    TITLE = "Polvon - System Service Manager"

    show_all_services = reactive(False)
    search_query = reactive("")

    def __init__(self, use_sudo: bool = False):
        super().__init__()
        self.service_manager = ServiceManager(use_sudo=use_sudo)
        self.services = []
        self.filtered_services = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Loading services...", id="info_bar")
        yield Container(
            Input(placeholder="Search services... (Press / to focus, Esc to clear)", id="search_input"),
            id="search_container"
        )
        yield DataTable(id="service_table")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the application on mount."""
        table = self.query_one("#service_table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        
        # Add columns
        table.add_columns("Service", "State", "Enabled", "Description")
        
        self.load_services()

    def load_services(self) -> None:
        """Load services from systemd."""
        self.services = self.service_manager.list_services(show_all=self.show_all_services)
        self.filter_services()
        self.update_table()
        self.update_info_bar()

    def filter_services(self) -> None:
        """Filter services based on search query."""
        if not self.search_query:
            self.filtered_services = self.services
        else:
            query = self.search_query.lower()
            self.filtered_services = [
                service for service in self.services
                if query in service.name.lower() or 
                   (service.description and query in service.description.lower())
            ]

    def update_table(self) -> None:
        """Update the service table with current data."""
        table = self.query_one("#service_table", DataTable)
        table.clear()
        
        for service in self.filtered_services:
            # Create colored state text
            state_text = Text(service.active_state.value)
            if service.active_state == ServiceState.ACTIVE:
                state_text.stylize("green")
            elif service.active_state == ServiceState.INACTIVE:
                state_text.stylize("yellow")
            elif service.active_state == ServiceState.FAILED:
                state_text.stylize("red")
            else:
                state_text.stylize("blue")
            
            enabled_text = "✓" if service.enabled else "✗"
            
            table.add_row(
                service.name,
                state_text,
                enabled_text,
                service.description[:60] + "..." if len(service.description) > 60 else service.description,
                key=service.name
            )

    def update_info_bar(self) -> None:
        """Update the information bar."""
        info = self.query_one("#info_bar", Static)
        total = len(self.services)
        active = sum(1 for s in self.services if s.active_state == ServiceState.ACTIVE)
        failed = sum(1 for s in self.services if s.active_state == ServiceState.FAILED)
        
        mode = "all services" if self.show_all_services else "active services"
        search_info = f" | Filtered: {len(self.filtered_services)}" if self.search_query else ""
        info.update(f"Total: {total} | Active: {active} | Failed: {failed} | Showing: {mode}{search_info}")

    def get_selected_service(self) -> str:
        """Get the currently selected service name."""
        table = self.query_one("#service_table", DataTable)
        if 0 <= table.cursor_row < len(self.filtered_services):
            return self.filtered_services[table.cursor_row].name
        return None

    def action_refresh(self) -> None:
        """Refresh the service list."""
        self.load_services()
        self.notify("Services refreshed")

    def action_toggle_all(self) -> None:
        """Toggle between showing all services and only active ones."""
        self.show_all_services = not self.show_all_services
        self.load_services()

    def action_start(self) -> None:
        """Start the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        def start_action():
            success, message = self.service_manager.start_service(service_name)
            if success:
                self.notify(message, severity="information")
                self.load_services()
            else:
                self.notify(f"Error: {message}", severity="error")

        self.push_screen(
            ConfirmDialog(f"Start service '{service_name}'?", start_action)
        )

    def action_stop(self) -> None:
        """Stop the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        def stop_action():
            success, message = self.service_manager.stop_service(service_name)
            if success:
                self.notify(message, severity="information")
                self.load_services()
            else:
                self.notify(f"Error: {message}", severity="error")

        self.push_screen(
            ConfirmDialog(f"Stop service '{service_name}'?", stop_action)
        )

    def action_restart(self) -> None:
        """Restart the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        def restart_action():
            success, message = self.service_manager.restart_service(service_name)
            if success:
                self.notify(message, severity="information")
                self.load_services()
            else:
                self.notify(f"Error: {message}", severity="error")

        self.push_screen(
            ConfirmDialog(f"Restart service '{service_name}'?", restart_action)
        )

    def action_enable(self) -> None:
        """Enable the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        def enable_action():
            success, message = self.service_manager.enable_service(service_name)
            if success:
                self.notify(message, severity="information")
                self.load_services()
            else:
                self.notify(f"Error: {message}", severity="error")

        self.push_screen(
            ConfirmDialog(f"Enable service '{service_name}'?", enable_action)
        )

    def action_disable(self) -> None:
        """Disable the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        def disable_action():
            success, message = self.service_manager.disable_service(service_name)
            if success:
                self.notify(message, severity="information")
                self.load_services()
            else:
                self.notify(f"Error: {message}", severity="error")

        self.push_screen(
            ConfirmDialog(f"Disable service '{service_name}'?", disable_action)
        )

    def action_status(self) -> None:
        """Show status of the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        status_info = self.service_manager.get_service_status(service_name)
        if status_info:
            self.push_screen(StatusScreen(status_info["output"]))
        else:
            self.notify("Failed to get service status", severity="error")

    def action_logs(self) -> None:
        """Show logs of the selected service."""
        service_name = self.get_selected_service()
        if not service_name:
            self.notify("No service selected", severity="warning")
            return

        logs = self.service_manager.get_service_logs(service_name)
        if logs:
            self.push_screen(LogScreen(logs))
        else:
            self.notify("Failed to get service logs", severity="error")

    def action_focus_search(self) -> None:
        """Focus the search input."""
        search_input = self.query_one("#search_input", Input)
        search_input.focus()

    def action_clear_search(self) -> None:
        """Clear the search input."""
        search_input = self.query_one("#search_input", Input)
        search_input.value = ""
        table = self.query_one("#service_table", DataTable)
        table.focus()

    @on(Input.Changed, "#search_input")
    def on_search_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        self.search_query = event.value
        self.filter_services()
        self.update_table()
        self.update_info_bar()

from textual.app import App, ComposeResult
from textual.widgets import (
    DirectoryTree,
    Header,
    Footer,
    TabbedContent,
    TabPane,
    Static,
    Label,
)
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from pathlib import Path
import json


class CustomExtensionDirectoryTree(DirectoryTree):
    """DirectoryTree that filters to show only specific file extensions."""

    def __init__(self, path: str = "./", extensions: list[str] | None = None, **kwargs):
        """
        Initialize the custom directory tree.

        Args:
            path: Root directory path
            extensions: List of file extensions to show (e.g., ['.py', '.txt', '.myext'])
        """
        super().__init__(path, **kwargs)
        self.extensions = extensions or [".py", ".txt"]

    def filter_paths(self, paths):
        """
        Filter paths to only show directories and files with allowed extensions.

        Args:
            paths: Iterable of Path objects from the directory

        Returns:
            Filtered list of Path objects
        """
        filtered = []
        for path in paths:
            # Always include directories
            if path.is_dir():
                filtered.append(path)
            # Include files with matching extensions
            elif path.suffix in self.extensions:
                filtered.append(path)
        return filtered


class FileInfoPane(Static):
    """Pane to display file information."""

    DEFAULT_CSS = """
    FileInfoPane {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
    }
    """

    file_path = reactive("")

    def render(self) -> str:
        """Render the file info."""
        if not self.file_path:
            return "[bold cyan]Select a file to view details[/bold cyan]"

        path = Path(self.file_path)
        if not path.exists():
            return f"[bold red]File not found: {path}[/bold red]"

        try:
            if path.is_file():
                stat = path.stat()
                content = f"""[bold cyan]File Information[/bold cyan]
[yellow]Name:[/yellow] {path.name}
[yellow]Path:[/yellow] {path.absolute()}
[yellow]Size:[/yellow] {stat.st_size} bytes
[yellow]Modified:[/yellow] {path.stat().st_mtime}
[yellow]Extension:[/yellow] {path.suffix}
"""
                return content
            else:
                stat = path.stat()
                content = f"""[bold cyan]Directory Information[/bold cyan]
[yellow]Name:[/yellow] {path.name}
[yellow]Path:[/yellow] {path.absolute()}
[yellow]Modified:[/yellow] {path.stat().st_mtime}

[bold]Contents:[/bold]
"""
                # List directory contents
                try:
                    for item in sorted(path.iterdir())[:20]:  # Show first 20 items
                        content += f"\n  {'📁' if item.is_dir() else '📄'} {item.name}"
                    if len(list(path.iterdir())) > 20:
                        content += "\n  ... and more"
                except PermissionError:
                    content += "\n  [red](Permission denied)[/red]"
                return content
        except Exception as e:
            return f"[bold red]Error: {str(e)}[/bold red]"


class FilePreviewPane(Static):
    """Pane to display file preview."""

    DEFAULT_CSS = """
    FilePreviewPane {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
        overflow: auto;
    }
    """

    file_path = reactive("")

    def render(self) -> str:
        """Render the file preview."""
        if not self.file_path:
            return "[bold cyan]Select a file to preview[/bold cyan]"

        path = Path(self.file_path)
        if not path.exists():
            return f"[bold red]File not found: {path}[/bold red]"

        if path.is_dir():
            return "[bold yellow]This is a directory, not a file[/bold yellow]"

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(5000)  # Read first 5000 characters
                if len(content) < f.seek(0, 2):
                    content += "\n\n[dim]... (truncated)[/dim]"
            return f"[bold cyan]{path.name}[/bold cyan]\n\n{content}"
        except Exception as e:
            return f"[bold red]Cannot preview: {str(e)}[/bold red]"


class DirectoryTreeTabbedApp(App):
    """Application with DirectoryTree and TabbedContent."""

    BINDINGS = [("q", "quit", "Quit")]

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 25% 1fr;
    }

    #tree_container {
        border: solid $accent;
        height: 100%;
    }

    #tabs_container {
        height: 100%;
        border: solid $accent;
    }

    DirectoryTree {
        width: 100%;
        height: 100%;
    }

    TabbedContent {
        width: 100%;
        height: 100%;
    }
    """

    selected_path = reactive("")

    def compose(self) -> ComposeResult:
        """Compose the app with directory tree and tabbed content."""
        yield Header(show_clock=True)

        with Horizontal(id="main_content"):
            with Container(id="tree_container"):
                yield CustomExtensionDirectoryTree(
                    path="./",
                    extensions=[".py", ".txt", ".json", ".md", ".myext"],
                    id="dir_tree",
                )

            with Container(id="tabs_container"):
                with TabbedContent(initial="info"):
                    with TabPane("📋 Info", id="info"):
                        yield FileInfoPane(id="file_info")
                    with TabPane("👁️ Preview", id="preview"):
                        yield FilePreviewPane(id="file_preview")
                    with TabPane("📊 Metadata", id="metadata"):
                        yield Static(id="metadata_pane")

        yield Footer()

    def on_mount(self) -> None:
        """Handle app mount."""
        self.title = "Directory Tree with Tabs"
        self.sub_title = "Click items in the tree to load tabs | Press Q to quit"

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle file selection from directory tree."""
        path = event.path
        self.selected_path = str(path)
        self._update_tabs(path)

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        """Handle directory selection from directory tree."""
        path = event.path
        self.selected_path = str(path)
        self._update_tabs(path)

    def watch_selected_path(self, new_path: str) -> None:
        """Watch for changes to selected_path and update tabs."""
        if new_path:
            self._update_tabs(Path(new_path))

    def _update_tabs(self, path: Path) -> None:
        """Update all tabs with information about the selected path."""
        # Update Info tab
        file_info = self.query_one("#file_info", FileInfoPane)
        file_info.file_path = str(path)

        # Update Preview tab
        file_preview = self.query_one("#file_preview", FilePreviewPane)
        file_preview.file_path = str(path)

        # Update Metadata tab
        metadata_pane = self.query_one("#metadata_pane", Static)
        metadata_pane.update(self._get_metadata(path))

    def _get_metadata(self, path: Path) -> str:
        """Generate metadata for the selected path."""
        try:
            stat = path.stat()
            metadata = {
                "name": path.name,
                "type": "directory" if path.is_dir() else "file",
                "absolute_path": str(path.absolute()),
                "size_bytes": stat.st_size,
                "is_symlink": path.is_symlink(),
                "extension": path.suffix,
                "parent": str(path.parent),
            }

            # Format as readable text
            content = "[bold cyan]📊 Metadata[/bold cyan]\n\n"
            for key, value in metadata.items():
                content += f"[yellow]{key.replace('_', ' ').title()}:[/yellow] {value}\n"

            return content
        except Exception as e:
            return f"[bold red]Error loading metadata: {str(e)}[/bold red]"


if __name__ == "__main__":
    app = DirectoryTreeTabbedApp()
    app.run()

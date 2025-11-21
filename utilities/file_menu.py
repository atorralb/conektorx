from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Header, Footer
from pathlib import Path


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
        # Always include directories, plus any matching extensions
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


class DirectoryTreeApp(App):
    """Application to display a directory tree with custom file extensions."""

    BINDINGS = [("q", "quit", "Quit")]
    CSS = """
    Screen {
        layout: vertical;
    }

    DirectoryTree {
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the app with header, tree, and footer."""
        yield Header()
        # Customize extensions here: add your own extension (e.g., '.myext')
        yield CustomExtensionDirectoryTree(
            path="./",
            extensions=[".py", ".txt", ".myext", ".json"]  # Add your extension here
        )
        yield Footer()

    def on_mount(self) -> None:
        """Handle app mount."""
        self.title = "Directory Tree - Custom Extensions"


if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
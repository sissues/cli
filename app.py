from __future__ import annotations

from pathlib import Path
from subprocess import Popen, PIPE

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, MarkdownViewer, Static, Header, TextArea
from textual import log

EXERCISES_DIR = Path(__file__).parent / "exercises"


class MarkdownApp(App):
    """A Markdown viewer TUI application."""

    CSS_PATH = "app.css"
    BINDINGS = [
        ("t", "toggle_table_of_contents", "Toggle TOC"),
        ("m", "toggle_menu", "Toggle Menu"),
        ("q", "quit", "Quit")
    ]

    def __init__(self):
        super().__init__()
        self.current_markdown_path = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            Container(id="menu", classes="menu"),
            Container(
                MarkdownViewer(id="markdown_viewer"),
                TextArea(id="test_output"),
                id="content",
                classes="content",
            ),
        )

    def on_mount(self) -> None:
        """Initial setup when the app starts."""
        self.show_menu()

    def show_menu(self) -> None:
        """Display the menu with available exercises."""
        menu = self.query_one("#menu")
        menu.remove_children()
        exercises = list(EXERCISES_DIR.glob("*.md"))
        for idx, exercise in enumerate(exercises):
            exercise_name = exercise.stem
            exercise_container = Container(
                Static(exercise_name, id=exercise_name, classes="menu-item"),
                Button("View", id=f"view-{exercise_name}", classes="view-button"),
                Button("Run Tests", id=f"test-{exercise_name}", classes="test-button"),
                classes="menu-actions"
            )
            menu.mount(exercise_container)

    async def handle_button_pressed(self, message: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = message.button.id
        action, exercise_id = button_id.split("-", 1)
        exercise_name = self.query_one(f"#{exercise_id}", Static).renderable
        log(f"ExerciseName = {exercise_name}")
        selected_exercise = EXERCISES_DIR / f"{exercise_name}.md"
        log(f"SelectedExercise = {selected_exercise}")
        if action == "view":
            self.current_markdown_path = selected_exercise
            markdown_viewer = self.query_one("#markdown_viewer", MarkdownViewer)
            await markdown_viewer.go(selected_exercise)
            self.query_one("#content").display = True

        elif action == "test":
            self.run_tests(selected_exercise)

    def run_tests(self, markdown_path: Path) -> None:
        """Run tests for the selected exercise and display the output."""
        test_output = self.query_one("#test_output", TextArea)
        test_output.clear()

        # Simulate running tests (replace with actual test commands)
        command = ["echo", f"Running tests for {markdown_path.stem}..."]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        test_output.append(stdout.decode())
        if stderr:
            test_output.append(stderr.decode())

    def action_toggle_table_of_contents(self) -> None:
        """Toggle the display of the table of contents."""
        markdown_viewer = self.query_one("#markdown_viewer", MarkdownViewer)
        markdown_viewer.show_table_of_contents = not markdown_viewer.show_table_of_contents

    def action_toggle_menu(self) -> None:
        """Toggle the display of the menu."""
        menu = self.query_one("#menu")
        menu.visible = not menu.visible


if __name__ == "__main__":
    MarkdownApp().run()

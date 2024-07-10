from pathlib import Path
from subprocess import Popen, PIPE

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, MarkdownViewer, Header, TextArea, Select, Label
from textual import log

from exercises_utils import EXERCISES_DIR, ExercisesUtils


class MarkdownApp(App):

    TITLE = "Skill Issues Killer"
    SUB_TITLE = "practice real-world projects"
    CSS_PATH = "app.css"
    BINDINGS = [
        ("t", "toggle_table_of_contents", "Toggle TOC"),
        ("m", "toggle_menu", "Toggle Menu"),
        ("q", "quit", "Quit")
    ]

    def __init__(self):
        super().__init__()
        self.files_view_names = ExercisesUtils.generate_view_names_map()
        self.current_markdown_path = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Container(
                id="menu", classes="menu"),
            Container(
                MarkdownViewer(id="markdown_viewer"),
                Label("Tests Output"),
                TextArea(id="test_output", read_only=True),
                id="content",
                classes="content",
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initial setup when the app starts."""
        self.show_menu()

    def show_menu(self) -> None:
        """Display the menu with available exercises."""
        log("entered show menu")
        menu = self.query_one("#menu")
        menu.remove_children()
        exercises = list(EXERCISES_DIR.glob("*.md"))
        log(f"exercises = {exercises}")
        log(f"map = {self.files_view_names}")
        exercise_names = [(self.files_view_names[exercise.stem], exercise.stem) for exercise in exercises]
        select_file_widget = Select(options=exercise_names, prompt="Select Exercise", id="exercise_select", classes="menu_widget", tooltip="Select an exercise to preview")
        menu.mount(select_file_widget)
        menu.mount(Button("View", id="view", variant="primary", classes="menu_widget"))
        menu.mount(Button("Run Tests", id="test", variant="success", classes="menu_widget"))

        select_lang_widget = Select(options=[('python', 'python'), ('javascript', 'javascript')], prompt="Select Programming Language", id="lang_select", classes="menu_widget", tooltip="Select a language to create your project's template")
        menu.mount(select_lang_widget)
        menu.mount(Button("Start Project", id="start", variant="warning", classes="menu_widget"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        select_widget = self.query_one("#exercise_select", Select)
        exercise_name = select_widget.value
        selected_exercise = EXERCISES_DIR / f"{exercise_name}.md"

        select_lang_widget = self.query_one("#lang_select", Select)
        lang = select_lang_widget.value

        if button_id in ('view', 'test'):
            if exercise_name == Select.BLANK:
                select_widget.notify("Please select a file", severity="error", timeout=5)
                return

            if button_id == "view":
                self.current_markdown_path = selected_exercise
                markdown_viewer = self.query_one("#markdown_viewer", MarkdownViewer)
                await markdown_viewer.go(selected_exercise)
                self.query_one("#content").display = True

            elif button_id == "test":
                log("about to test")
                self.run_tests(selected_exercise)

        if button_id == 'start':
            if lang == Select.BLANK:
                select_lang_widget.notify("Please select a language", severity="error")
                return
            self.start_project(lang)

    def start_project(self, lang) -> None:
        test_output = self.query_one("#test_output", TextArea)
        test_output.notify(f'Creating project structure for lang {lang}')

    def run_tests(self, markdown_path: Path) -> None:
        """Run tests for the selected exercise and display the output."""
        log("starting to test")
        test_output = self.query_one("#test_output", TextArea)
        test_output.value = ""  # Clear the text area
        log("found test_output")
        # Simulate running tests (replace with actual test commands)
        command = ["echo", f"Running tests for {markdown_path.stem}..."]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        log("command executed")
        test_output.insert(stdout.decode())
        test_output.insert("wooo")
        test_output.insert("multiline\na lot \n of text\n testing\n if \nscrolling\nworks")
        if stderr:
            test_output.insert(stderr.decode())

        test_output.notify("Tests execution done", timeout=3)

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

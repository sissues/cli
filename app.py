import subprocess

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, MarkdownViewer, Header, TextArea, Select, Label

from exercises_utils import EXERCISES_DIR, ExercisesUtils
from project_generators.base_project_generator import BaseProjectGenerator


class MarkdownApp(App):

    TITLE = "Skill Issues Killer"
    SUB_TITLE = "practice real-world projects"
    CSS_PATH = "app.css"
    BINDINGS = [
        ("t", "toggle_table_of_contents", "Toggle TOC"),
        ("h", "show_help", "Show Help"),
        ("q", "quit", "Quit")
    ]

    help_text = """Pick an exercise, and generate a project template by click 'Start Project'
Once you are done implementing the exercise requirements, click on 'Run Tests'.\n
If all the tests passed, congrats!\n
If not, keep at it, one test at a time :)\n

[b][i]Got stuck?[/b][/i] \nRefer to the project's README.md at https://github.com/sissues/cli/blob/main/README.MD,\nor open an issue at https://github.com/sissues/cli/issues
    """

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
        self.notify(title="Hello World!", message=self.help_text, timeout=30)

    def show_menu(self) -> None:
        menu = self.query_one("#menu")
        menu.remove_children()

        exercises = list(EXERCISES_DIR.glob("*.md"))
        exercise_names = [(self.files_view_names[exercise.stem], exercise.stem) for exercise in exercises]
        select_file_widget = Select(options=exercise_names, allow_blank=False, prompt="Select Exercise", id="exercise_select", classes="menu_widget", tooltip="Select an exercise to preview")

        menu.mount(select_file_widget)
        menu.mount(Button("Start Project", id="start", variant="warning", classes="menu_widget"))
        menu.mount(Button("Run Tests", id="test", variant="success", classes="menu_widget"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        select_widget = self.query_one("#exercise_select", Select)
        exercise_name = select_widget.value

        if button_id == "test":
            self.run_tests(exercise_name)

        elif button_id == 'start':
            self.start_project(exercise_name)

    def start_project(self, exercise_name: str) -> None:
        test_output = self.query_one("#test_output", TextArea)
        project_path = BaseProjectGenerator().generate(exercise_name)
        test_output.notify(f'Creating project structure for project {exercise_name}')
        ExercisesUtils.open_file_in_explorer(project_path)

    def run_tests(self, exercise_name: str) -> None:
        test_output = self.query_one("#test_output", TextArea)
        docker_compose_file_name = ExercisesUtils.get_resource_path(f"exercises_test_suites/docker_compose_{exercise_name}.yml")
        command = f"docker-compose -f {docker_compose_file_name} up --build"
        try:
            test_output.notify("Tests execution started, might take a few seconds", timeout=3)
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            test_output.insert(result.stdout)
        except subprocess.CalledProcessError as e:
            test_output.insert(f"An error occurred: {e.stderr}")

        test_output.notify("Tests execution done", timeout=3)

    def action_toggle_table_of_contents(self) -> None:
        """Toggle the display of the table of contents."""
        markdown_viewer = self.query_one("#markdown_viewer", MarkdownViewer)
        markdown_viewer.show_table_of_contents = not markdown_viewer.show_table_of_contents

    def action_show_help(self):
        self.notify(title="Hello World!", message=self.help_text, timeout=30)

    @on(Select.Changed)
    async def view_select(self, event: Select.Changed):
        selected_exercise = EXERCISES_DIR / f"{event.value}.md"
        self.current_markdown_path = selected_exercise
        markdown_viewer = self.query_one("#markdown_viewer", MarkdownViewer)
        await markdown_viewer.go(selected_exercise)
        self.query_one("#content").display = True


if __name__ == "__main__":
    MarkdownApp().run()

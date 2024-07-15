import os
import platform
import subprocess
from pathlib import Path

EXERCISES_DIR = Path(__file__).parent / "exercises"


class ExercisesUtils:
    @staticmethod
    def generate_view_names_map():
        all_md_files = list(EXERCISES_DIR.glob("*.md"))
        return {
            filename.stem: ' '.join(filename.stem.split('_')).title()
            for filename in all_md_files
        }

    @staticmethod
    def open_file_in_explorer(file_path):
        system = platform.system()

        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", file_path])

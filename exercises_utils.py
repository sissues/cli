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

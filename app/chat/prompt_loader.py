from pathlib import Path


class PromptLoader:
    # pointing to template directory
    BASE_PATH = Path(__file__).parent / "templates"

    @classmethod
    def load(cls, name: str) -> str:
        prompt_file = cls.BASE_PATH / f"{name}.txt"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt '{name}' not found.")

        return prompt_file.read_text(encoding="utf-8")

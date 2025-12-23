import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    input_file: str
    output_dir: str
    temperature: float

def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Не найден OPENAI_API_KEY. Добавь ключ в .env.")

    return Settings(
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        input_file=os.getenv("INPUT_FILE", "input_text.txt"),
        output_dir=os.getenv("OUTPUT_DIR", "notes"),
        temperature=float(os.getenv("TEMPERATURE", "0.3")),
    )

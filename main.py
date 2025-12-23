import logging
import warnings

from langchain_core._api import LangChainDeprecationWarning

from app.config import get_settings
from app.summarizer import SummarizerApp

warnings.filterwarnings(
    "ignore",
    category=LangChainDeprecationWarning
)

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# )

HELP = """
Команды:
  summarize            — резюмировать input.txt
  refine <инструкция>  — доработать последний результат (memory)
  show                — показать последний результат
  save                — сохранить в summaries/summary_<ТЕМА>.txt (tool)
  help                — показать помощь
  exit                — выход
""".strip()

def main():
    try:
        s = get_settings()
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return

    app = SummarizerApp(model=s.openai_model, temperature=s.temperature, output_dir=s.output_dir)

    print("✅ LangChain Summarizer (CLI) запущен.")
    print(HELP)

    while True:
        try:
            cmd = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Выход.")
            break

        if not cmd:
            print("⚠️ Пустая команда. help — список.")
            continue

        if cmd in ("exit", "quit"):
            print("👋 Выход.")
            break

        if cmd in ("help", "?"):
            print(HELP)
            continue

        if cmd == "summarize":
            try:
                app.summarize_file(s.input_file)
                print("✅ Готово. show — посмотреть, save — сохранить.")
            except Exception as e:
                print(f"❌ Ошибка summarize: {e}")
            continue

        if cmd.startswith("refine "):
            instruction = cmd[len("refine "):].strip()
            if not instruction:
                print("⚠️ refine <инструкция>")
                continue
            try:
                app.refine(instruction)
                print("✅ Обновлено. show — посмотреть, save — сохранить.")
            except Exception as e:
                print(f"❌ Ошибка refine: {e}")
            continue

        if cmd == "show":
            if not app.last_answer:
                print("⚠️ Пока нет результата. summarize.")
            else:
                print("\n" + app.last_answer)
            continue

        if cmd == "save":
            try:
                path = app.save_last()
                print(f"✅ Сохранено: {path}")
            except Exception as e:
                print(f"❌ Ошибка save: {e}")
            continue

        print("❓ Неизвестная команда. help — список.")

if __name__ == "__main__":
    main()

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader

# ---------- Document Loader ----------
def load_text(path: str) -> str:
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    return ("\n\n".join(d.page_content for d in docs).strip()) if docs else ""

# ---------- Memory ----------
def build_memory() -> ConversationBufferMemory:
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ---------- Tool ----------
@tool
def save_notes(output_dir: str, topic: str, content: str) -> str:
    """Сохраняет заметки в txt файл summary_<topic>.txt и возвращает путь."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"summary_{topic}.txt"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ---------- Prompt + Chain ----------
PROMPT = PromptTemplate.from_template(
    """
Ты помощник для академического резюмирования текста на русском.

ИСХОДНЫЙ ТЕКСТ: примерно {word_count} слов.
Требование к КРАТКОМУ ПЕРЕСКАЗУ: ровно {sentences_target} предложений (не больше и не меньше).

Сделай:
1) ТЕМА (2–5 слов).
2) КОНСПЕКТ:
   - Основные идеи (4–10 пунктов)
   - Ключевые термины (5–12)
   - Вывод (2–4 предложения)
3) КРАТКИЙ ПЕРЕСКАЗ: ровно {sentences_target} предложений.

Верни СТРОГО в формате:

ТЕМА: <тема>

КОНСПЕКТ:
- Основные идеи:
  - ...
- Ключевые термины:
  - ...
- Вывод:
  ...

КРАТКИЙ ПЕРЕСКАЗ:
<ровно {sentences_target} предложений>

Текст:
{text}
""".strip()
)

def build_chain(model: str, temperature: float):
    llm = ChatOpenAI(model=model, temperature=temperature)
    parser = StrOutputParser()
    # LCEL chain (Chain компонент)
    return PROMPT | llm | parser

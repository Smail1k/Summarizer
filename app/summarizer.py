import re
from typing import Optional

from app.utils import load_text, build_chain, build_memory, save_notes


# ---------- Utils ----------
def word_count(text: str) -> int:
    return len(text.split())


def sentences_target_for_words(wc: int) -> str:
    """
    Адаптация длины пересказа по размеру исходного текста.
    """
    if wc <= 800:
        return "4–5"
    if wc <= 4000:
        return "6–8"
    if wc <= 12000:
        return "10–14"
    return "15–20"


def extract_topic(answer: str) -> str:
    for line in answer.splitlines():
        if line.strip().startswith("ТЕМА:"):
            return line.split("ТЕМА:", 1)[1].strip()
    return ""


def sanitize_topic(topic: str, fallback: str = "unknown_topic") -> str:
    topic = (topic or "").strip()
    if not topic:
        return fallback
    topic = topic.replace(" ", "_")
    topic = re.sub(r"[^\w\-А-Яа-яЁё]", "", topic)
    topic = re.sub(r"_+", "_", topic).strip("_")
    return topic or fallback


# ---------- App ----------
class SummarizerApp:
    def __init__(self, model: str, temperature: float, output_dir: str):
        self.chain = build_chain(model, temperature)
        self.memory = build_memory()
        self.output_dir = output_dir

        self.last_answer: Optional[str] = None
        self.last_topic: str = "unknown_topic"

    def summarize_file(self, input_file: str) -> str:
        text = load_text(input_file)
        if not text:
            raise ValueError("Файл пустой или не удалось прочитать текст.")

        wc = word_count(text)
        target = sentences_target_for_words(wc)

        answer = self.chain.invoke({
            "text": text,
            "word_count": wc,
            "sentences_target": target,
        })

        self.last_answer = answer
        self.last_topic = sanitize_topic(extract_topic(answer))

        # Memory сохраняем историю
        self.memory.save_context(
            {"input": f"summarize (words={wc}, target={target})"},
            {"output": answer}
        )
        return answer

    def refine(self, instruction: str) -> str:
        if not self.last_answer:
            raise ValueError("Сначала сделай summarize.")

        refine_text = (
            "Переработай текст ниже по инструкции, не добавляя новых фактов и сохраняя формат.\n"
            f"ИНСТРУКЦИЯ: {instruction}\n\n"
            f"ТЕКУЩИЙ РЕЗУЛЬТАТ:\n{self.last_answer}"
        )

        answer = self.chain.invoke({
            "text": refine_text,
            "word_count": word_count(self.last_answer),
            "sentences_target": "4–20",
        })

        self.last_answer = answer
        t = extract_topic(answer).strip()
        if t:
            self.last_topic = sanitize_topic(t)

        self.memory.save_context(
            {"input": f"refine: {instruction}"},
            {"output": answer}
        )
        return answer

    def save_last(self) -> str:
        if not self.last_answer:
            raise ValueError("Нет результата для сохранения. Сделай summarize.")
        return save_notes.invoke({
            "output_dir": self.output_dir,
            "topic": self.last_topic,
            "content": self.last_answer
        })

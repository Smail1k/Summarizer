# LangChain Text Summarizer (Конспект + заметки)

Проект: система резюмирования больших текстов и сохранения заметок.
Читает `input.txt`, делает структурированный конспект + краткий пересказ, сохраняет в `summaries/summary_<ТЕМА>.txt`.

## Возможности
- Загрузка текста из файла (Document Loader)
- Резюмирование через OpenAI модель (ChatOpenAI) с управляемым промптом (PromptTemplate)
- Построение цепочки (LCEL chain)
- Память диалога (Memory) для доработок результата (refine)
- Tool для сохранения результата в файл (Tools / Functions)
- CLI интерфейс
- Логи и обработка ошибок

## Требования
- Python 3.10+
- Аккаунт OpenAI + API key
- Установленные зависимости из `requirements.txt`

## Установка
```bash
pip install -r requirements.txt

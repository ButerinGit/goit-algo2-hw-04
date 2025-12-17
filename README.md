# Design and Analysis of Algorithms

Репозиторій містить розв'язки двох завдань з алгоритмів та структур даних:

- `task1_max_flow_algo/` — алгоритм максимального потоку (Едмондса–Карпа) для логістичної мережі.
- `task2_prefix_tree/` — розширення функціоналу префіксного дерева (Trie).

## Структура проєкту

```text
..
├── task1_max_flow_algo/
│   ├── max_flow_algo.py
│   └── README_task1_max_flow.md
├── task2_prefix_tree/
│   ├── prefix_tree.py
│   ├── trie.py  
│   └── README_task2_prefix_tree.md
├── requirements.txt
├── .gitignore
└── README_root.md   # цей файл
```

## Віртуальне оточення

Рекомендується використовувати окреме віртуальне оточення Python.

```bash
python3 -m venv .venv

# Активувати (Linux/macOS):
source .venv/bin/activate

# або (Windows PowerShell):
.\.venv\Scriptsctivate
```

Встановлення залежностей (якщо вони будуть додані):

```bash
pip install -r requirements.txt
```

> На даний момент реалізації обох завдань використовують стандартну бібліотеку Python, тому `requirements.txt` може бути порожнім або містити тільки коментар.

## Запуск завдань

### Task 1 — Max Flow

```bash
cd task1_max_flow_algo
python3 max_flow_algo.py
```

Скрипт:
- будує граф логістичної мережі,
- обчислює максимальний потік,
- виводить потоки по ребрах та зведену таблицю «Термінал — Магазин».

### Task 2 — Prefix Tree (Trie)

```bash
cd task2_prefix_tree
python3 prefix_tree.py
```

Скрипт:
- створює екземпляр розширеного Trie (`PrefixTree`),
- додає тестові слова,
- перевіряє роботу методів `count_words_with_suffix` і `has_prefix` через `assert`,
- у разі успішного проходження тестів виводить повідомлення.
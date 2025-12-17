# Task 2 — Розширення префіксного дерева (Trie)

## Постановка задачі

Є базовий клас `Trie`, який підтримує зберігання рядків (слів) та їхніх значень (наприклад, індекс або будь-які інші дані).

Потрібно реалізувати дочірній клас `PrefixTree`, який:

1. Успадковує базовий клас `Trie`.
2. Додає два методи:
   - `count_words_with_suffix(pattern) -> int` — рахує кількість слів, що закінчуються на заданий суфікс `pattern`.
   - `has_prefix(prefix) -> bool` — перевіряє, чи існує хоча б одне слово з префіксом `prefix`.

## Вимоги

1. Клас `PrefixTree` **успадковує** клас `Trie`:
   ```python
   from trie import Trie

   class PrefixTree(Trie):
       ...
   ```

2. Обидва методи перевіряють **коректність типів аргументів**:
   - якщо `pattern` або `prefix` не є рядком (`str`), методи кидають `TypeError`.

3. Обробка регістру:
   - методи **враховують регістр** символів (`"App"` і `"app"` вважаються різними).

4. Типи результатів:
   - `count_words_with_suffix` повертає **ціле число (`int`)**;
   - `has_prefix` повертає **булеве значення (`bool`)**.

5. Ефективність:
   - реалізація базується на зберіганні всіх вставлених слів у множині `set`, що дозволяє просто й ефективно ітерувати по словах;
   - вставка при цьому не стає повільнішою (Trie працює як раніше, додатково — O(1) на вставку в `set`).

## Ідея реалізації

Оскільки внутрішню реалізацію класу `Trie` ми не знаємо, то:

- у класі `PrefixTree` перевизначається метод `put(key, value)`:
  - додає слово `key` до внутрішнього набору `self._words`,
  - викликає базовий `super().put(key, value)`, щоб не зламати поведінку Trie.

- метод `count_words_with_suffix(pattern)`:
  - перевіряє, що `pattern` — рядок;
  - проходить по всіх словах у `self._words`,
  - рахує, скільки з них задовольняють `word.endswith(pattern)`;
  - якщо таких немає — повертає `0`.

- метод `has_prefix(prefix)`:
  - перевіряє, що `prefix` — рядок;
  - повертає `True`, якщо існує хоч одне слово, що задовольняє `word.startswith(prefix)`;
  - якщо таких слів немає — повертає `False`.

Порожній рядок:
- для суфікса `""` логічно вважати, що він «підходить» до будь-якого слова → метод повертає кількість усіх слів;
- для префікса `""` будь-яке слово формально має такий префікс → якщо в Trie є хоча б одне слово, метод повертає `True`.

## Приклад реалізації

Файл `prefix_tree.py` містить щось на кшталт:

```python
from trie import Trie


class PrefixTree(Trie):
    def __init__(self) -> None:
        super().__init__()
        self._words: set[str] = set()

    def put(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        self._words.add(key)
        return super().put(key, value)

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")

        if pattern == "":
            return len(self._words)

        count = 0
        for word in self._words:
            if word.endswith(pattern):
                count += 1
        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")

        if prefix == "":
            return len(self._words) > 0

        for word in self._words:
            if word.startswith(prefix):
                return True
        return False


if __name__ == "__main__":
    trie = PrefixTree()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1   # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1   # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") is True   # apple, application
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True   # banana
    assert trie.has_prefix("ca") is True    # cat

    print("All tests passed for PrefixTree Trie.")
```

## Запуск

```bash
cd task2_prefix_tree
python3 prefix_tree.py
```

Успішний запуск без помилок і з повідомленням:

```text
All tests passed for PrefixTree Trie.
```

означає, що реалізація відповідає вимогам і проходить базові тести.
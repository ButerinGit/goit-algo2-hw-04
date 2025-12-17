from trie import Trie


class PrefixTree(Trie):
    """
    Розширення Trie:
    - count_words_with_suffix(pattern): рахує слова, що закінчуються на pattern
    - has_prefix(prefix): перевіряє наявність слів із заданим префіксом
    """

    def __init__(self) -> None:
        super().__init__()
        # Зберігаємо всі вставлені слова, щоб не лізти у внутрішню реалізацію Trie
        self._words: set[str] = set()

    def put(self, key, value):
        """
        Перевизначаємо put, щоб запам'ятовувати всі слова.
        Викликаємо оригінальний Trie.put, щоб не зламати базовий функціонал.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        self._words.add(key)
        return super().put(key, value)

    def count_words_with_suffix(self, pattern) -> int:
        """
        Повертає кількість слів, що закінчуються на заданий суфікс pattern.
        Враховує регістр. За відсутності — 0.
        """
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")

        # Якщо захочеш іншу поведінку для порожнього суфікса — можна змінити.
        if pattern == "":
            return len(self._words)

        count = 0
        for word in self._words:
            if word.endswith(pattern):
                count += 1
        return count

    def has_prefix(self, prefix) -> bool:
        """
        Повертає True, якщо існує хоч одне слово з префіксом prefix.
        Враховує регістр.
        """
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")

        # Порожній префікс — вважаємо, що підходить будь-яке слово
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
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") is True   # apple, application
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True   # banana
    assert trie.has_prefix("ca") is True    # cat

    print("All tests passed for PrefixTree Trie.")
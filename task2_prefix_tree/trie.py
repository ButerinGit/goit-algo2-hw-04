class TrieNode:
    """Внутрішній вузол Trie."""
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None


class Trie:
    """
    Проста реалізація префіксного дерева (Trie).

    Методи:
    - put(key, value): додати слово key з пов'язаним значенням value.
    - get(key, default=None): отримати значення для слова key, або default, якщо його немає.
    """

    def __init__(self):
        self.root = TrieNode()

    def put(self, key, value):
        """Додає слово key до Trie та зберігає для нього value."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.value = value

    def get(self, key, default=None):
        """Повертає value для key, якщо слово є в Trie, інакше default."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        node = self.root
        for ch in key:
            if ch not in node.children:
                return default
            node = node.children[ch]
        if node.is_end:
            return node.value
        return default
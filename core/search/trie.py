from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TrieNode:
    """
    A node in the ContentTrie.

    Attributes:
        children: Mapping of character -> child TrieNode.
        values: List of values stored at this node when it represents
                the end of one or more inserted keys.
        is_terminal: True if this node marks the end of at least one key.
    """

    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    values: List[Any] = field(default_factory=list)
    is_terminal: bool = False


class ContentTrie:
    """
    Trie for efficient prefix-based search of content.

    Keys are normalized to lowercase, making the trie case-insensitive.

    Example:
        trie = ContentTrie()
        trie.insert("arrays", "Arrays - Introduction")
        trie.insert("arraylist", "ArrayList - Dynamic Arrays")

        results = trie.autocomplete("arr")
        # results contains both values.
    """

    def __init__(self) -> None:
        self._root = TrieNode()

    @staticmethod
    def _normalize_key(key: str) -> str:
        """
        Normalize keys before inserting/searching.

        Currently this just lowercases the string, making search case-insensitive.
        """
        return key.lower()

    def insert(self, key: str, value: Any) -> None:
        """
        Insert a (key, value) pair into the trie.

        Args:
            key: The string key, such as a title or keyword.
            value: Arbitrary value associated with the key (course ID, title, object, etc.).
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        normalized = self._normalize_key(key)
        node = self._root

        # Traverse or create nodes for each character
        for ch in normalized:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]

        node.is_terminal = True
        node.values.append(value)

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """
        Find the node corresponding to the end of the given prefix.

        Returns:
            The TrieNode for the prefix, or None if the prefix is not present.
        """
        normalized = self._normalize_key(prefix)
        node = self._root

        for ch in normalized:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def autocomplete(self, prefix: str) -> List[Any]:
        """
        Return all values whose keys start with the given prefix.

        Args:
            prefix: The prefix to search for.
                    If empty string, returns all values stored in the trie.

        Returns:
            A list of values associated with keys that share this prefix.
        """
        # Special case: empty prefix -> everything
        if prefix == "":
            start_node = self._root
        else:
            start_node = self._find_node(prefix)
            if start_node is None:
                return []

        collected: List[Any] = []
        self._collect_values(start_node, collected)
        return collected

    def _collect_values(self, node: TrieNode, collected: List[Any]) -> None:
        """
        Depth-first traversal from the given node, collecting all values.
        """
        if node.is_terminal:
            collected.extend(node.values)

        for child in node.children.values():
            self._collect_values(child, collected)

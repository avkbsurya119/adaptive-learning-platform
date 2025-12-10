import pytest

from core.search.trie import ContentTrie


def test_insert_and_autocomplete_basic():
    trie = ContentTrie()
    trie.insert("arrays", "Arrays - Intro")
    trie.insert("linked lists", "Linked Lists - Intro")

    results = trie.autocomplete("arr")
    assert "Arrays - Intro" in results
    assert "Linked Lists - Intro" not in results


def test_shared_prefix_returns_all_matches():
    trie = ContentTrie()
    trie.insert("sort", "Sorting - Overview")
    trie.insert("sorting", "Sorting Algorithms")
    trie.insert("search", "Searching Algorithms")

    results = trie.autocomplete("sort")
    assert len(results) == 2
    assert "Sorting - Overview" in results
    assert "Sorting Algorithms" in results
    assert "Searching Algorithms" not in results


def test_no_matches_returns_empty_list():
    trie = ContentTrie()
    trie.insert("arrays", "Arrays")
    trie.insert("linked lists", "Linked Lists")

    results = trie.autocomplete("graph")
    assert results == []


def test_case_insensitive_search():
    trie = ContentTrie()
    trie.insert("Arrays", "Arrays - Uppercase Insert")
    trie.insert("aRRAYlist", "ArrayList - Mixed Case")

    # Different prefix cases:
    results_lower = trie.autocomplete("arr")
    results_upper = trie.autocomplete("ARR")
    results_mixed = trie.autocomplete("ArR")

    # All should be equivalent and contain both inserted values
    for results in (results_lower, results_upper, results_mixed):
        assert len(results) == 2
        assert "Arrays - Uppercase Insert" in results
        assert "ArrayList - Mixed Case" in results


def test_empty_prefix_returns_all_values():
    trie = ContentTrie()
    values = [
        "Arrays",
        "Linked Lists",
        "Stacks",
        "Queues",
    ]
    for v in values:
        trie.insert(v, v)

    results = trie.autocomplete("")
    # Order is not guaranteed, but contents should match
    assert sorted(results) == sorted(values)


def test_inserting_multiple_values_for_same_key():
    trie = ContentTrie()
    trie.insert("dp", "Dynamic Programming - Basics")
    trie.insert("dp", "Dynamic Programming - Advanced")

    results = trie.autocomplete("dp")
    assert len(results) == 2
    assert "Dynamic Programming - Basics" in results
    assert "Dynamic Programming - Advanced" in results

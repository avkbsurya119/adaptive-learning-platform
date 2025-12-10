class TrieNode:
    def __init__(self):
        self.children = {}
        self.endOfString = False
        self.contentList = []     #For storing title,keyword,tag at the end of each word

class ContentTrie:
    def __init__(self):
        self.root = TrieNode()

    def insertContent(self, content):
        current = self.root
        for letter in content:
            node = current.children.get(letter)
            if node is None:
                node = TrieNode()
                current.children[letter] = node
            current = node
        current.endOfString = True
        current.contentList.append(content)  # Store title in a list

    def autocomplete(self, prefix):
        currentNode = self.root
        result = []

        # Find the node at the end of the prefix
        for letter in prefix:
            node = currentNode.children.get(letter)
            if node is None:
                return result  # If no matches are found
            currentNode = node

        # A recursive function to find all words starting with the prefix
        self._findAllWords(currentNode, prefix, result)
        return result

    def _findAllWords(self, node, prefix, result):
        if node.endOfString:
            result.extend(node.contentList)  # Append all content related to the prefix

        for ch, childNode in node.children.items():
            self._findAllWords(childNode, prefix + ch, result)

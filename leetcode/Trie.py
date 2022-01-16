from collections import defaultdict


class Trie:
    def __init__(self):
        self.children = defaultdict(Trie)
        self.is_leaf = False

    def insert(self, word: str) -> None:
        childs = self
        for c in word:
            childs = childs.children[c]
        childs.is_leaf = True

    def search(self, word: str) -> bool:
        childs = self
        for c in word:
            if c not in childs.children:
                return False
            childs = childs.children[c]
        return childs.is_leaf

    def startsWith(self, prefix: str) -> bool:
        childs = self
        for c in prefix:
            if c not in childs.children:
                return False
            childs = childs.children[c]
        return True


# Your Trie object will be instantiated and called as such:
obj = Trie()
obj.insert("apple")
param_2 = obj.search("apple")
param_3 = obj.startsWith("app")

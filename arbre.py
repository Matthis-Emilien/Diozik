# Objet Arbre

class Arbre:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

    def insert(self, data):
        if data < self.data:
            if self.left is None:
                self.left = Arbre(data)
                self.left.parent = self
            else:
                self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right = Arbre(data)
                self.right.parent = self
            else:
                self.right.insert(data)

    def pprint(self, level=0):
        if self.right:
            self.right.pprint(level + 1)
        print(f"{' ' * 4 * level}{self.data}")
        if self.left:
            self.left.pprint(level + 1)

    def count_children(self):
        return bool(self.left) + bool(self.right)

    def is_left_child(self):
        return self.parent and self is self.parent.left

    def is_right_child(self):
        return self.parent and self is self.parent.right

    def delete(self, data):

        arbre = self.get(data)

        if not arbre:
            return

        children_count = arbre.count_children()

        if children_count == 0:
            if arbre.is_left_child():
                arbre.parent.left = None
            else:
                arbre.parent.right = None
            del arbre

        elif children_count == 1:
            child = arbre.left or arbre.right
            if arbre.is_left_child():
                arbre.parent.left = child
                child.parent = arbre.parent
                del arbre
            elif arbre.is_right_child():
                arbre.parent.right = child
                child.parent = arbre.parent
                del arbre
            else:
                root = arbre
                root.data = child.data
                root.left = child.left
                root.right = child.right
                if child.left:
                    child.left.parent = root
                if child.right:
                    child.right.parent = root
                del child

        else:
            succ = arbre.get_successor()
            arbre.data = succ.data
            if succ.is_left_child():
                succ.parent.left = succ.right
            else:
                succ.parent.right = succ.right
            if succ.right:
                succ.right.parent = succ.parent
            del succ

# Getters

    def get(self, data):
        if data < self.data:
            return self.left.get(data) if self.left else None
        elif data > self.data:
            return self.right.get(data) if self.right else None
        return self

    def getMin(self):
        arbre = self
        while arbre.left:
            arbre = arbre.left
        return arbre

    def getMax(self):
        arbre = self
        while arbre.right:
            arbre = arbre.right
        return arbre

    def get_height(self):
        return 1 + max(
            self.left.get_height() if self.left else -1,
            self.right.get_height() if self.right else -1
        )

    def get_successor(self):
        if self.right:
            return self.right.min()
        arbre = self
        while arbre.is_right_child():
            arbre = arbre.parent
        return arbre.parent

    def get_predecessor(self):
        if self.left:
            return self.left.max()
        arbre = self
        while arbre.is_left_child():
            arbre = arbre.parent
        return arbre.parent

    def getData(self):
        return self.data
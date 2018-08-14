
class Type: pass    

class SType(Type):
    def __init__(self, label):
        self.label = label
    
    def __eq__(self, other):
        return (type(other) == type(self)) and (other.label == self.label)

    def __str__(self):
        return str(self.label)
    
class CType(Type):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        return (type(other) == type(self)) and (other.left == self.left) and (other.right == self.right)

    def __str__(self):
        return "(" + str(self.left) + " -> " + str(self.right) + ")"

class RType(Type):
    def __init__(self, _dict = dict()):
        self.types = _dict
    
    def __eq__(self, other):
        return (type(other) == type(self) and (other.types == self.types))

    def __str__(self):
        string = "{"
        for key in self.types:
            string += str(key) + " : " + str(self.types[key]) + ", "
        string = string[:-2] + "}"
        return string
    
    def set_type(self, key, value):
        self.types[key] = value
    
    def get_type(self, key):
        return self.types[key]
    
    def get_types(self):
        return self.types


class VType(Type):
    def __init__(self, _dict):
        self.types = _dict
    
    def __eq__(self, other):
        return (type(other) == type(self) and (other.types == self.types))

    def __str__(self):
        string = "<"
        for key in self.types:
            string += str(key) + " : " + str(self.types[key]) + ", "
        string = string[:-2] + ">"
        return string
    
    def set_type(self, key, value):
        self.types[key] = value
    
    def get_type(self, key):
        return self.types[key]

class BoolType(Type):
    def __str__(self):
        return "Boolean"
    def __eq__(self, other):
        return type(other) == type(self)

class IntType(Type):
    def __str__(self):
        return "Integer"
    def __eq__(self, other):
        return type(other) == type(self)

class FloatType(Type):
    def __str__(self):
        return "Float"
    def __eq__(self, other):
        return type(other) == type(self)

class StringType(Type):
    def __str__(self):
        return "String"
    def __eq__(self, other):
        return type(other) == type(self)


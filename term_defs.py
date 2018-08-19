
class Value: pass

class Term: pass

# INTERNAL TYPES ::::::::::
# string
# int
# float
# bool
        
class Integer(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        # return str("Integer(" + str(self.value) + ")")
        return str(self.value)
    def __eq__(self, other):
        return (type(other) == type(self)) and other.value == self.value

class Float(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        # return str("Float("+ str(self.value) +")")
        return str(self.value)
    def __eq__(self, other):
        return (type(other) == type(self)) and other.value == self.value

class String(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        # return str("String("+ str(self.value) +")")
        return str(self.value)
    def __eq__(self, other):
        return (type(other) == type(self)) and other.value == self.value

class Boolean(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        # return str("Boolean("+ str(self.value) +")")
        return str(self.value)
    def is_true(self):
        return bool(self.value) == True
    def __eq__(self, other):
        return (type(other) == type(self)) and other.value == self.value
    
class Var(Term):
    def __init__(self, label, T=None):
        self.label = label
        self.T = T

    def __str__(self):
        # return "Var(" + str(self.label) + ")"
        return str(self.label)

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.label == self.label)
    
    def get_label(self):
        return self.label + " "

class Abs(Term, Value):
    def __init__(self, param, given_type, body):
        self.param = param
        self.given_type = given_type
        self.body = body

    def __str__(self):
        # return "Abs(" + str(self.param) + ":" + str(self.given_type) + ".(" + str(self.body) + ")"
        return "\\" + str(self.param) + ":" + str(self.given_type) + ".(" + str(self.body) + ")"

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.param == self.param) and (other.body == self.body) and (other.given_type == self.given_type)
    
    def get_param(self) :
        return self.param
    
    def get_type(self):
        return self.given_type

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body


class App(Term):
    def __init__(self, abs, arg):
        self.abs = abs
        self.arg = arg
        self.value = False
    
    def __str__(self):
        # return "App(" + str(self.abs) + "," + str(self.arg) + ")"
        return "(" + str(self.abs) + "<-" + str(self.arg) + ")"

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.abs == self.abs) and (other.arg == self.arg)
    
    def get_abs(self):
        return self.abs

    def get_arg(self):
        return self.arg

    def is_value(self):
        return self.value
    
    def set_value(self):
        self.value = True
    
class Record(Term):
    def __init__(self, vals):
        self.vals = vals
    
    def __str__(self):
        string = "{"
        for key in self.vals:
            string += str(key) + " = " + str(self.vals[key]) + ", "
        string = string[:-2] + "}"
        return string

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.vals == self.vals)
    
    def get_value(self, key):
        return self.vals[key]

    def set_value(self, key, value):
        self.vals[key] = value
    
    def get_values(self):
        return self.vals


class Proj(Term):
    def __init__(self, record, label):
        self.record = record
        self.label = label
    
    def __str__(self):
        return "Proj(" + str(self.record) + "." + str(self.label) + ")"

    def __eq__(self, other):
        return (type(other) == type(self)) and other.record == self.record and other.label == self.label
    
    def get_record(self):
        return self.record

    def get_label(self):
        return self.label
    
  
class Tag(Term):
    def __init__(self, subtype_label, term, as_type):
        self.subtype_label = subtype_label
        self.term = term
        self.as_type = as_type
    
    def __str__(self):
        return "<" + str(self.subtype_label) + "=" + str(self.term) + "> as " + str(self.as_type)

    def __eq__(self, other):
        return (type(other) == type(self)) and other.subtype_label == self.subtype_label and other.term == self.term and other.as_type == self.as_type
    
    def get_label(self):
        return self.subtype_label
    
    def get_as_type(self):
        return self.as_type

# mapping is a map from 
class Case(Term):
    def __init__(self, tag, mapping):
        self.tag = tag
        self.mapping = mapping
    
    def __str__(self):
        string = "case " + str(self.tag) + " of [" 
        for key in self.mapping:
            string += "( " + str(key) + " ), "
        return string[:-2] + "]" 

    def __eq__(self, other):
        return type(other) == type(self) and other.tag == self.tag and other.mapping == self.mapping


class Map(Term):
    def __init__(self, subtype_label, abstr, mapped_action):
        self.subtype_label = subtype_label
        self.abstr = abstr
        self.mapped_action = mapped_action

    def __str__(self):
        return "<" + str(self.subtype_label) + "=" + str(self.abstr) + "> => " + str(self.mapped_action)

    def __eq__(self, other):
        return (type(other) == type(self)) and other.subtype_label == self.subtype_label and other.abstr == self.abstr and other.mapped_action == self.mapped_action
    
    def __hash__(self):
        return str(str(self.subtype_label) + str(self.mapped_action)).__hash__()

class Fix(Term):
    def __init__(self, term):
        self.term = term

    def __str__(self):
        return "fix " + str(self.term) 

    def __eq__(self, other):
        return (type(other) == type(self)) and other.term == self.term

class If(Term):
    def __init__(self, cond, then, _else):
        self.cond = cond
        self.then = then
        self._else = _else

    def __str__(self):
        return "if " + str(self.cond) + " then " + str(self.then) + " else " + str(self._else) + " fi"

    def __eq__(self, other):
        return type(other) == type(self) and self.cond == other.cond and self.then == other.then and self._else == other._else
    
    def get_cond(self):
        return self.cond

    def get_then(self):
        return self.then
    
    def get_else(self):
        return self._else

class Plus(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " + " + str(self.right)

    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class Minus(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " - " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class Times(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " * " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class Div(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " / " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class EQ(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return str(self.left) + " == " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class LT(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return str(self.left) + " < " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right
    

class GT(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return str(self.left) + " > " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right


class LE(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return str(self.left) + " <= " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right

class GE(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return str(self.left) + " >= " + str(self.right)
    def __eq__(self, other):
        return type(other) == type(self) and self.left == other.left and self.right == other.right


class Seq(Term):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
    def __str__(self):
        return str(self.head) + " ; " + str(self.tail)
    def __eq__(self, other):
        return type(other) == type(self) and self.head == other.head and self.tail == other.tail
    
    def get_list(self):
        h = None
        t = None
        if type(self.head) == Seq:
            h = self.head.get_list()
        else:
            h = [self.head]

        if type(self.tail) == Seq:
            t = self.tail.get_list()
        else:
            t = [self.tail]
        return h + t

class Zero(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(0)
    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

class Succ(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "succ " + str(self.value)
    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

class Pred(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "pred " + str(self.value)
    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

class ZeroTest(Term, Value):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "iszero (" + str(self.value) + ")"
    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value



class Assign(Term):
    def __init__(self, var, body):
        self.var = var
        self.body = body
    def __str__(self):
        return str(self.var) + " := " + str(self.body)
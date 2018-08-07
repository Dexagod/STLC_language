import copy

class Value: pass

class Term: pass


class Const(Term, Value):
    def __init__(self, value, T):
        self.value = value
        self.T = T

    def __str__(self):
        return "c." + str(self.value) + "::" + str(self.T)

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.value == self.value)
    
    def __hash__(self):
        return self.value.__hash__()

    def get_value(self):
        return self.value
    
    def get_type(self):
        return self.T

class Var(Term):
    def __init__(self, label, T=None):
        self.label = label
        self.T = T

    def __str__(self):
        return "v." + self.label

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
        return "(\\" + str(self.param) + ":" + str(self.given_type) + "." + str(self.body) + ")"

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
        return "(" + str(self.abs) + " " + str(self.arg) + ")"

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
            string += str(key) + " : " + str(self.vals[key]) + ", "
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
        return str(self.record) + ".=>." + str(self.label)

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
    def __init__(self, subtype_label, record, record_label):
        self.subtype_label = subtype_label
        self.record = record
        self.record_label = record_label

    def __str__(self):
        return "<" + str(self.subtype_label) + "=" + str(self.record) + "> => " + self.record_label

    def __eq__(self, other):
        return (type(other) == type(self)) and other.subtype_label == self.subtype_label and other.record == self.record and other.record_label == self.record_label
    
    def __hash__(self):
        return str(str(self.subtype_label) + str(self.record_label)).__hash__()

class Fix(Term):
    def __init__(self, term):
        self.term = term

    def __str__(self):
        return "fix " + str(self.term) 

    def __eq__(self, other):
        return (type(other) == type(self)) and other.term == self.term

class IF(Term):
    def __init__(self, cond, then, _else):
        self.cond = cond
        self.then = then
        self._else = _else

    def __str__(self):
        return "(if " + str(self.cond) + " then " + str(self.then) + " else " + str(self._else) + ")"

    def __eq__(self, other):
        return type(other) == type(self) and self.__dict__ == other.__dict__
    
    def get_cond(self):
        return self.cond

    def get_then(self):
        return self.then
    
    def get_else(self):
        return self._else




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
    def __init__(self):
        self.types = dict()
    
    def __eq__(self, other):
        return (type(other) == type(self) and (other.types == self.types))

    def __str__(self):
        string = "{"
        for key in self.types:
            string += str(key) + " ~ " + str(self.types[key]) + ", "
        string = string[:-2] + "}"
        return string
    
    def set_type(self, key, value):
        self.types[key] = value
    
    def get_type(self, key):
        return self.types[key]
    
    def get_types(self):
        return self.types


class VType(Type):
    def __init__(self):
        self.types = dict()
    
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



def typecheck_exp(exp, context):
    print("checking", exp, context)
    exp_class = type(exp)

    if exp_class == Const:
        T = exp.get_type()
        print(T, exp.get_value())
        if T == 'bool' and (exp.get_value() != 'true' and exp.get_value() != 'false'):
            raise Exception(str(exp.get_value()) + " is not of type 'bool'")

        if T == 'int' and not isinstance(exp.get_value(), int):
            raise Exception("'" + str(exp.get_value()) +  "' is not of type 'int'")

        return T

    if exp_class == Var:
        if exp.get_label() in context:
            return context[exp.get_label()]
        else:
            raise Exception(str(exp) + " is not in context")
    
    elif exp_class == Abs:
        new_context = context.copy()
        new_context[exp.get_param().get_label()] = exp.get_type() 
        body_type = typecheck_exp(exp.get_body(), new_context)  
        return CType(exp.get_type(), body_type)

    elif exp_class == Record:
        record_type = RType()
        value_dict = exp.get_values()
        for key in value_dict:
            record_type.set_type(key, typecheck_exp(value_dict[key], context))
        return record_type
    
    elif exp_class == Proj:
        record_type = typecheck_exp(exp.record, context)
        if not exp.label in record_type.get_types():
            raise Exception("label " + str(exp.label) + " was not found in RType " + str(record_type))
        else:
            return record_type.get_type(exp.label)
    
    elif exp_class == Tag:
        if not issubclass(type(exp.get_as_type()), Type):
            raise Exception("Tag " + str(exp) + " did not receive a correct type")
        return exp.get_as_type()
    
    elif exp_class == Case:
        # TODO:: WHAT IF TAG IS NOT A TAG BUT A VAR TO BE REPLACED OR STH
        supertype = exp.tag.as_type
        tag_subtype_label = exp.tag.subtype_label
        subtype = supertype.get_type(tag_subtype_label)

        if type(subtype) != RType:
            raise Exception("The subtype of the variant was no record type")

        shared_type = None
        for m in exp.mapping:
            subT = supertype.get_type(m.subtype_label)
            found_type = subT.get_type(m.record_label)
            if shared_type == None:
                shared_type = found_type
            else:
                if shared_type != found_type:
                    raise Exception("The case statement can return more than one type")

        record_label = ""
        for m in exp.mapping:
            if m.subtype_label == tag_subtype_label:
                record_label = m.record_label
            

        if record_label == "":
            raise Exception("There was no mapping for this subtype")

        return subtype.get_type(record_label)
    
    
        
    elif exp_class == App:
        t_abs = typecheck_exp(exp.abs, context)
        t_arg = typecheck_exp(exp.arg, context)

        # THE PROBLEM IS THAT THE ARGUMENT ONLY GIVES TYPE::int for example, however we do not posess the label itself, so are unable to return the
        if type(t_abs) != CType:
            string = str("Application " + str(exp) + " first type is not a CType but " + str(t_abs) + " and second type is " + str(t_arg))
            raise Exception(string)
        
        if t_arg != t_abs.left:
            string = str("Application " + str(exp) + " types do not match: left_type = " + str(t_abs) + " | right_type = " + str(t_arg))
            raise Exception(string)
        return t_abs.right

    elif exp_class == Fix:
        term_type = typecheck_exp(exp.term, context)
        if type(term_type) != CType:
            raise Exception("Fix argument has type " + str(type(exp.term)) + " instead of a type T->T")
        if term_type.left != term_type.right:
            raise Exception("Fix argument left type " + str(term_type.left) + " does not match the right type " + str(term_type.right))
        return term_type.right


    # def __init__(self, cond, then, _else):
    elif exp_class == IF:
        cond_type = typecheck_exp(exp.get_cond(), context)
        then_type = typecheck_exp(exp.get_then(), context)
        else_type = typecheck_exp(exp.get_else(), context)
        if cond_type != 'bool':
            raise Exception("If-statement conditional is not of type 'bool'")
        elif then_type != else_type:
            s = "If-statement then has type '" + exp.get_then().get_type() + "' while else has type '" + exp.get_else().get_type() + "'"
            raise Exception(s)
        else:
            return else_type

def eval_exp(exp):
    
    print("EVAL", exp)
    exp_class = type(exp)


    if exp_class == Const: # Abs
        # print("EVAL - CONST")
        return exp
        
    if exp_class == Abs: # Abs
        # print("EVAL - ABS")
        return exp
    
    elif exp_class == Var:
        # print("EVAL - VAR")
        return exp
    
    elif exp_class == Record:
        # print("E-RCD")
        for key in exp.get_values():
            new_value = eval_exp(exp.get_value(key))
            exp.set_value(key, new_value)
        return exp

    elif exp_class == Proj:
        # print("E-PROJ")
        exp.record = eval_exp(exp.record)
        return exp.record.get_value(exp.label)

    
    elif exp_class == Tag:
        # print("E-VARIANT")
        exp.term = eval_exp(exp.term)
        return exp

    elif exp_class == Case:
        # print("E-CASE")
        exp.tag = eval_exp(exp.tag)
        if type(exp.tag) == Tag:
            mapping = exp.mapping
            tag = exp.tag
            subtype_label = tag.subtype_label
            record_label = ""
            for m in mapping:
                if m.subtype_label == subtype_label:
                    record_label = m.record_label
            if record_label == "":
                raise Exception("subtype label not found in Variant")
            
            return eval_exp(Proj(tag.term, record_label))
        else:
            return exp
    
    elif exp_class == Fix:
        if type(exp.term) != Abs:
            raise Exception("Fix body is an: " + str(type(exp.term)) + " instead of an Abs")
        else:
            t2 = exp.term.body
            substituted_term = application_substitution(t2, exp.term.param, exp) # TODO:: deepcopy of exp
            return substituted_term


    elif exp_class == IF:
        if not issubclass(type(exp.get_cond()), Value):
            cond_eval = eval_exp(exp.get_cond())
            exp.cond = cond_eval
            return exp
        else:
            cond_val = exp.get_cond().get_value()
            if type(exp.get_cond()) == Const:
                if not (cond_val == 'true' or cond_val == 'false'):
                    raise Exception("Constant boolean value is not 'true' or 'false'")
                elif cond_val == 'true':
                    return exp.get_then()
                else:
                    return exp.get_else()
            else:
                return exp


    #  NAKIJKEN OF VOLDOET AAN DE REGELS
    elif exp_class == App:
        e_abs = exp.abs
        e_arg = exp.arg


        if not issubclass(type(e_abs), Value):
            print("E-APP1")
            evaluated_abstraction = eval_exp(e_abs)
            if evaluated_abstraction != e_abs:
                return eval_exp( App(evaluated_abstraction, e_arg) )

        if not issubclass(type(e_arg), Value):
            print("E-APP2")
            evaluated_argument = eval_exp(e_arg)
            if evaluated_argument != e_arg:
                return eval_exp( App(e_abs, evaluated_argument) )
        
        if type(e_abs) == Abs:
            print("E-APPABS")
            abstr_param = e_abs.get_param()
            body = e_abs.get_body()
            arg = e_arg
            substituted_exp = application_substitution(body, abstr_param, arg)
            return substituted_exp # evaluate once more?

        if type(e_abs) == Record:
            print("E-PROJRCD")
            try:
                return e_abs.get_value(e_arg)
            except Exception:
                raise Exception("Record " + str(e_abs) + " does not contain label " + str(e_arg))
            

        if not exp.is_value and (issubclass(type(e_abs), Value) and issubclass(type(e_arg), Value)):
            exp.set_value()
            return eval_exp(exp)

        return exp


def application_substitution(abstraction_body, abstraction_param, arg):
    print("substitution", abstraction_body, "|", abstraction_param, "|", arg)

    if type(abstraction_body) is Const:
        return abstraction_body

    if type(abstraction_body) is Var:
        if abstraction_body == abstraction_param:
            print("SUBSTITUTED", " - " , abstraction_body, " - " , arg)
            return arg # TODO:: deepcopy
        else:
            # print("SUBST - VAR - NO")
            return abstraction_body
    
    if type(abstraction_body) is Record:
        for key in abstraction_body.get_values():
            substituted_value = application_substitution(abstraction_body.get_value(key), abstraction_param, arg)
            abstraction_body.set_value(key, substituted_value)
        return abstraction_body

    if type(abstraction_body) is Proj:
        # E-PROJ
        abstraction_body.record = application_substitution(abstraction_body.record, abstraction_param, arg)
        return abstraction_body
    
    # TODO:: RULES FOR VARIANTS NEED TO BE ADDED
    if type(abstraction_body) is Tag:
        # E-Variant
        abstraction_body.term = application_substitution(abstraction_body.term, abstraction_param, arg)
        return abstraction_body
    
    if type(abstraction_body) is Case:
        # E-CASE
        abstraction_body.tag = application_substitution(abstraction_body.tag, abstraction_param, arg)
        return abstraction_body

    elif type(abstraction_body) is Fix:
        # E-FIX
        abstraction_body.term = substituted_value(abstraction_body.term, abstraction_param, arg)

    elif type(abstraction_body) is Abs:
        # E-APPABS
        param = abstraction_body.get_param()
        # if abstraction argument is equal to argument, it also has to be replaced.
        if param != abstraction_param:
            s_body = application_substitution(abstraction_body.get_body(), abstraction_param, arg)
            abstraction_body.body = s_body
        return abstraction_body
            
    elif type(abstraction_body) is App:
        # E-APP1, E-APP2
        app_abs = abstraction_body.get_abs()
        app_arg = abstraction_body.get_arg()
        print("substleft")
        abstraction_body.abs = application_substitution(app_abs, abstraction_param, arg)
        print("substright")
        abstraction_body.arg = application_substitution(app_arg, abstraction_param, arg)
        return abstraction_body

def evaluate_expression(exp):
    exp_copy = copy.deepcopy(exp)
    evaluated = eval_exp(exp_copy)
    print(evaluated, exp)
    while evaluated != exp:
        exp = evaluated
        exp_copy = copy.deepcopy(exp)
        evaluated = eval_exp(exp_copy)

    return evaluated


if __name__ == "__main__":
    

    # int_type = SType("int")
    # int_int_type = CType(int_type, int_type)
    # int_int_to_int_int_type = CType(int_int_type, int_int_type)

    # const_zero = Const(0, int_type)
    # const_succ = Const("succ", int_int_type)

    # one = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), Var("z"))))
    # two = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), App(Var("s"), Var("z") ) ) ) )
    # two2 = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), App(Var("s"), Var("z") ) ) ) )

    # addition = Abs(Var("m"), int_int_to_int_int_type, Abs(Var("n"), int_int_to_int_int_type, Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App( App(Var("m"), Var("s")), App( App( Var("n"), Var("s")), Var("z") )) ) ) ) )

    # successor = Abs(Var("n"), int_int_to_int_int_type, Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App( Var("s"), App( App( Var("n"), Var("s")), Var("z") )) ) ) )

    # oneplustwo = App(App(addition, one), two)

    # oneplustwowithargs = App(App(App(App(addition, one), two), Const("succ", int_int_type)), Const(0, int_type))

    # twoplustwowithargs = App(App(App(App(addition, two), two2), Const("succ", int_int_type)), Const(0, int_type))

    # successorone = App(App(App(successor, one), Const("succ", int_int_type)), Const(0, int_type))

    # # TODO:: FIX IN PARSER
    # record_dict = dict()
    # record_dict[1] = Abs(Var("x"), int_type, Var("x"))
    # record_dict[2] = App(Abs(Var("x"), int_type, Var("x")), Const(2, SType("int")))
    # record_dict["test"] = Const("4", SType("str"))
    # record = Record(record_dict)
    # record_application = Proj( Record(record_dict), "test")

    # record_type = typecheck_exp(record, dict(""))
    # record_application2 = Proj( App(Abs( Var("x"), record_type, Var("x")), Record(record_dict)), 1)
    
    # rd3 = dict()
    # rd3["a"] = Const("KOK", SType("string"))
    # rd3["b"] = Const(2, SType("int"))
    # r3 = Record(rd3)
    # r3type = typecheck_exp(r3, dict())


    # rd1 = dict()
    # rd1["a"] = Var("z") # Const("KOK", SType("string"))
    # rd1["b"] = Const(2, SType("int"))
    # r1 = Record(rd1)
    # # r1type = typecheck_exp(r1, dict())
    # rd2 = dict()
    # rd2["c"] = Const("kuk", SType("string"))
    # rd2["d"] = Const(4, SType("int"))
    # r2 = Record(rd2)
    # r2type = typecheck_exp(r2, dict())
    # td = dict()
    # td["one"]=r3type#r1type
    # td["two"]=r2type
    # vtype = VType()
    # vtype.types = td
    # print("vtype", vtype)
    # a = Tag("one", Var("x"), vtype)
    # mapping = set()
    # mapping.add(Map("one", r1, "a"))
    # mapping.add(Map("two", r2, "c"))
    # # getname = App(Abs( Var("x"), vtype, Case(Var("x"), mapping)), Tag("one", Record(rd1), vtype))
    # getname = App(Abs( Var("z"), SType("string"), App(Abs( Var("x"), vtype, Case(Var("x"), mapping)), Tag("one", Record(rd1), vtype))), Const("appel",SType("string")))
    # print(evaluate_expression(getname))
    # print(typecheck_exp(getname, dict()))


    print("")
    print("")
    print("")
    print("")

    exp = IF(App(Abs(Var("x"), 'bool', Var("x")), Const('false', 'bool')), Const(5, 'int'), Const(10, 'int') )

    ev = evaluate_expression(exp)
    print("evaluated", ev)
    print("")
    print(typecheck_exp(exp, dict()))

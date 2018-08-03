

class Value: pass

class Term: pass


class Const(Term, Value):
    def __init__(self, value, T):
        self.value = value
        self.T = T

    def __str__(self):
        # return "Const(" + str(self.value) + ", " + str(self.T) + ")"
        return "c." + str(self.value) + "::" + str(self.T)
        #return str(self.value)

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
        # return "Var(" + str(self.labsel) + ")"
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
        # return "Abs(" + str(self.param) + ", " + str(self.given_type) + ", " + str(self.body) + ")"
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
        # return "App(" + str(self.abs) + ", " + str(self.arg) + ")"
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
  
class Tag(Term):
    def __init__(self, label, term, as_type):
        self.label = label
        self.term = term
        self.as_type = as_type
    
    def __str__(self):
        return "<" + str(self.label) + "=" + str(self.term) + "> as " + str(self.as_type)

    def __eq__(self, other):
        return (type(other) == type(self)) and other.label == self.label and other.term == self.term and other.as_type == self.as_type
    
    def get_label(self):
        return self.label

    def get_term(self):
        return self.term
    
    def get_as_type(self):
        return self.as_type

class Case(Term):
    def __init__(self, term, mapping):
        self.term = term
        self.mapping = mapping
    
    def __str__(self):
        string = "case " + str(self.term) + " of [" 
        for key in self.mapping:
            string += "( " + key + " => " + self.mapping[key] + " ), "
        return string[:-2] + "]" 

    def __eq__(self, other):
        return type(other) == type(self) and other.term == self.term and other.mapping == self.mapping

    def get_term(self):
        return self.term
    
    def get_mapping(self):
        return self.mapping


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
            string += str(key) + " : " + str(self.types[key]) + ", "
        string = string[:-2] + "}"
        return string
    
    def set_type(self, key, value):
        self.types[key] = value
    
    def get_type(self, key):
        return self.types[key]


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
    
    exp_class = type(exp)

    if exp_class == Const:
        return exp.get_type()

    if exp_class == Var:
        if exp.get_label() in context:
            return context[exp.get_label()]
        else:
            raise Exception("Var" + str(exp) + " is not in context")
    
    elif exp_class == Abs:
        new_context = context.copy()
        new_context[exp.get_param().get_label()] = exp.get_type() 
        body_type = typecheck_exp(exp.get_body(), new_context)  
        return CType(exp.get_type(), body_type)

    elif exp_class == Record:
        record_type = RType()
        value_dict = exp.get_values()
        for key in value_dict:
            if type(key) != Const:
                raise Exception("Record key is not a constant")
            else:
                record_type.set_type(key, typecheck_exp(value_dict[key], context))
        return record_type
    
    elif exp_class == Tag:
        if not issubclass(exp.get_as_type(), Type):
            raise Exception("Tag " + str(exp) + " did not receive a correct type")
        elif not type(exp.get_label()) != Const:
            raise Exception("Tag " + str(exp) + " did not receive a Const as label")
        
        

    elif exp_class == App:
        t_abs = typecheck_exp(exp.abs, context)
        t_arg = typecheck_exp(exp.arg, context)
        if type(t_abs) != CType:
            string = str("Application " + str(exp) + " first type is not a CType but " + str(t_abs) + " and second type is " + str(t_arg))
            raise Exception(string)
        
        if t_arg != t_abs.left:
            string = str("Application " + str(exp) + " types do not match")
            raise Exception(string)
        return t_abs.right
    

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
        # print("E-PROJ + E-RCD")
        for key in exp.get_values():
            new_value = eval_exp(exp.get_value(key))
            exp.set_value(key, new_value)
        return exp
    
    elif exp_class == Tag:
        # print("E-PROJ + E-RCD")
        for key in exp.get_values():
            new_value = eval_exp(exp.get_value(key))
            exp.set_value(key, new_value)
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
            return e_abs.get_value(e_arg)
            

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
            return arg
        else:
            # print("SUBST - VAR - NO")
            return abstraction_body
    
    if type(abstraction_body) is Record:
        for key in abstraction_body:
            abstraction_body[key] = application_substitution(abstraction_body[key], abstraction_param, arg)


    elif type(abstraction_body) is Abs:
        # print("SUBST - ABS")
        param = abstraction_body.get_param()
        # if abstraction argument is equal to argument, it also has to be replaced.
        if param != abstraction_param:
            s_body = application_substitution(abstraction_body.get_body(), abstraction_param, arg)
            abstraction_body.body = s_body
        return abstraction_body
            
    elif type(abstraction_body) is App:
        # print("SUBST - APP")
        app_abs = abstraction_body.get_abs()
        app_arg = abstraction_body.get_arg()
        print("substleft")
        abstraction_body.abs = application_substitution(app_abs, abstraction_param, arg)
        print("substright")
        abstraction_body.arg = application_substitution(app_arg, abstraction_param, arg)
        return abstraction_body




if __name__ == "__main__":
    

    int_type = SType("int")
    int_int_type = CType(int_type, int_type)
    int_int_to_int_int_type = CType(int_int_type, int_int_type)

    const_zero = Const(0, int_type)
    const_succ = Const("succ", int_int_type)

    one = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), Var("z"))))
    two = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), App(Var("s"), Var("z") ) ) ) )
    two2 = Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App(Var("s"), App(Var("s"), Var("z") ) ) ) )

    addition = Abs(Var("m"), int_int_to_int_int_type, Abs(Var("n"), int_int_to_int_int_type, Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App( App(Var("m"), Var("s")), App( App( Var("n"), Var("s")), Var("z") )) ) ) ) )

    successor = Abs(Var("n"), int_int_to_int_int_type, Abs(Var("s"), int_int_type, Abs( Var("z"), int_type, App( Var("s"), App( App( Var("n"), Var("s")), Var("z") )) ) ) )

    oneplustwo = App(App(addition, one), two)

    oneplustwowithargs = App(App(App(App(addition, one), two), Const("succ", int_int_type)), Const(0, int_type))

    twoplustwowithargs = App(App(App(App(addition, two), two2), Const("succ", int_int_type)), Const(0, int_type))

    successorone = App(App(App(successor, one), Const("succ", int_int_type)), Const(0, int_type))

    # TODO:: FIX IN PARSER
    record_dict = dict()
    record_dict[Const("1", SType("String"))] = Abs(Var("x"), int_int_type, Var("x"))
    record_dict[Const("2", SType("String"))] = App(Abs(Var("x"), int_int_type, Var("x")), Const(2, SType("Integer")))
    record_dict[Const(3, SType("Integer"))] = Const("4", SType("String"))
    record = Record(record_dict)

    print(eval_exp(record))
    print(typecheck_exp(record, dict()))

    # exp = twoplustwowithargs
    # print("TYPECHECKING")
    # print(typecheck_exp(exp, dict()))

    # evaluated = eval_exp(exp)
    # while (evaluated != exp):
    #     print("NEXTWHILE")
    #     exp = evaluated
    #     evaluated = eval_exp(evaluated)
    
    # print(evaluated)

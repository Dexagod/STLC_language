import copy
from term_defs import *
from type_defs import *

def typecheck_exp(exp, context):
    print("checking", exp, context)
    exp_class = type(exp)

    if exp_class == Integer:
        return IntType()

    if exp_class == Float:
        return FloatType()

    if exp_class == String:
        return StringType()

    if exp_class == Boolean:
        return BoolType()

    if exp_class == Var:
        if exp.get_label() in context:
            return context[exp.get_label()]
        else:
            raise Exception(str(exp) + " not found in current context")
    
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
        # TODO:: WHAT If TAG IS NOT A TAG BUT A VAR TO BE REPLACED OR STH
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
    elif exp_class == If:
        cond_type = typecheck_exp(exp.get_cond(), context)
        if type(cond_type) != BoolType:
            string = "If-statement conditional is not of type 'Boolean' but has type " + str(cond_type)
            raise Exception(string)

        then_type = typecheck_exp(exp.get_then(), context)
        else_type = typecheck_exp(exp.get_else(), context)
        if then_type != else_type:
            s = "If-statement then has type '" + exp.get_then().get_type() + "' while else has type '" + exp.get_else().get_type() + "'"
            raise Exception(s)
        else:
            return else_type
    
    elif exp_class == Plus or exp_class == Minus or exp_class == Times or exp_class == Div:
        left_type = typecheck_exp(exp.left, context)
        right_type = typecheck_exp(exp.right, context)
        if type(left_type) != IntType and type(left_type) != FloatType:
            raise Exception("Left argument of plus is not of type 'Integer' or type 'Float'")
        if type(right_type) != IntType and type(right_type) != FloatType:
            raise Exception("Right argumeright_typent of plus is not of type 'Integer' or type 'Float'")
        if left_type != right_type:
            raise Exception("Operand arguments must both be of the same type.")
        return left_type

    elif exp_class == LT or exp_class == GT or exp_class == LE or exp_class == GE:
        left_type = typecheck_exp(exp.left, context)
        right_type = typecheck_exp(exp.right, context)
        if type(left_type) != IntType and type(left_type) != FloatType:
            raise Exception("Left argument of plus is not of type 'Integer' or type 'Float'")
        if type(right_type) != IntType and type(right_type) != FloatType:
            raise Exception("Right argument of plus is not of type 'Integer' or type 'Float'")
        if left_type != right_type:
            raise Exception("Operand arguments must both be of the same type.")
        return BoolType()
    
    elif exp_class == EQ:
        left_type = typecheck_exp(exp.left, context)
        right_type = typecheck_exp(exp.right, context)
        if not (type(left_type) == IntType or type(left_type) == FloatType or type(left_type) == StringType or type(left_type) == BoolType):
            raise Exception("Left argument of equals is not valid")
        if not (type(right_type) == IntType or type(right_type) == FloatType or type(right_type) == StringType or type(right_type) == BoolType):
            raise Exception("Right argument of equals is not valid'")
        if left_type != right_type:
            raise Exception("Operand arguments must both be of the same type.")
        return BoolType()



def eval_exp(exp):
    
    print("EVAL", exp)
    exp_class = type(exp)

    if exp_class == Integer or exp_class == Float or exp_class == String or exp_class == Boolean:
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
    
    # elif exp_class == Fix:
    #     # TODO:: FIX THIS
    #     if type(exp.term) != Abs:
    #         exp.term = eval_exp(exp.term)
    #         return exp
    #     else:
    #         t2 = copy.deepcopy(exp.term.body)
    #         substituted_term = application_substitution(t2, exp.term.param, exp) 
    #         return substituted_term
    

    elif exp_class == Fix:
        return eval_exp(App(Abs(Var("f"), SType, App( Abs(Var("x"), SType, App( Var("f"), App(Var("x"), Var("x")) )), Abs(Var("x"), xtype, App( Var("f"), App(Var("x"), Var("x")))))), exp.term))

    elif exp_class == If:
        if not issubclass(type(exp.get_cond()), Value):
            cond_eval = eval_exp(exp.get_cond())
            exp.cond = cond_eval
            return exp
        else:
            cond_val = exp.get_cond()
            if type(cond_val) == Boolean:
                if cond_val.is_true():
                    return eval_exp(exp.get_then())
                else:
                    return eval_exp(exp.get_else())
            else:
                return exp
    
    elif exp_class == Plus or exp_class == Minus or exp_class == Times or exp_class == Div:
        if not (type(exp.left) == Integer or type(exp.left) == Float):
            exp.left == eval_exp(exp.left)
            return exp
        if not (type(exp.right) == Integer or type(exp.right) == Float):
            exp.right == eval_exp(exp.right)
            return exp
        return substitute_expression(exp)
    

    elif  exp_class == LT or exp_class == GT or exp_class == LE or exp_class == GE:
        if not (type(exp.left) == Integer or type(exp.left) == Float):
            exp.left == eval_exp(exp.left)
            return exp
        if not (type(exp.right) == Integer or type(exp.right) == Float):
            exp.right == eval_exp(exp.right)
            return exp
        return substitute_expression(exp)

    elif exp_class == EQ:
        if not (type(exp.left) == Integer or type(exp.left) == Float or type(exp.left) == String or type(exp.left) == Boolean):
            exp.left == eval_exp(exp.left)
            return exp
        if not (type(exp.right) == Integer or type(exp.right) == Float or type(exp.right) == String or type(exp.right) == Boolean):
            exp.right == eval_exp(exp.right)
            return exp
        return substitute_expression(exp)



    #  NAKIJKEN OF VOLDOET AAN DE REGELS
    elif exp_class == App:
        e_abs = exp.abs
        e_arg = exp.arg


        if not issubclass(type(e_abs), Value):
            # print("E-APP1")
            evaluated_abstraction = eval_exp(e_abs)
            if evaluated_abstraction != e_abs:
                return eval_exp( App(evaluated_abstraction, e_arg) )

        if not issubclass(type(e_arg), Value):
            # print("E-APP2")
            evaluated_argument = eval_exp(e_arg)
            if evaluated_argument != e_arg:
                return eval_exp( App(e_abs, evaluated_argument) )
        
        if type(e_abs) == Abs:
            # print("E-APPABS")
            abstr_param = e_abs.get_param()
            body = e_abs.get_body()
            arg = e_arg
            substituted_exp = application_substitution(body, abstr_param, arg)
            return substituted_exp # evaluate once more?

        if type(e_abs) == Record:
            # print("E-PROJRCD")
            try:
                return e_abs.get_value(e_arg)
            except Exception:
                raise Exception("Record " + str(e_abs) + " does not contain label " + str(e_arg))

        if not exp.is_value and (issubclass(type(e_abs), Value) and issubclass(type(e_arg), Value)):
            exp.set_value()
            return eval_exp(exp)

        return exp


def application_substitution(abstraction_body, abstraction_param, arg):
    # print("substitution", abstraction_body, "|", abstraction_param, "|", arg)

    if type(abstraction_body) == Integer or type(abstraction_body) == Float or type(abstraction_body) == String or type(abstraction_body) == Boolean:
        return abstraction_body

    if type(abstraction_body) is Var:
        if abstraction_body == abstraction_param:
            # print("SUBSTITUTED", " - " , abstraction_body, " - " , arg)
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
        abstraction_body.term = application_substitution(abstraction_body.term, abstraction_param, arg)

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
        # print("substleft")
        abstraction_body.abs = application_substitution(app_abs, abstraction_param, arg)
        # print("substright")
        abstraction_body.arg = application_substitution(app_arg, abstraction_param, arg)
        return abstraction_body
    
    elif type(abstraction_body) == Plus or type(abstraction_body) == Minus or type(abstraction_body) == Times or type(abstraction_body) == Div:
        abstraction_body.left = application_substitution(abstraction_body.left, abstraction_param, arg)
        abstraction_body.right = application_substitution(abstraction_body.right, abstraction_param, arg)
        return abstraction_body

    elif type(abstraction_body) == EQ or type(abstraction_body) == LT or type(abstraction_body) == GT or type(abstraction_body) == LE or type(abstraction_body) == GE:
        abstraction_body.left = application_substitution(abstraction_body.left, abstraction_param, arg)
        abstraction_body.right = application_substitution(abstraction_body.right, abstraction_param, arg)
        return abstraction_body
     
    

def substitute_expression(exp):
    expr_kind = type(exp)

    if expr_kind == Plus:
        exp.left.value = exp.left.value + exp.right.value
        return exp.left

    if expr_kind == Minus:
        exp.left.value = exp.left.value - exp.right.value
        return exp.left

    if expr_kind == Times:
        exp.left.value = exp.left.value * exp.right.value
        return exp.left
    
    if expr_kind == Div:
        exp.left.value = exp.left.value / exp.right.value
        return exp.left

    if expr_kind == EQ:
        exp.left.value = exp.left.value == exp.right.value
        return exp.left

    if expr_kind == LT:
        exp.left.value = exp.left.value < exp.right.value
        return exp.left

    if expr_kind == GT:
        exp.left.value = exp.left.value > exp.right.value
        return exp.left

    if expr_kind == LE:
        exp.left.value = exp.left.value <= exp.right.value
        return exp.left

    if expr_kind == GE:
        exp.left.value = exp.left.value >= exp.right.value
        return exp.left

def evaluate_expression(exp):
    exp_copy = copy.deepcopy(exp)
    evaluated = eval_exp(exp_copy)
    while evaluated != exp:
        exp = evaluated
        exp_copy = copy.deepcopy(exp)
        evaluated = eval_exp(exp_copy)
    return evaluated


def typecheck_expression(exp, context):
    checked = typecheck_exp(exp, context)
    return str(checked)



# if __name__ == "__main__":

    

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

    # expressions = []
    # expressions.append( If(App(Abs(Var("x"), BoolType(), Var("x")), Boolean('false')), Boolean("true"), Boolean("false") ) )
    # expressions.append( Plus(Float(3), Float(4)) )

    # expressions.append( 
    #     App(
    #         Fix(
    #             Abs(
    #                 Var("fct"), CType(IntType, IntType), 
    #                     Abs(Var("n"), IntType, 
    #                         If( 
    #                             EQ(Var("n"), Integer(0)), 
    #                             Integer(1), 
    #                             Times(Var("n"), App(
    #                                 Var("fct"), 
    #                                 Minus( Var("n"), Integer(1))
    #                             )
    #                         )
    #                     )
    #                 )
    #             ) 
    #         ),
    #         Integer(5)
    #     )
    # )
    
    # for exp in expressions:
    #     print('')
    #     typechecked = typecheck_expression(exp, dict())
    #     print('typechecked:\n', typechecked)
    #     ev = evaluate_expression(exp)
    #     print("evaluated:\n", ev)



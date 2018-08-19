import copy
from term_defs import *
from type_defs import *

def typecheck_exp(exp, context):
    
    exp_class = type(exp)

    if exp_class == Zero:
        return IntType()

    if exp_class == Succ:
        term_type = typecheck_exp(exp.value, context)
        if type(term_type) != IntType:
            string = str(exp.value) + " is not an integer type"
            print(term_type)
            raise Exception(string)
        return IntType()

    if exp_class == Pred:
        term_type = typecheck_exp(exp.value, context)
        if type(term_type) != IntType:
            string = str(exp.value) + " is not an integer type"
            print(term_type)
            raise Exception(string)
        return IntType()

    if exp_class == ZeroTest:
        term_type = typecheck_exp(exp.value, context)
        if type(term_type) != IntType:
            string = str(exp.value) + " is not an integer type"
            print(term_type)
            raise Exception(string)
        return BoolType()

    if exp_class == Integer:
        return IntType()

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
        
        variant_type = typecheck_exp(exp.tag, context)
        
        return_type = None
        for m in exp.mapping:
            mapped_type = variant_type.get_type(m.subtype_label)    
            newcontext = copy.deepcopy(context)
            newcontext[m.abstr.get_label()] = variant_type.get_type(m.subtype_label)
            mapped_record_type = typecheck_exp(m.mapped_action, newcontext)
            # TODO:: THIS DOES NOT USE THE VARIANT TYPE>
            if return_type == None:
                return_type = mapped_record_type
            else:
                if return_type != mapped_record_type:
                    string = str("Addressed fields of Case statement do not return equal types: " + str(mapped_type) + "   ||    " + str(mapped_record_type))
                    raise Exception(string)
        return return_type

    elif exp_class == App:
        t_abs = typecheck_exp(exp.abs, context)
        t_arg = typecheck_exp(exp.arg, context)

        # THE PROBLEM IS THAT THE ARGUMENT ONLY GIVES TYPE::int for example, however we do not posess the label itself, so are unable to return the
        if type(t_abs) != CType:
            string = str("Application " + str(exp) + " first type is not a CType but " + str(t_abs) + " and second type is " + str(t_arg))
            raise Exception(string)
        
        if t_arg != t_abs.left:
            string = str("Application " + str(exp) + " types do not match: left_type = " + str(t_abs.left) + " | right_type = " + str(t_arg))
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
            s = "If-statement then has type '" + str(then_type) + "' while else has type '" + str(else_type) + "'"
            raise Exception(s)
        else:
            return else_type

    else:
        return exp



def eval_exp(exp):
    
    # print("")
    # print("EVAL", exp)
    exp_class = type(exp)

    if exp_class == Zero:
        return exp

    if exp_class == Succ:
        # print("E-SUCC")
        exp.value = evaluate_expression(exp.value)
        return exp

    if exp_class == Pred:
        if type(exp.value) == Zero:
            # print("E-PREDZERO")
            return Zero(0)
        if type(exp.value) == Succ:
            # print("E-PREDSUCC")
            return exp.value.value
        else:
            # print("E-PRED")
            exp.value = evaluate_expression(exp.value)
            return exp

    if exp_class == ZeroTest:
        # print("E-ISZERO")
        exp.value = evaluate_expression(exp.value)
        if type(exp.value) == Zero:
            # print("E-ISZEROZERO")
            return Boolean(True)
        else:
            # print("E-ISZEROSUCC")
            return Boolean(False)

    if exp_class == String:
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
            mapped_action = ""
            for m in mapping:
                if m.subtype_label == subtype_label:
                    application_substitution(m.mapped_action, m.abstr, tag.term)
                    mapped_action = m.mapped_action
            if mapped_action == "":
                raise Exception("subtype label not found in Variant")
            
            return eval_exp(mapped_action)
        else:
            return exp
    

    elif exp_class == Fix:

        return App( Abs(Var("fix_function_variable_replacement"), "ftype", Abs(Var("fix_y_variable_replacement"), "ytype", App(App(Abs(Var("fix_x_variable_replacement"), "xtype", App(Var("fix_function_variable_replacement"), Abs(Var("fix_y_variable_replacement"), "ytype", App(App(Var("fix_x_variable_replacement"), Var("fix_x_variable_replacement")), Var("fix_y_variable_replacement"))))), Abs(Var("fix_x_variable_replacement"), "xtype", App(Var("fix_function_variable_replacement"), Abs(Var("fix_y_variable_replacement"), "ytype", App(App(Var("fix_x_variable_replacement"), Var("fix_x_variable_replacement")), Var("fix_y_variable_replacement")))))), Var("fix_y_variable_replacement")))) , exp.term)

    elif exp_class == If:
        if not issubclass(type(exp.get_cond()), Value):
            cond_eval = evaluate_expression(exp.get_cond())
            exp.cond = cond_eval
            return exp
        else:
            cond_val = evaluate_expression(exp.get_cond())
            if type(cond_val) == Boolean:
                if cond_val.is_true():
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

        if type(e_abs) == Record:
            # print("E-PROJRCD")
            try:
                return e_abs.get_value(e_arg)
            except Exception:
                raise Exception("Record " + str(e_abs) + " does not contain label " + str(e_arg))

        if type(e_abs) == Fix:
            # print("E-PROJRCD")
            eval_abs = eval_exp(e_abs)
            return eval_exp(App(eval_abs, e_arg))

        if not exp.is_value and (issubclass(type(e_abs), Value) and issubclass(type(e_arg), Value)):
            exp.set_value()
            return eval_exp(exp)

        return exp


def application_substitution(abstraction_body, abstraction_param, arg):
    # print("application_substitution", abstraction_body, "########",  abstraction_param, "################", arg)

    # print("")
    if type(abstraction_body) is Var:
        if abstraction_body == abstraction_param:
            # print("SUBSTITUTED", " - " , abstraction_body, " - " , arg)

            # print("")   
            return copy.deepcopy(arg) # TODO:: deepcopy
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
    
    elif type(abstraction_body) is If:
        abstraction_body.cond = application_substitution(abstraction_body.cond, abstraction_param, arg)
        abstraction_body.then = application_substitution(abstraction_body.then, abstraction_param, arg)
        abstraction_body._else = application_substitution(abstraction_body._else, abstraction_param, arg)
        return abstraction_body
    
    elif type(abstraction_body) == Succ:
        abstraction_body.value = application_substitution(abstraction_body.value, abstraction_param, arg)
        return abstraction_body

    elif type(abstraction_body) == Pred:
        abstraction_body.value = application_substitution(abstraction_body.value, abstraction_param, arg)
        return abstraction_body

    elif type(abstraction_body) == ZeroTest:
        abstraction_body.value = application_substitution(abstraction_body.value, abstraction_param, arg)
        return abstraction_body

    elif type(abstraction_body) == Zero:
        return abstraction_body
    
    else:
        return abstraction_body

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



if __name__ == "__main__":

    expressions = []

    # TESTING EXPRESSIONS

    expressions.append( App(Abs(Var("x"), IntType(), Var("x")), Integer(3)) )
    expressions.append( If(Boolean('true'), Integer(5), Integer(6) ) )
    expressions.append( If(Boolean('false'), Integer(5), Plus(Integer(5), Times(Integer(6), Integer(7) ) ) ) )
    expressions.append( If(Boolean('true'), Div(Integer(5), Integer(9)), Integer(6) ) )
    expressions.append( If(GT(Integer(3), Integer(5)), Integer(5), Integer(6) ) )
    expressions.append( If(GT(Integer(5), Integer(3)), Integer(5), Integer(6) ) )
    expressions.append( If(GE(Integer(4), Integer(4)), Integer(5), Integer(6) ) )

    # TESTING RECORDS
    
    rd3 = dict()
    rd3["a"] = String("Hey")
    rd3["b"] = String("Hoi")
    expressions.append(Record(rd3))


    record_dict = dict()
    record_dict["hey"] = Abs(Var("x"), IntType(), Var("x"))
    record_dict["lel"] = App(Abs(Var("x"), IntType(), Var("x")), Integer(2))
    record_dict["test"] = Integer(5)
    record = Record(record_dict)
    record_type = typecheck_exp(record, dict(""))
    expressions.append( Proj( App(Abs( Var("x"), record_type, Var("x")), Record(record_dict)), "lel") )
    
    # TESTING VARIANTS

    rd1 = dict()
    rd1["a"] = Var("z") # Const("KOK", SType("string"))
    rd1["b"] = Integer(2)
    r1 = Record(rd1)
    # r1type = typecheck_exp(r1, dict())
    rd2 = dict()
    rd2["c"] = String("TEST")
    rd2["d"] = Integer(4)
    r2 = Record(rd2)
    r2type = typecheck_exp(r2, dict())

    rd3 = dict()
    rd3["a"] = String("appel") # Const("KOK", SType("string"))
    rd3["b"] = Integer(2)
    r3 = Record(rd3)
    r3type = typecheck_exp(r3, dict())


    td = dict()
    td["one"] = r3type#r1type
    td["two"] = r2type

    vtype = VType(td)
    print("VTYPE")
    print(vtype)
    a = Tag("one", Var("x"), vtype)
    mapping = set()
    mapping.add(Map("one", Var("l"), Proj(Var("l"), "a")))
    mapping.add(Map("two", Var("k"), Proj(Var("k"), "c")))
    
    expressions.append( App(Abs( Var("z"), StringType(), App(Abs( Var("x"), vtype, Case(Var("x"), mapping)), Tag("one", Record(rd1), vtype))), String("appel")) )

    # case <varianttag = {'}> as VTYPE of ( <varianttag = record1> => record1.a | <varianttag2 = record2> => record2.b ) 
    expressions.append( Case(  Tag("one", Record({'a': Integer(1), 'b': Integer(2)}), VType( { "one": RType({'a': IntType, 'b': IntType}), "two": RType({'c': IntType, 'd': IntType}) } )) , set([Map('one', Var("l"), Proj(Var("l"), 'a')), Map('two', Var("k"), Proj(Var("k"), 'c'))]) ))

    for exp in expressions:
        print('')
        print(exp)
        typechecked = typecheck_expression(exp, dict())
        print('typechecked:\n', typechecked)
        ev = evaluate_expression(exp)
        print("evaluated:\n", ev)


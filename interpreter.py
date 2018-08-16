import sys
from parser import MyParser
from check_and_eval import typecheck_expression, evaluate_expression
from term_defs import Seq


if __name__ == "__main__":
    parser = MyParser()
    print("Parser setup finished")
        #('case Tag("one", {"a"= 1, "b"= 2}), < "one": {"a": int, "b": int}, "two": {"c": int, "d":int} >  of <"one", {"a"= Integer(1), "b"= Integer(2)}> => {"a"= 1, "b"=2}["a"])) | Map("two", {'c': Integer(3), 'd': Integer(4)}, Proj(Record({'c': Integer(3), 'd': Integer(4)}), 'c'))]) ))'),
        # STILL ERROR PRESENT IN VARIANT:: not checked on variant type of element!!!!

        # subject :::        'object with type in varianttype'
        # tag :::             < label = subject > as variantType
        # variantType :::     < label1 : T1 , label2 : T2 >

    for line in open("program.ayylmao"):
        print("")
        print(line)
        result = parser.parse(line)
        print(result)
        _type = typecheck_expression(result, dict())
        print("")
        print("TYPECHECKED")
        print(_type)
        _eval = evaluate_expression(result)
        print("")
        print("EVALUATED")
        print(_eval)
        print("")
        

        #case <<"one" = {"a"= 1, "b"= 2} >> as <<"one": {"a": int, "b": int}, "two": {"c": int, "d":int} >>  of  <{ "one" = {"a"= Integer(1), "b"= Integer(2) } >> => {"a"= 1, "b"=2}["a"])) | Map("two", {'c': Integer(3), 'd': Integer(4)}, Proj(Record({'c': Integer(3), 'd': Integer(4)}), 'c'))]) ))'),
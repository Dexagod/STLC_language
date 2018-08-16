import sys
from parser import MyParser
from check_and_eval import typecheck_expression, evaluate_expression
from term_defs import Seq


if __name__ == "__main__":
    parser = MyParser()
    print("Parser setup finished")


    with open('program.ayylmao', 'r') as myfile:
        data=myfile.read()
        parsed_data = parser.parse(data)
        print(parsed_data)
        for expression in parsed_data:
            print("")
            _type = typecheck_expression(expression, dict())
            print("")
            print("TYPECHECKED")
            print(_type)
            _eval = evaluate_expression(expression)
            print("")
            print("EVALUATED")
            print(_eval)
            print("")


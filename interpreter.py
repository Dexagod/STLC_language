import sys
from parser import MyParser
from check_and_eval import typecheck_expression, evaluate_expression
from term_defs import Seq


if __name__ == "__main__":
    parser = MyParser()
    print("Parser setup finished")

    for arg in sys.argv[1:]:
        print("Interpreting file: ", str(arg))
        with open(arg, 'r') as myfile:
            data=myfile.read()
            print(data)
            parsed_data = parser.parse(data)
            print(parsed_data)
            for expression in parsed_data:
                print("")
                _type = typecheck_expression(expression, dict())
                print("Expression:")
                print(" ", expression)
                print("")
                print("Typecheck:")
                print(" ", _type)
                print("")
                _eval = evaluate_expression(expression)
                print("Evaluation:")
                print(" ", _eval)
                print("")


import sys
from parser import MyParser
from check_and_eval import typecheck_expression, evaluate_expression
from term_defs import Seq


if __name__ == "__main__":
    print("START")
    arguments = sys.argv
    print(arguments)
    with open(arguments[1], 'r') as myfile:
        context = dict()
        data=myfile.read()
        print(data)
        parser = MyParser()
        parsed = parser.parse(data)
        print(parsed)
        expressions = []
        if (type(parsed) == Seq):
            expressions = parsed.get_list()
        else:
            expressions = [parsed]

        for expr in expressions:

            print(expr)
        #     typechecked = typecheck_expression(expr, context)
        #     print(expr)
        #     evaluated = evaluate_expression(expr)
        #     print(evaluated)
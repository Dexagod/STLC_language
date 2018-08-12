import sys
from parser import MyParser
from check_and_eval import typecheck_expression, evaluate_expression
from term_defs import Seq


if __name__ == "__main__":
    parser = MyParser()
    print("Parser setup finished")
    problems = [
        ('\\x:int.x| 5'),
        ('\\x:int.x| (5)'),
        ('(\\y:(int->int).\\z:int. y z || \\x:int.x| 10) '),
        ('5 + 6'),
        ('5 - 6'),
        ('5 * 6'),
        ('5 / 6'),
        ('5 + (6 * 7)'),
        ('if true then 5 else 6'),
        ('if false then 5 else (5 + (6 * 7))'),
        ('if true then (5 / 9) else 6'),
        ('if 3 > 5 then 5 else 6'),
        ('if (5 < 3) then 5 else 6'),
        ('if 4 >= 4 then 5 else 6'),
        ('{"a"=1, "b"=2, "c"=3}')
    ]
    for problem in problems:
        print("")
        print(problem)
        result = parser.parse(problem)
        print(result)
        _type = typecheck_expression(result, dict())
        print(_type)
        _eval = evaluate_expression(result)
        print(_eval)
        print("")
        
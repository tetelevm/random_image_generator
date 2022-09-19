"""
Tests all operators that they result in [-1; 1] for any input values
from [-1.01; 1.01].
Third-arity operators do not pass this test, but they do not break
calculations.
"""

from itertools import combinations_with_replacement

from operators import *


test_range = [(p-101) / 100 for p in range(203)]

for OperatorClass in OperatorManager.operators_dimensional:
    # if OperatorClass.arity > 2:
    #     continue
    operator = OperatorClass()
    args = combinations_with_replacement(test_range, OperatorClass.arity)
    is_correct = all(
        isinstance(result, (int, float)) and (-1 <= result <= 1)
        for result in (operator.formula(*cols) for cols in args)
    )
    name = format(OperatorClass.__name__, "<15")
    print(f"({OperatorClass.arity}) {name} ... {is_correct}")

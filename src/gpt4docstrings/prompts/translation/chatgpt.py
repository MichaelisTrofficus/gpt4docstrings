PROMPT = '''
If I give you this docstring:

"""
Calculate the average of a list of numbers.

Parameters
----------
numbers : list
    A list of numeric values.

Returns
-------
float
    The average of the input numbers.

Raises
------
ZeroDivisionError
    If the input list is empty.
"""

The google style version of this docstring is:

"""
Calculate the average of a list of numbers.

Args:
    numbers (list): A list of numeric values.

Returns:
    float: The average of the input numbers.

Raises:
    ZeroDivisionError: If the input list is empty.
"""

If I give you this docstring:

"""
Calculate the average of a list of numbers.

@param numbers: A list of numeric values.
@type numbers: list

@return: The average of the input numbers.
@rtype: float

@raise ZeroDivisionError: If the input list is empty.
"""

The reStructuredText style version of this docstring is:

"""
Calculate the average of a list of numbers.

:param numbers: A list of numeric values.
:type numbers: list

:return: The average of the input numbers.
:rtype: float

:raise ZeroDivisionError: If the input list is empty.
"""

If I give you this docstring:

"""
{docstring}
"""

The {style} style version of this docstring is:
'''

FUNCTION_PROMPTS = {
    "google": '''
For this Python function:

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

The function docstring using Google style is:


"""
Calculate the average of a list of numbers.

Args:
    numbers (list): A list of numeric values.

Returns:
    float: The average of the input numbers.

Raises:
    ZeroDivisionError: If the input list is empty.
"""

For this Python function:

```python
{code}
```

The function docstring using Google style is:
''',
    "numpy": '''
For this Python function:

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

The function docstring using NumPy style is:

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

For this Python function:

```python
{code}
```

The function docstring using NumPy style is:
''',
    "reStructuredText": '''
For this Python function:

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

The function docstring using reStructuredText style is:

"""
Calculate the average of a list of numbers.

:param numbers: A list of numeric values.
:type numbers: list

:return: The average of the input numbers.
:rtype: float

:raise ZeroDivisionError: If the input list is empty.
"""

For this Python function:

```python
{code}
```

The function docstring using reStructuredText style is:
''',
    "epytext": '''
For this Python function:

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

The function docstring using Epytext style is:

"""
Calculate the average of a list of numbers.

@param numbers: A list of numeric values.
@type numbers: list

@return: The average of the input numbers.
@rtype: float

@raise ZeroDivisionError: If the input list is empty.
"""

For this Python function:

```python
{code}
```

The function docstring using Epytext style is:
''',
}

CLASS_PROMPTS = {
    "google": '''
For this Python class:

```python
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")
```

The class docstring using Google style is:

"""
A class representing a student.

Attributes:
    name (str): The student's name.
    student_id (int): The unique identifier for the student.
"""

For this Python class:

```python
{code}
```

The class docstring using Google style is:
''',
    "numpy": '''
For this Python class:

```python
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")
```

The class docstring using Numpy style is:

"""
A class representing a student.

Parameters
----------
name : str
    The student's name.
student_id : int
    The unique identifier for the student.
"""

For this Python class:

```python
{code}
```

The class docstring using Numpy style is:
''',
    "reStructuredText": '''
For this Python class:

```python
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")
```

The class docstring using reStructuredText style is:

"""
A class representing a student.

:param name: The student's name.
:type name: str
:param student_id: The unique identifier for the student.
:type student_id: int
"""

For this Python class:

```python
{code}
```

The class docstring using reStructuredText style is:
''',
    "epytext": '''
For this Python class:

```python
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")
```

The class docstring using Epytext style is:

"""
A class representing a student.

@param name: The student's name.
@type name: str
@param student_id: The unique identifier for the student.
@type student_id: int
"""

For this Python class:

```python
{code}
```

The class docstring using Epytext style is:
''',
}

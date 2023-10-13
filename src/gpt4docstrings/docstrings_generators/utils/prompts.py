FUNCTION_PROMPTS = {
    "google": '''
If I give you this Python function:

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count

The documented function using a Google docstring will be:

```
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        float: The average of the input numbers.

    Raises:
        ZeroDivisionError: If the input list is empty.
    """
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

If I give you this Python function:

{code}

The documented function using a Google docstring will be:
''',
    "numpy": '''
If I give you this Python function:

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count

The documented function using a NumPy docstring will be:

```
def calculate_average(numbers):
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
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

If I give you this Python function:

{code}

The documented function using a NumPy docstring will be:
''',
    "reStructuredText": '''
If I give you this Python function:

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count

The documented function using a reStructuredText docstring will be:

```
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.

    :param numbers: A list of numeric values.
    :type numbers: list

    :return: The average of the input numbers.
    :rtype: float

    :raise ZeroDivisionError: If the input list is empty.
    """
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

If I give you this Python function:

{code}

The documented function using a reStructuredText docstring will be:
''',
    "epytext": '''
If I give you this Python function:

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count

The documented function using a Epytext docstring will be:

```
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.

    @param numbers: A list of numeric values.
    @type numbers: list

    @return: The average of the input numbers.
    @rtype: float

    @raise ZeroDivisionError: If the input list is empty.
    """
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        raise ZeroDivisionError("Cannot calculate the average of an empty list.")
    return total / count
```

If I give you this Python function:

{code}

The documented function using a Epytext docstring will be:
''',
}

CLASS_PROMPTS = {
    "google": '''
If I give you this Python class:

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")

The documented class using Google docstrings will be:

```
class Student:
    """
    A class representing a student.

    Attributes:
        name (str): The student's name.
        student_id (int): The unique identifier for the student.
    """

    def __init__(self, name, student_id):
        """
        Initialize a new Student instance.

        Args:
            name (str): The student's name.
            student_id (int): The unique identifier for the student.
        """
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        """
        Simulate the student studying a subject.

        Args:
            subject (str): The subject the student is studying.
        """
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        """
        Have the student take an exam for a subject.

        Args:
            subject (str): The subject for which the student is taking an exam.
        """
        print(self.name + " is taking an exam in " + subject + ".")
```

If I give you this Python class:

{code}

The documented class using Google docstrings will be:
''',
    "numpy": '''
If I give you this Python class:

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")

The documented class using NumPy docstrings will be:

```
class Student:
    """
    A class representing a student.

    Parameters
    ----------
    name : str
        The student's name.
    student_id : int
        The unique identifier for the student.
    """

    def __init__(self, name, student_id):
        """
        Initialize a new Student instance.

        Parameters
        ----------
        name : str
            The student's name.
        student_id : int
            The unique identifier for the student.
        """
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        """
        Simulate the student studying a subject.

        Parameters
        ----------
        subject : str
            The subject the student is studying.
        """
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        """
        Have the student take an exam for a subject.

        Parameters
        ----------
        subject : str
            The subject for which the student is taking an exam.
        """
        print(self.name + " is taking an exam in " + subject + ".")
```

If I give you this Python class:

{code}

The documented class using NumPy docstrings will be:
''',
    "reStructuredText": '''
If I give you this Python class:

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")

The documented class using reStructuredText docstrings will be:

```
class Student:
    """
    A class representing a student.

    :param name: The student's name.
    :type name: str
    :param student_id: The unique identifier for the student.
    :type student_id: int
    """

    def __init__(self, name, student_id):
        """
        Initialize a new Student instance.

        :param name: The student's name.
        :type name: str
        :param student_id: The unique identifier for the student.
        :type student_id: int
        """
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        """
        Simulate the student studying a subject.

        :param subject: The subject the student is studying.
        :type subject: str
        """
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        """
        Have the student take an exam for a subject.

        :param subject: The subject for which the student is taking an exam.
        :type subject: str
        """
        print(self.name + " is taking an exam in " + subject + ".")
```

If I give you this Python class:

{code}

The documented class using reStructuredText docstrings will be:
''',
    "epytext": '''
If I give you this Python class:

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        print(self.name + " is taking an exam in " + subject + ".")

The documented class using Epytext docstrings will be:

```
class Student:
    """
    A class representing a student.

    @param name: The student's name.
    @type name: str
    @param student_id: The unique identifier for the student.
    @type student_id: int
    """

    def __init__(self, name, student_id):
        """
        Initialize a new Student instance.

        @param name: The student's name.
        @type name: str
        @param student_id: The unique identifier for the student.
        @type student_id: int
        """
        self.name = name
        self.student_id = student_id

    def study(self, subject):
        """
        Simulate the student studying a subject.

        @param subject: The subject the student is studying.
        @type subject: str
        """
        print(self.name + " is studying " + subject + ".")

    def take_exam(self, subject):
        """
        Have the student take an exam for a subject.

        @param subject: The subject for which the student is taking an exam.
        @type subject: str
        """
        print(self.name + " is taking an exam in " + subject + ".")
```

If I give you this Python class:

{code}

The documented class using Epytext docstrings will be:
''',
}

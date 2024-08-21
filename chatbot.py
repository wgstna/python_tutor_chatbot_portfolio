import re
import ast
from difflib import get_close_matches


class Chatbot:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        return {
            'help': """Welcome to the Python Tutor Chatbot! Here's how you can interact with me:

        1. Ask questions about Python concepts, e.g., "What is a list in Python?"

        2. Request code analysis by starting your message with "Analyze:" followed by your code snippet enclosed in triple backticks, like this:

        Analyze: ```python
        def example_function():
            print("Hello, World!")
        ```

        3. Ask for examples or explanations of specific Python features.

        4. If you're not sure what to ask, try "Tell me about Python data types" or "What are common Python mistakes?"

        Remember, I'm here to help you learn Python. Feel free to ask anything!""",

            'common python mistakes': """Here are some common Python mistakes and how to avoid them:

        1. Indentation errors: Python uses indentation to define code blocks. Inconsistent indentation can lead to IndentationError or unexpected behavior.

        2. Forgetting colons: Always remember to add a colon (:) at the end of statements that start a new block, like if, for, while, def, and class.

        3. Using = instead of == for comparison: Use == for equality comparison and = for assignment.

        4. Forgetting to close parentheses, brackets, or quotes: Always ensure that opened parentheses (), brackets [], and quotes '' or "" are properly closed.

        5. Mixing tabs and spaces for indentation: Stick to either tabs or spaces (preferably spaces) for indentation throughout your code.

        6. Off-by-one errors in loops: Be careful with loop ranges, especially when using indexing. Remember that range(5) gives 0, 1, 2, 3, 4.

        7. Modifying a list while iterating over it: This can lead to unexpected results. Use a slice or create a new list instead.

        8. Mutable default arguments: Avoid using mutable objects as default arguments in functions.

        9. Forgetting to import modules: Always import the necessary modules at the beginning of your script.

        10. Ignoring exception handling: Use try-except blocks to handle potential errors gracefully.

        Remember, practice and careful coding can help you avoid these common mistakes!""",
            'python data types': """Python has several built-in data types. Here are the main ones:

        1. Numeric Types:
           - int: Integer numbers (e.g., 5, -17, 1000)
           - float: Floating-point numbers (e.g., 3.14, -0.001, 2.0)
           - complex: Complex numbers (e.g., 1+2j)

        2. Sequence Types:
           - list: Ordered, mutable sequences (e.g., [1, 2, 3])
           - tuple: Ordered, immutable sequences (e.g., (1, 2, 3))
           - range: Immutable sequence of numbers

        3. Text Type:
           - str: Strings, immutable sequences of Unicode characters (e.g., "Hello, World!")

        4. Mapping Type:
           - dict: Key-value pairs (e.g., {"name": "John", "age": 30})

        5. Set Types:
           - set: Unordered collection of unique elements (e.g., {1, 2, 3})
           - frozenset: Immutable version of set

        6. Boolean Type:
           - bool: True or False

        7. Binary Types:
           - bytes: Immutable sequence of bytes
           - bytearray: Mutable sequence of bytes
           - memoryview: Memory view of bytes-like objects

        8. None Type:
           - NoneType: The None object, representing absence of value

        Key points about Python data types:
        - Python is dynamically typed, meaning you don't need to declare the type of a variable.
        - You can use the type() function to check the type of any object.
        - Many types have built-in methods and operations specific to them.
        - You can convert between types using functions like int(), float(), str(), list(), etc.

        Example usage:
        ```python
        # Numeric types
        x = 5  # int
        y = 3.14  # float

        # Sequence types
        my_list = [1, 2, 3]  # list
        my_tuple = (4, 5, 6)  # tuple

        # String
        name = "Alice"  # str

        # Dictionary
        person = {"name": "Bob", "age": 25}  # dict

        # Set
        unique_numbers = {1, 2, 3, 3, 4}  # set (note: duplicates are removed)

        # Boolean
        is_python_fun = True  # bool

        # Checking types
        print(type(x))  # <class 'int'>
        print(type(name))  # <class 'str'>
        ```

        Understanding these data types is crucial for effective Python programming!""",
            'variable': 'Variables are containers for storing data values. In Python, you don\'t need to declare a variable type, and you can change the value and type of a variable after it has been set.',
            'integer': 'An integer is a whole number, positive or negative, without decimals, of unlimited length. In Python, you can create an integer by assigning a whole number to a variable, e.g., x = 5.',
            'float': 'A float is a number with a decimal point. In Python, you can create a float by assigning a number with a decimal point to a variable, e.g., x = 5.0.',
            'string': 'A string is a sequence of characters. In Python, you can create a string by enclosing characters in quotes, either single or double quotes, e.g., x = "Hello" or x = \'World\'.',
            'list': 'A list is an ordered, changeable, and indexable collection that allows duplicate members. You can create a list using square brackets, e.g., my_list = [1, 2, 3].',
            'tuple': 'A tuple is an ordered and unchangeable collection. Tuples are written with round brackets, e.g., my_tuple = (1, 2, 3).',
            'dictionary': 'A dictionary is a collection of key-value pairs. It is unordered, changeable, and indexed. In Python, dictionaries are written with curly brackets, e.g., my_dict = {"name": "John", "age": 30}.',
            'function': 'A function is a block of code which only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result.',
            'if statement': 'An if statement is used for conditional execution. It allows you to execute a block of code only if a certain condition is true.',
            'for loop': 'A for loop is used for iterating over a sequence (like a list, tuple, dictionary, set, or string). It allows you to execute a set of statements for each item in a sequence.',
            'while loop': "A while loop executes a set of statements as long as a condition is true. It's used when you don't know beforehand how many times you need to execute a block of code.",
            'class': 'A class is a code template for creating objects. Objects have member variables and have behaviour associated with them. In Python, a class is created by the keyword class.',
            'module': 'A module is a file containing Python definitions and statements. The file name is the module name with the suffix .py added.',
            'exception': 'An exception is an event that occurs during the execution of a program that disrupts the normal flow of instructions. In Python, you can use try, except, and finally to handle exceptions.',
        }

    def get_response(self, user_message):
        preprocessed_message = user_message.lower()

        # Check for code analysis request
        if 'analyze' in preprocessed_message or 'check' in preprocessed_message:
            code = self.extract_code(user_message)
            if code:
                return self.analyze_code(code)

        # Check for direct matches in knowledge base
        for concept, explanation in self.knowledge_base.items():
            if concept in preprocessed_message:
                return explanation

        # If no direct match, look for close matches
        possible_concepts = get_close_matches(preprocessed_message, self.knowledge_base.keys(), n=1, cutoff=0.6)
        if possible_concepts:
            return f"Did you mean to ask about '{possible_concepts[0]}'? {self.knowledge_base[possible_concepts[0]]}"

        # If still no match, provide a general response
        return "I'm not sure about that. Can you please rephrase your question or ask about a specific Python concept?"

    def extract_code(self, message):
        code_match = re.search(r'```python(.*?)```', message, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return None

    def analyze_code(self, code):
        try:
            tree = ast.parse(code)
            analysis = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis.append(f"Found a function definition: '{node.name}'")
                    if len(node.body) == 0:
                        analysis.append(f"  Warning: The function '{node.name}' is empty.")
                elif isinstance(node, ast.For):
                    analysis.append("Found a for loop")
                    if len(node.body) == 0:
                        analysis.append("  Warning: This for loop is empty.")
                elif isinstance(node, ast.While):
                    analysis.append("Found a while loop")
                    if len(node.body) == 0:
                        analysis.append("  Warning: This while loop is empty.")
                elif isinstance(node, ast.If):
                    analysis.append("Found an if statement")
                    if len(node.body) == 0:
                        analysis.append("  Warning: This if statement is empty.")
                elif isinstance(node, ast.ClassDef):
                    analysis.append(f"Found a class definition: '{node.name}'")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis.append(f"Importing module: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    analysis.append(f"Importing from module: {node.module}")

            if analysis:
                return "Here's what I found in your code:\n" + "\n".join(analysis)
            else:
                return "I analyzed your code but didn't find any notable structures. It might be a simple script or expression."
        except SyntaxError as e:
            return f"There's a syntax error in your code: {str(e)}"
        except Exception as e:
            return f"An error occurred while analyzing your code: {str(e)}"


# Example usage (for testing purposes)
if __name__ == "__main__":
    chatbot = Chatbot()

    # Test concept explanation
    print(chatbot.get_response("What is a variable in Python?"))
    print(chatbot.get_response("How do I use a for loop?"))

    # Test code analysis
    code_snippet = """
def greet(name):
    print(f"Hello, {name}!")

for i in range(5):
    greet(f"Person {i}")

class MyClass:
    def __init__(self):
        pass

import math
from datetime import datetime
"""
    print(chatbot.get_response(f"Can you analyze this code? ```python{code_snippet}```"))
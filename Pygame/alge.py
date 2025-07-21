from operator import ge
import sympy as sp
from sympy import symbols, expand, factor, solve, simplify
import random

# Generate simple algebra questions
def generate_algebra_question():
    x = symbols('x')
    
    # Linear equations: ax + b = c
    a = random.randint(2, 10)
    b = random.randint(1, 20)
    c = random.randint(1, 30)
    equation = sp.Eq(a*x + b, c)
    solution = solve(equation, x)[0]
    
    return f"Solve for x: {a}x + {b} = {c}", solution

def generate_simple_math_question():
    # Choose two random integers
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    # Randomly choose an operation
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        question = f"{a} + {b} = ?"
        answer = a + b
    elif operation == '-':
        question = f"{a} - {b} = ?"
        answer = a - b
    elif operation == '*':
        question = f"{a} * {b} = ?"
        answer = a * b
    else:  # division, ensure no division by zero and integer result
        # Make sure b divides a for integer division
        a = a * b
        question = f"{a} / {b} = ?"
        answer = a // b
    return question, answer

# Quadratic equations
def generate_quadratic():
    x = symbols('x')
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    
    equation = a*x**2 + b*x + c
    question = f"Factor: {equation}"
    factored = factor(equation)
    
    return question, factored

# Expansion problems
def generate_expansion():
    x = symbols('x')
    a = random.randint(1, 5)
    b = random.randint(1, 10)
    c = random.randint(1, 5)
    d = random.randint(1, 10)
    
    expr = (a*x + b) * (c*x + d)
    expanded = expand(expr)
    
    return f"Expand: ({a}x + {b})({c}x + {d})", expanded


print("Algebra Questions:")
question, answer = generate_simple_math_question()
print(question)
print("Answer:", answer)
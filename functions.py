import latex2sympy2 as ls
import sympy as syp


def convert_latex_to_sympy(expression):
    try:
        symbolic = ls.latex2sympy(expression)
    except Exception as e:
        print(f"Error in the conversion to symbolic equation: {e}")
        return None, None
    return symbolic


# Example of what de function output is
print(convert_latex_to_sympy(r'\frac{x}{y}'))


def derivatives(expression, var):
    symb = convert_latex_to_sympy(expression)
    variable = syp.symbols(str(var))
    derivative = syp.diff(symb, variable)

    return derivative


# Example of partial derivative
print(derivatives(r'\frac{x}{y}', 'x'))
print(derivatives(r'\frac{x}{y}', 'y'))


def detect_var(expression):
    symb = convert_latex_to_sympy(expression)
    variables = symb.free_symbols
    return list(variables)


print(detect_var(r'\frac{r}{r_{300}}'))


def inside_sqrt(expression):
    var = detect_var(expression)
    var_errors = [syp.symbols(f'\Delta{v}') for v in var]
    der = 0
    for i, j in zip(var, var_errors):
        der += (derivatives(expression, i))**2*j**2

    return der


print(inside_sqrt(r'\frac{r}{r_{300}}'))

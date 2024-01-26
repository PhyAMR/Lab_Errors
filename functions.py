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


print(detect_var(r'\frac{r}{yr_{300}}'))


def Error(expression, cons):
    const = syp.symbols(list(cons))
    variables = detect_var(expression)
    var_errors = [syp.symbols(f'\Delta{var}')
                  for var in variables if var not in const]
    der = 0
    var_no_con = [var for var in variables if var not in const]
    for i, j in zip(var_no_con, var_errors):
        der += (derivatives(expression, i))**2*j**2

    return syp.sqrt(der)


print(Error(r'\frac{r}{r_{300}}', [r"r_{300}"]))


def trans_expression(formula):

    before, after = formula.split('=', maxsplit=2)
    before = r'\Delta' + before + r'='
    return before, after


# print(trans_expression(r'\frac{r}{r_{300}}'))


def calculate_error(formula, const):
    if "=" in formula:
        before, expression = trans_expression(formula)
    else:
        expression = formula

    error = Error(expression, const)
    error_formula = before + str(error)
    error_formula = error_formula.replace('\Delta', '\Delta ')
    return error_formula, error


print(calculate_error(r'T=\frac{r}{r_{300}}', ["r_{300}"]))

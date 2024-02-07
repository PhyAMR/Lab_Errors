import latex2sympy2 as ls
import sympy as syp
import matplotlib.pyplot as plt

# expr = input(' Insert expression written in latex: ')
# const = input(' Insert constants written in latex: ')

expr1 = r'T=50.25+260.7\left(\frac{R}{R_{300}}\right)-11.0\left(\frac{R}{R_{300}}\right)^2'
expr2 = r'T=47.657+258.72\left(\frac{R}{R_{300}}\right)^{0.9}-2.7381\left(\frac{R}{R_{300}}\right)^{1.6}'


def convert_latex_to_sympy(expression):
    try:
        symbolic = ls.latex2sympy(expression)
    except Exception as e:
        # print(f"Error in the conversion to symbolic equation: {e}")
        return None, None
    return symbolic


# Example of what de function output is
# #print(convert_latex_to_sympy(expr))


def derivatives(expression, var):
    symb = convert_latex_to_sympy(expression)
    variable = syp.symbols(str(var))
    derivative = syp.diff(symb, variable)

    return derivative


# Example of partial derivative
# print(derivatives(r'47.657+258.72\left(\frac{R}{R_{300}}\right)^{0.9}-2.7381\left(\frac{R}{R_{300}}\right)^{1.6}', 'R'))
# #print(derivatives(expr, 'y'))


def detect_var(expression):
    symb = convert_latex_to_sympy(expression)
    variables = symb.free_symbols
    return list(variables)


# #print(detect_var(expr))


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


# #print(Error(expr, ["r_{300}"]))


def trans_expression(formula):

    before, after = formula.split('=', maxsplit=2)
    before = r'\Delta' + before + r'='
    return before, after


# #print(trans_expression(r'\frac{r}{r_{300}}'))


def calculate_error(formula, const):
    if "=" in formula:
        before, expression = trans_expression(formula)
    else:
        before = ' '
        expression = formula

    error = syp.simplify(Error(expression, const))
    error_formula = before + str(syp.latex(error))
    error_show = str(error_formula.replace('\Delta', '\Delta '))

    return error_show


# print(calculate_error(expr1, ["R_{300}"]))
# print(calculate_error(expr2, ["R_{300}"]))


def render_formula(expr):
    fig = plt.figure()
    plt.axis("off")
    plt.text(0.5, 0.5, f"${expr}$", size=50, ha="center", va="center")
    return fig


def render_var(expr):
    fig = plt.figure()
    plt.axis("off")
    if "\\" in expr:
        expr = "\\"+expr
    plt.text(0.2, 0.2, f"${expr}$",
             size=5, ha="center", va="center")
    return fig

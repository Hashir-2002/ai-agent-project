def calculator(expression: str):
    try:
        return eval(expression)
    except:
        return "Invalid Expression"


print(calculator("10*2+3-4"))
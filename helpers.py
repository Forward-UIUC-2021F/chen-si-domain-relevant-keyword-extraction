def string_to_float(string):
    index = string.find('e')
    if index == -1:
        return float(string)
    else:
        number = string[:index]
        exp = int(string[index + 1:])
        return float(number) * 10 ** exp
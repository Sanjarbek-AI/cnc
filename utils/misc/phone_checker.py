import re


async def is_valid(number):
    if len(number) == 13:
        pattern = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")
        return pattern.match(number)
    else:
        return False
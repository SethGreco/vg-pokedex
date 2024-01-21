
"""
TODO: small unit test? error handling?
"""


def inches_to_feet(height_in_inches: str):

    feet = int(height_in_inches) // 12
    remainder = int(height_in_inches) % 12

    height_as_string = str(feet) + "\'" + str(remainder) + '\"'
    return height_as_string

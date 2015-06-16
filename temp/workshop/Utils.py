import re
import sys

EPS = sys.float_info.epsilon
GRAVITATION = 9.81

def bool_to_int(boolean):
    if(boolean):
        return 1
    else:
        return 0
    
def parse(string):
    """
    regular expression which parses the floats or the integers in an input string
    and return them as a list
    """
    return re.findall(r'\d+(?:\.\d+)?', string)

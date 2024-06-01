from flask import flash

def validate_password(password):
    '''Validates the password user wrote.'''
    if (len(password) < 8):
        return False
    
    has_upper = False 
    has_symbol = False
    has_digit = False
    
    symbols = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    
    for character in password:
        if character.isupper():
            has_upper = True
            
        if character in "0123456789":
            has_digit = True
            
        if character in symbols :
            has_symbol = True
        
        if has_upper and has_symbol and has_digit:
            break

    return has_upper and \
        has_digit and has_symbol 


def validate_form(functionargs):
    '''Used to check that only a single value was written in the form.'''
    argscounter = 0
    for arg in functionargs:
        if argscounter > 1:
            return
        if arg:
            result = [arg, functionargs[arg]]
            argscounter += 1
    return result
        
            


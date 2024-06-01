def validate_password(password):
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
        
    return has_upper and \
        has_digit and has_symbol 

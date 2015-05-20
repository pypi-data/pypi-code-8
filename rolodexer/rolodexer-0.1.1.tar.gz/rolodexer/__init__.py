from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from parser import (
    tokenize, classify,
    
    RolodexerError,
    RDAmbiguousTerms,
    RDAmbiguousNames,
    RDAmbiguousNumber,
    RDPhoneNumberError,
    RDZipCodeError,
    
    ZipcodeField,
    ColorField,
    PhoneNumberField
)
from pyvalidator import Validator, And, Using, Optional

validator = Validator([{
    'name': And(str, len),
    'age': And(Using(int), lambda n: 18 <= n <= 99),
    Optional('sex'): And(str, Using(str.lower), lambda s: s in
                         ('male', 'female'))
}])

data = [{'name': 'Sue',
         'age': '28',
         'sex': 'FEMALE'}, {'name': 'Sam',
                            'age': '42'},
        {'name': 'Sacha',
         'age': '20',
         'sex': 'Male'}]

validated = validator.validate(data)

assert validated == [{'name': 'Sue',
                      'age': 28,
                      'sex': 'female'}, {'name': 'Sam',
                                         'age': 42},
                     {'name': 'Sacha',
                      'age': 20,
                      'sex': 'male'}]

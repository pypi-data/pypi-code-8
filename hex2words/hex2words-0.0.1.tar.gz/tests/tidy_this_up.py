# coding: utf-8

# FIXME this file has to be tided up and tested

def process_XXXsum_output_line_test1():
    input = '4ae9441337aba65ec89304f5afd87fbd  foobar.txt'
    expected_output = ('0x4ae9441337aba65ec89304f5afd87fbd', 'foobar.txt')
    real_output = process_XXXsum_output_line(input)
    real_output = (hex(real_output[0]), real_output[1])
    assert real_output == expected_output

def process_GPG_output_line_test1():
    input = '   Key fingerprint = 6282 432A 74BE 3561 7FC3  B935 AED0 F18B F604 2B33'
    expected_output = '0x6282432a74be35617fc3b935aed0f18bf6042b33'
    real_output = process_GPG_output_line(input)
    real_output = hex(real_output)
    assert real_output == expected_output
    
def process_GPG_output_line_test2():
    input = 'Wr0Ng F0rm4t'
    expected_output = None
    real_output = process_GPG_output_line(input)
    assert real_output == expected_output

def process_output_test1():
    input = (
        '4ae9441337aba65ec89304f5afd87fbd  foobar.txt\n',
        'd63f5b0ef39b05144a0716053d9a7f32  file45.pdf\n',
    )
    expected_output = '''foobar.txt: abc def ghi
file45.pdf: abc def ghi
'''
    real_output = process_output(input)
    print(real_output)
    assert expected_output == real_output


def hex2words_test1():
    input = '00'
    expected_output = 'aardvark'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    assert expected_output == real_output

def hex2words_test2():
    input = '0000'
    expected_output = 'aardvark adroitness'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    assert expected_output == real_output
    
def hex2words_test3():
    input = '000000'
    expected_output = 'aardvark adroitness aardvark'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    assert expected_output == real_output

def hex2words_test4():
    input = 'E582'
    expected_output = 'topmost Istanbul'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    assert expected_output == real_output
    
def hex2words_test5():
    input = '82E5'
    expected_output = 'miser travesty'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    assert expected_output == real_output

def hex2words_test6():
    input = 'E58294F2E9A227486E8B061B31CC528FD7FA3F19'
    expected_output = 'topmost Istanbul Pluto vagabond '\
        'treadmill Pacific brackish dictator '\
        'goldfish Medusa afflict bravado '\
        'chatter revolver Dupont midsummer '\
        'stopwatch whimsical cowbell bottomless'
    real_output = hex2words(input)
    print('"%s"' % real_output)
    print('"%s"' % expected_output)
    assert expected_output == real_output


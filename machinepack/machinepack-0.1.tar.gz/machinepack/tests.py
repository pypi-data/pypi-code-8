from machinepack.helpers import render


def execute_machinetest(func, test):
    mocks = test.get('mocks', None)
    test_result = func(test['inputs'], mocks)

    expected_result = test['exit']

    if test_result.name in expected_result.name:
        if set(test_result.args.keys()) == set(expected_result.args.keys()):
            return True
        else:
            return render('wrong_arguments', {
                'test_result': ", ".join(test_result.args.keys()),
                'expected_result': ", ".join(expected_result.args.keys())
            })
    else:
        return render('wrong_response', {
            'test_result': test_result.name,
            'expected_result': expected_result.name
        })

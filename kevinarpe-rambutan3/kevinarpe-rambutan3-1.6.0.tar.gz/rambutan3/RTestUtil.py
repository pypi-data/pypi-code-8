

def test_eq_and_ne(left, right, *, is_equal: bool):
    assert is_equal == (left == right)
    assert is_equal != (left != right)


# Later: test_le(), test_eq_and_le()

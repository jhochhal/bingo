# Ignoring some linting rules in tests
# pylint: disable=redefined-outer-name
# pylint: disable=missing-docstring
import pytest

from bingo.Util.ArgumentValidation import argument_validation


@pytest.mark.parametrize("func_arg,check", [
    (-0.1, {">=": 0}),
    (-0.1, {">": 0}),
    (0, {">": 0.0}),
    (0.1, {"<=": 0}),
    (0.1, {"<": 0}),
    (0, {"<": 0}),
    ("A", {"in": [1, 2]}),
    ("A", {"in": "BCDE"}),
    ("A", {"in": ["ABCDE", "BCD"]})
])
@pytest.mark.parametrize("keyword", [True, False])
def test_raises_error_failed_check(func_arg, check, keyword):
    @argument_validation(a=check)
    def test(a):
        pass

    with pytest.raises(ValueError):
        if keyword:
            test(a=func_arg)
        else:
            test(func_arg)


@pytest.mark.parametrize("check_type", [">=", ">", "<=", "<"])
@pytest.mark.parametrize("keyword", [True, False])
def test_raises_error_wrong_type_for_check(check_type, keyword):
    @argument_validation(a={check_type: 0})
    def test(a):
        pass

    with pytest.raises(TypeError):
        if keyword:
            test(a="string")
        else:
            test("string")


@pytest.mark.parametrize("func_arg,check", [
    (0.1, {">=": 0}),
    (0.1, {">": 0}),
    (0, {">=": 0.0}),
    (-0.1, {"<=": 0}),
    (-0.1, {"<": 0}),
    (0, {"<=": 0}),
    ("A", {"in": [1, "A"]}),
    ("A", {"in": "ABCDE"}),
])
@pytest.mark.parametrize("keyword", [True, False])
def test_valid_checks(func_arg, check, keyword):
    @argument_validation(a=check)
    def test(a):
        pass

    if keyword:
        test(a=func_arg)
    else:
        test(func_arg)


@pytest.mark.parametrize("default,check", [
    (-0.1, {">=": 0}),
    ("A", {"in": [1, 2]}),
    ("A", {">": 1}),
])
def test_ignoring_defaults(default, check):
    @argument_validation(a=check)
    def test(a=default):
        pass
    test()


def test_raises_error_nonexisting_argument():
    @argument_validation(b={"<=": 0})
    def test(a):
        pass

    with pytest.raises(SyntaxError):
        test(-1)


def test_raises_error_nonexisting_check():
    @argument_validation(b={"==": 0})
    def test(a):
        pass

    with pytest.raises(SyntaxError):
        test(0)

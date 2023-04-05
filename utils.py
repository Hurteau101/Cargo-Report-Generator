def type_check(arg, arg_name: str, expected_type: type):
    """
    Check the type of argument
    :param arg: The argument.
    :param arg_name: The argument name.
    :param expected_type: The type expected.
    :raise KeyError: Raises an error, if the argument is not what is expected
    """
    """Check the type of argument. Raise an error, if the argument is not what is expected"""
    if type(arg) != expected_type:
        raise TypeError(f"Expected '{arg_name}' to be of type '{expected_type.__name__}' "
                        f"but got '{type(arg).__name__}' instead")

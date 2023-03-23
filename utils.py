def type_check(arg, arg_name: str, expected_type: type):
    """Check the type of argument. Raise an error, if the argument is not what is expected"""
    if not isinstance(arg, expected_type):
        raise TypeError(f"Expected '{arg_name}' to be of type '{expected_type.__name__}' "
                        f"but got '{type(arg).__name__}' instead")
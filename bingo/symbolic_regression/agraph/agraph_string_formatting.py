from .maps import STACK_PRINT_MAP, LATEX_PRINT_MAP, CONSOLE_PRINT_MAP


def get_formatted_string(style, command_array, constants):
    if style == "console":
        return _get_formatted_string_using(CONSOLE_PRINT_MAP, command_array,
                                           constants)
    elif style == "latex":
        return _get_formatted_string_using(LATEX_PRINT_MAP, command_array,
                                           constants)
    else:  # style == "stack"
        return _get_stack_string(command_array, constants)


def _get_formatted_string_using(format_dict, command_array, constants):
    str_list = []
    for stack_element in command_array:
        tmp_str = _get_formatted_element_string(stack_element, str_list,
                                                format_dict, constants)
        str_list.append(tmp_str)
    return str_list[-1]


def _get_formatted_element_string(stack_element, str_list,
                                  format_dict, constants):
    node, param1, param2 = stack_element
    if node == 0:
        tmp_str = "X_%d" % param1
    elif node == 1:
        if param1 == -1 or param1 >= len(constants):
            tmp_str = "?"
        else:
            tmp_str = str(constants[param1])
    else:
        tmp_str = format_dict[node].format(str_list[param1], str_list[param2])
    return tmp_str


def _get_stack_string(stack, constants):
    tmp_str = ""
    for i, stack_element in enumerate(stack):
        tmp_str += _get_stack_element_string(i, stack_element, constants)

    return tmp_str


def _get_stack_element_string(command_index, stack_element, constants):
    node, param1, param2 = stack_element
    tmp_str = "(%d) <= " % command_index
    if node == 0:
        tmp_str += "X_%d" % param1
    elif node == 1:
        if param1 == -1 or param1 >= len(constants):
            tmp_str += "C"
        else:
            tmp_str += "C_{} = {}".format(param1, constants[param1])
    else:
        tmp_str += STACK_PRINT_MAP[node].format(param1, param2)
    tmp_str += "\n"
    return tmp_str
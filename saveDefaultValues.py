import os
import ast

header = 'Default Values for ETG_Tkinter_Window'
# TODO: Either remove this instance or remove default_dict from ETG_TkinterWindow
#  so as not to have to update both when one changes. Preferably, remove this instance
text_template = ['Target Directory',
                 'CSV Filename',
                 'Doc Name',
                 'Picture Width',
                 'Picture Height',
                 'Page Margins',
                 'Tab Stops',
                 'Line Spacing',
                 'Test Default']


# separator = '='

def return_template():
    return text_template


def access_file(file_path):
    directory, filename = os.path.split(file_path)
    # print(directory, filename)
    separator = '='  # removed the global to allow other functions an argument of the same name

    if '.txt' in filename:
        print('proper filename')
    else:
        print('improper filename')
        return False

    # final_directory = os.path.join(directory_in, image_folder_name)
    # if not os.path.exists(final_directory):
    #     os.makedirs(final_directory)
    if directory != '' and not os.path.exists(directory):
        os.makedirs(directory)

    # doc_title = "defaultValues.txt"

    if os.path.exists(file_path):
        print(f'file exists: {filename}')
        try:
            open(file_path, "r")
        except IOError:
            print("Write access DENIED on %s" % filename)
            return False
        # pass
    else:
        print(f'file doesn\'t exist: {filename}')
        print(f'Creating {filename}...')
        with open(file_path, 'w') as f:
            # print('writeLines')
            f.write(header + '\n')
            f.write(f'{separator}\n'.join(text_template))
            f.write(separator)
            f.close()
        print(f'{filename} created')
    return True


def read_file_original(file_path,
                       seperator='='):  # This doesn't work if you put a parameter name in the text file that doesn't exist in the template

    if not access_file(file_path):
        return

    par_list = []
    print_i = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            text_index = 0  # first line is the header
            # print(row)
            while text_index < len(text_template) - 1 and row.find(text_template[text_index]) == -1:
                text_index += 1
            else:
                if row.find(text_template[text_index]) != -1:
                    # creating a list of two values (var, value),                 , row.find returns the starting index of the found word, that index plus the length of the word + seperator gives the index position of the value. The split removes \n from the value
                    par_list.append((text_template[text_index].split(seperator)[0], (
                    row[row.find(text_template[text_index]) + len(text_template[text_index]) + len(seperator):].split(
                        '\n')[0])))
                    # print(par_list[print_i])
                    print_i += 1
                    # print('-')
            # for word in text_template:
            #     # if row.find(word) != -1:
            #     #     # print('line number:', lines.index(row))
            #     #     split_row = row.split('=')
            #     #     splitsplitRow = split_row[-1].split('\n')
            #     #     print(split_row)
            #     #     print(splitsplitRow)
            #     #     par_list_order.append((word,lines.index(row)))
            #     print(row[row.find(word)+len(word):].split('\n')[0])

    return par_list


def read_file(file_path,
              assign_symbol='='):  # This doesn't work if you put a parameter name in the text file that doesn't exist in the template

    if not access_file(file_path):
        return

    par_list = []
    print_i = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            if row.find(assign_symbol) != -1:
                ParName, ParValue = row.split(assign_symbol)
                par_list.append((ParName, ParValue.split('\n')[0]))

            # text_index = 0 # first line is the header
            # # print(row)
            # while text_index < len(text_template)-1 and row.find(text_template[text_index]) == -1:
            #     text_index += 1
            # else:
            #     if row.find(text_template[text_index]) != -1:
            #         # creating a list of two values (var, value),                 , row.find returns the starting index of the found word, that index plus the length of the word + seperator gives the index position of the value. The split removes \n from the value
            #         par_list.append((text_template[text_index].split(assign_symbol)[0],(row[row.find(text_template[text_index])+len(text_template[text_index])+len(seperator):].split('\n')[0])))
            #         # print(par_list[print_i])
            #         print_i += 1

    return par_list


def write_file(file_path, parameters=[['', '']], assign_symbol='='):
    if not access_file(file_path):
        return
    line = []
    with open(file_path, 'w') as f:
        f.write(header + '\n')
        for par in parameters:
            line.append(par[0] + assign_symbol + par[1])
        f.write('\n'.join(line))
        f.close()


# https://www.programiz.com/python-programming/decorator
# https://stackoverflow.com/questions/21716940/is-there-a-way-to-track-the-number-of-times-a-function-is-called

def count_func_calls(func):
    def inner(*args, **kwargs):
        inner.iteration += 1
        print(f'{func.__name__} #{inner.iteration}')
        return func(*args, **kwargs)

    inner.iteration = 0
    return inner


@count_func_calls
def parse_par(in_str, first_bound='(', second_bound=')', separator=','):  #,iter=0):
    par_out = []
    first = in_str.find(first_bound)
    second = in_str[first:].find(
        second_bound) + first  # find the first instance of the second_bound after the first first_bound
    if first != -1 and second != -1:
        par_out.append(in_str[first + len(first_bound):second].split(separator))
        if second != len(in_str) - 1:
            # Recursion, call the function again on the remaining string
            # Once the end of the string is reached, return the found parameter
            par_out = par_out + (parse_par(in_str[second + len(second_bound):], first_bound=first_bound,
                                           second_bound=second_bound))  #, iter=iter))
    return par_out


def conc_par(par_list, first_bound='(', second_bound=')', separator=','):
    par = []
    for i in par_list:
        if '' not in i:
            par.append(first_bound + i[0] + separator + i[1] + second_bound)
    out_str = ','.join(par)
    return out_str


def getVarFromFile(filename):
    import imp
    # import importlib
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    # data = importlib.import_module('data', '', f)
    f.close()


def load_variables_from_textfile(file_path: str) -> dict:
    variables = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=')
                key = key.strip()
                value = value.strip()
                variables[key] = value
    return variables


def read_lines_of_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # print(lines)
    # file.close() # using "with" allows you to open the file and it'll automatically close after
    return (lines)


def is_key_in_lines(key, lines):
    for index, line in enumerate(lines):
        # print(f'{key} == {line.split("=")[0]} = {key == line.split("=")[0]}')
        if key == line.split("=")[0]:
            return index
    return None


# https://www.youtube.com/watch?v=cI7StKdm6tI
def write_variables_to_textfile(file_path, variables):
    # print(variables)
    if not access_file(file_path):
        return
    updated = False  # initialize updated flag
    lines = read_lines_of_file(file_path)
    for key in variables:
        result = is_key_in_lines(key, lines)
        if result is not None:
            lines[result] = key + '=' + variables[key] + '\n'
            updated = True  # flag signals the var was found and the line is updated
        if not updated:
            if lines[-1][-1:] != '\n':  # Is the last element of the last entry a newline (\n)?
                lines[-1] += '\n'  # If it isn't, then add one before adding a new entry
            lines.append(key + '=' + variables[key])  # add a new entry
        else:  # reset updated
            updated = False

    with open(file_path, 'w') as file:
        print(lines)
        file.writelines(lines)
        file.close()


def interpret_dictionary(in_str: str) -> dict:
    return ast.literal_eval(in_str)


if __name__ == "__main__":

    #-------------------------------------------------------------------------------------------------------------------
    # # access_file(r'C:\pythonProject\Employee_Tag_Generator\test_defaults\defaultValues.txt')
    # # access_file('defaultValues.txt')
    # in_par = [('Target Directory','nowhere'),
    #           ('Center Margin','89'),
    #           ('CSV Filename','Book2.csv'),
    #           ('Enter Doc Name','New Doc.doc'),
    #           ('Picture Width','8.5'),
    #           ('Fake Input','False'),
    #           ('Picture Height','11'),
    #           ('Left Margin','0.2'),
    #           ('Right Margin','4'),
    #           ('Line Spacing','1.0')
    #           ]
    #
    # write_file(r'C:\pythonProject\Employee_Tag_Generator\test_defaults\defaultValues.txt', in_par)
    #
    # parameters = read_file(r'C:\pythonProject\Employee_Tag_Generator\test_defaults\defaultValues.txt')
    # print(parameters)
    #
    # parameter = []
    # # for par in text_template:
    # #     parameter.append((par, ''))
    # # for i in range(len(in_par)):
    # #     parameter[i][1] = in_par[i][1]
    # # print(parameter)
    #
    # parameter.append((text_template[3], '342'))
    # print(parameter)
    #-------------------------------------------------------------------------------------------------------------------

    # par_list = read_file(r'C:\pythonProject\Employee_Tag_Generator\test_defaults\defaultValues.txt')
    # # print(par_list[-1][1])
    # # test_string = '(left,0.14),(center,4.25),(right,8.36),(left,10)'
    # test_string = par_list[-1][1]
    # out_str = parse_par(test_string, first_bound='<<', second_bound=')')
    # print(out_str)
    # print(test_string)
    # conc_par(out_str, first_bound='(', second_bound=')', separator=',')

    # file_path = r'C:\pythonProject\Employee_Tag_Generator\test_defaults\mydata.txt'
    #
    # loaded_variables = load_variables_from_textfile(file_path)
    # for key in loaded_variables:
    #     print(key, "->", loaded_variables[key])
    #
    # updated_variables = {'Doc Name': 'Operator Tags Updated',
    #                      'Line Spacing': '1.5',
    #                      'New Variable': 'This is New'}

    # write_variables_to_textfile(file_path, updated_variables)
    #
    # par_to_conc = [('left', '0.14'), ('center', '4.25'), ('right', '8.36'), ('left', '10'), ('', ''), ('', '')]
    # print(conc_par(par_to_conc))

    lines = read_lines_of_file(r'C:\pythonProject\Employee_Tag_Generator\default_value.txt')
    for line in lines:
        print(line)

    # #https://www.programiz.com/python-programming/decorator
    # def make_pretty(func):
    #     # define the inner function
    #     def inner():
    #         # add some additional behavior to decorated function
    #         print("I got decorated")
    #         # call original function
    #         func()
    #     # return the inner function
    #     return inner
    #
    # # define ordinary function
    # def ordinary():
    #     print("I am ordinary")
    #
    # # decorate the ordinary function
    # decorated_func = make_pretty(ordinary)
    #
    # # call the decorated function
    # decorated_func()

    myDict = interpret_dictionary("{'top': 0.5, 'bottom': 0.4, 'left': 0.0, 'right': 0.0}")
    for key, value in myDict.items():
        print(f'dictionary[{key}] = {value}')

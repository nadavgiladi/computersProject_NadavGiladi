# this program takes as input data points, and will give as output the
# minimal chi^2, and plot a linear graph according to the results.

# THE MAIN FUNCTION.


# function receives a file with the data.
def fit_linear(filename):
    raw_data = open(filename, 'r')
    data = raw_data.readlines()
    # Strip lines and then delete empty ones if there are any.
    for line_index in range(len(data)):
        data[line_index] = data[line_index].strip()
    data.remove('')
    sort_method = check_sort_method(data[0])  # Check how data is sorted
    if sort_method == 'row_sorted':  # Data is row sorted
        data = split_check_row_sorted(data)  # Split & lowercase data
        data_and_titles_tuple = row_sorted_data_to_dict(data)
        data_dict = data_and_titles_tuple[0]  # data as dictionary
        titles_dict = data_and_titles_tuple[1]  # titles as dictionary
    if sort_method == 'column_sorted':  # Data is row sorted
        data[0] = data[0].lower()  # Split & lowercase data
        for line_index, line in enumerate(data):
            data[line_index] = data[line_index].split()
        data_and_titles_tuple = column_sorted_data_to_dict(data)
        data_dict = data_and_titles_tuple[0]  # data as dictionary
        titles_dict = data_and_titles_tuple[1]  # titles as dictionary
    return weighted_averages(data_dict)

    # a = calc_a_for_min_chi_squared(data_dict)
    # b = calc_b_for_min_chi_squared(data_dict)


# THOSE ARE FUNCTIONS THAT ARE USED BY THE MAIN FUNCTION:

#  This function checks if data is sorted by lines or columns by checking how
#  is the first line looks like. return the answer.


def check_sort_method(first_line):
    sort_method = ''
    digits_str = '0123456789'
    for char in first_line:
        if char in digits_str:  # If char contains digit, file is row sorted.
            sort_method = 'row_sorted'
            break
        else:
            sort_method = 'column_sorted'
    return sort_method


# This function takes as input a row sorted data list and splits it such
# that each row is a list of numbers and the 1st item of the row is the title


def split_check_row_sorted(data):
    titles_list = ['x', 'dx', 'y', 'dy', 'axis']
    digits_str = '0123456789-'
    for line_index, line in enumerate(data):
        data[line_index] = data[line_index].lower()
        for char_index, char in enumerate(data[line_index]):
            if data[line_index][char_index] in titles_list and data[
                          line_index][char_index + 1] in digits_str:
                new_line = data[line_index][:char_index + 1] + ' ' + data[
                                              line_index][char_index + 1:]
                data[line_index] = new_line
    for line_index, line in enumerate(data):
        data[line_index] = line.split()
    return data


# This function takes a *row* sorted data and makes 2 dictionary such that:
# x, y, dx, dy are keys and the data as integers are the values in data_dict
# x axis, y axis are keys and the titles are the values in titles_dict
# The function also checks if the data is valid for a plot

def row_sorted_data_to_dict(data):
    data_dict = {}
    titles_dict = {}
    length = len(data[0])
    for row in data[:-2]:
        if len(row) != length:
            return 'Input file error: Data lists are not the same length.'
        for number_index, number in enumerate(row[1:]):
            if ((row[0] == 'dx') or (row[0] == 'dy')) and (number == '0' or
                                         number == '0.0' or '-' in number):
                return 'input file error: Not all uncertainties are positive.'
            row[number_index+1] = float(number)
        data_dict[row[0]] = row[1:]
    for row in data[-2:]:
        titles_dict[row[0] + ' ' + row[1]] = row[2] + row[3]
    return data_dict, titles_dict


# This function takes *column* sorted data and makes it 2 dictionary such that:
# x, y, dx, dy are the keys and the data is the values in data_dict
# x axis, y axis are keys and the titles are the values in titles_dict
# The function also checks if the data is valid for a plot

def column_sorted_data_to_dict(data):
    length = len(data[0])
    dx_index = data[0].index('dx')
    dy_index = data[0].index('dy')
    data_dict = {'x': [], 'dx': [], 'y': [], 'dy': []}
    titles_dict = {}
    for row in data[1:-2]:
        if len(row) != length:
            return 'Input file error: Data lists are not the same length.'
        else:
            for number_index, number in enumerate(row):
                if (number_index == dx_index or number_index == dy_index) \
                 and (number == '0' or number == '0.0' or '-' in number):
                    return 'input file error: Not all uncertainties are ' \
                                                              'positive.'
                row[number_index] = float(number)
                data_dict[data[0][number_index]].append(row[number_index])
    for row in data[-2:]:
        titles_dict[row[0] + ' ' + row[1]] = row[2] + row[3]
    return data_dict, titles_dict


# This function takes as input 'data_dict' and returns a parameter 'a' for
# the minimum chi^2
# def calc_a_for_min_chi_squared(data_dict):
#     xy_list = []
#     for point in data_dict['x'][]:
#         xy = data_dict['x'][point] *




# This function takes as input 'data_dict' and returns a parameter 'b' for
# the minimum chi^2
# def calc_b_for_min_chi_squared(data_dict):

# This function calculates the weighted average. The input is a list of
# variables taken from data_dict. For example: data_dict[x], data_dict[y]
# data_dict[x]*data_dict[x], data_dict[x]*data_dict[y] etc...
# then the output is the weighted average(var sign with a line above it) and
# it's uncertainty.


def weighted_averages(data_dict):
    x = data_dict['x']
    dx = data_dict['dx']
    y = data_dict['y']
    dy = data_dict['dy']
    sum_x = 0
    sum_y = 0
    sum_squared_x = 0
    sum_squared_y = 0
    sum_squared_dy = 0
    sum_x_times_y = 0
    for index in range(len(data_dict)):  # calc relevant sums for the average
        sum_x = sum_x + x[index] ** 2
        sum_y = sum_y + y[index] ** 2
        sum_squared_x = sum_squared_x + sum_squared_x[index] ** 2
        sum_squared_y = sum_squared_y + sum_squared_y[index] ** 2
        sum_squared_dy = sum_squared_dy + dy[index] ** 2
        sum_x_times_y = sum_x_times_y + sum_x_times_y[index] ** 2

    return





# things to try function#


print_try = fit_linear('input_for_row.txt')
print(print_try)

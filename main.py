#  Final Python Project.
#  Name: Nadav Giladi.
#  I.D: 204686240.
#  Course: Computers for physics. first year, first semester.
#
#  IMPORTANT TO READ, BEFORE READING THE CODE ITSELF:
#  I tried to write the code as comprehensive as I can. I followed the
#  'code styling' presentation that was given too. You may find some
#  code segments that their presence is not completely obvious. for example,
#  The output of almost every function is organized as a dictionary,
#  even when it may force me to write extra code lines in order to extract it
#  later (an example for an 'extraction' is in line 243). The reason for that
#  is to make the organization and order methods more understandable and
#  simple for anyone who reads the code. There is also an explanation above
#  every function for it's general purpose and inside those functions there
#  are short comments above every code segment that does a specific action.
#  I hope it helps understanding the way the code is written.


#  This program takes as input data points, and will give as output:
#  - The parameters a & b that brings the chi squared function to the minimum.
#  - Chi squared accordingly
#  - Chi squared reduced
#  - Linear graph that fits those values (Saved as a SVG file and shown).


# THE MAIN FUNCTION.


# Function receives a file with the data.
def fit_linear(filename):
    raw_data = open(filename, 'r')
    data = raw_data.readlines()

    # Strip lines and then delete empty ones if there are any.
    for line_index in range(len(data)):
        data[line_index] = data[line_index].strip()
    data.remove('')

    # Check how data is sorted
    sort_method = check_sort_method(data[0])

    # Data is row sorted
    if sort_method == 'row_sorted':
        data = split_check_row_sorted(data)  # Split & lowercase data

        #  Organize the data into two dictionaries and check if input is valid.
        data_and_titles_tuple = row_sorted_data_to_dict(data)
        data_dict = data_and_titles_tuple[0]  # data as dictionary
        titles_dict = data_and_titles_tuple[1]  # titles as dictionary

    # Data is column sorted
    if sort_method == 'column_sorted':
        data[0] = data[0].lower()  # Split & lowercase data
        for line_index, line in enumerate(data):
            data[line_index] = data[line_index].split()

        #  Organize the data into two dictionaries and check if input is valid.
        data_and_titles_tuple = column_sorted_data_to_dict(data)
        data_dict = data_and_titles_tuple[0]  # arrange data as dictionary
        titles_dict = data_and_titles_tuple[1]  # arrange titles as dictionary

    #  Check if there is an input error. If there is, return an error message
    #  and abort the function.
    if type(data_and_titles_tuple) == str:
        return print(data_and_titles_tuple)

    #  Calculate the weighted averages and then calculate a and b
    weit_avgs_dict = weighted_averages(data_dict)
    number_of_points = len(data_dict['x'])
    a_dict = calc_a_for_min_chi_squared(weit_avgs_dict, number_of_points)
    b_dict = calc_b_for_min_chi_squared(weit_avgs_dict, number_of_points,
                                        a_dict)

    #  Calc chi squared & chi squared reduced, organize them in dictionaries.
    a = a_dict['a']
    b = b_dict['b']
    chi2_and_reduced_dict = calc_chi_squared_and_reduced(data_dict, a, b,
                                                         number_of_points)

    #  Extract the final values out of the relevant dictionaries. Then, print
    #  the values as instructed.
    da = a_dict['da']  # (a was extracted in line 40 already)
    db = b_dict['db']  # (b was extracted in line 41 already)
    chi2 = chi2_and_reduced_dict['chi2']
    chi2_reduced = chi2_and_reduced_dict['chi2_reduced']

    print('Evaluated fitting parameters:', '\n')
    print('a =', a, '+-', da, '\n')
    print('b =', b, '+-', db, '\n')
    print('chi2 =', chi2, '\n')
    print('chi2_reduced =', chi2_reduced, '\n')

    #  Plot the data into a linear graph and show it.
    plot_results_on_graph(data_dict, titles_dict, a_dict, b_dict)


# THE NEXT FUNCTIONS ARE THE ONES BEING USED BY THE MAIN FUNCTION.


#  This function checks if data is sorted by lines or columns by checking how
#  is the first line looks like. returns the answer as a string.
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


# This function takes a *row* sorted data and makes 2 dictionaries such that:
# x, y, dx, dy are keys and the data (as int) are the values in data_dict.
# x axis, y axis are keys and the titles are the values in titles_dict.
# The function also checks if the data is valid for a plot

def row_sorted_data_to_dict(data):
    data_dict = {}
    titles_dict = {}
    length = len(data[0])
    #  Build data_dict
    for row in data[:-2]:
        if len(row) != length:
            return 'Input file error: Data lists are not the same length.'
        for number_index, number in enumerate(row[1:]):
            if ((row[0] == 'dx') or (row[0] == 'dy')) and (number == '0' or
                                                           number == '0.0' or
                                                           '-' in number):
                return 'input file error: Not all uncertainties are positive.'
            row[number_index+1] = float(number)
        data_dict[row[0]] = row[1:]

    #  Build titles_dict
    for row in data[-2:]:
        titles_dict[row[0] + ' ' + row[1]] = row[2] + row[3]
    return data_dict, titles_dict


# This function takes *column* sorted data and makes 2 dictionaries such that:
# x, y, dx, dy are the keys and the data is the values in data_dict
# x axis, y axis are keys and the titles are the values in titles_dict
# The function also checks if the data is valid for a plot

def column_sorted_data_to_dict(data):
    length = len(data[0])
    dx_index = data[0].index('dx')
    dy_index = data[0].index('dy')
    data_dict = {'x': [], 'dx': [], 'y': [], 'dy': []}
    titles_dict = {}

    #  Build data_dict
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
    #  Build titles_dict
    for row in data[-2:]:
        titles_dict[row[0] + ' ' + row[1]] = row[2] + row[3]
    return data_dict, titles_dict


# This function calculates the weighted average. The input is data_dict.
# then the output are the weighted averages(it's formal sign is the variable
# with a line above it) and their uncertainties, in a dictionary.
# weit_avg_<x,y,dy, xy, etc..> is the variable's weighted average.

def weighted_averages(data_dict):
    # Extract variables from data_dict.
    x = data_dict['x']
    y = data_dict['y']
    dy = data_dict['dy']

    # calc sum(1/dy**2) which is the denominator of all the weighted sums
    inverse_sum_squared_dy = 0
    for index in range(len(data_dict['x'])):
        inverse_sum_squared_dy = inverse_sum_squared_dy + (1 / (dy[index]**2))

    # Setup the weit_avgs variables names
    weit_avg_x = 0
    weit_avg_y = 0
    weit_avg_xy = 0
    weit_avg_dy_squared = 0
    weit_avg_x_squared = 0

    # Calc the weit_avg's numerators
    for index in range(len(data_dict['x'])):
        weit_avg_x = weit_avg_x + (x[index] / (dy[index] ** 2))
        weit_avg_y = weit_avg_y + (y[index] / (dy[index] ** 2))
        weit_avg_xy = weit_avg_xy + ((y[index]*x[index]) / (dy[index] ** 2))
        weit_avg_x_squared = weit_avg_x_squared + (x[index] ** 2) / (dy[index]
                                                                     ** 2)
        weit_avg_dy_squared = weit_avg_dy_squared + 1

    # divide each weit_avg by the denominator which is sum(1/(dy**2))
    weit_avg_x = weit_avg_x / inverse_sum_squared_dy
    weit_avg_y = weit_avg_y / inverse_sum_squared_dy
    weit_avg_xy = weit_avg_xy / inverse_sum_squared_dy
    weit_avg_x_squared = weit_avg_x_squared / inverse_sum_squared_dy
    weit_avg_dy_squared = weit_avg_dy_squared / inverse_sum_squared_dy
    weit_avgs_dict = {'weit_avg_x': weit_avg_x, 'weit_avg_y': weit_avg_y,
                      'weit_avg_xy': weit_avg_xy, 'weit_avg_x_squared':
                      weit_avg_x_squared, 'weit_avg_dy_squared':
                      weit_avg_dy_squared}
    return weit_avgs_dict


# This function takes as input 'weit_avgs_dict' and returns a parameter 'a'
# and 'da' for the minimum chi^2

def calc_a_for_min_chi_squared(weit_avgs_dict, number_of_points):
    #  Extract from weit_avgs_dict the variables in order to make the
    #  equation of 'a' and 'da' shorter in the code line
    n = number_of_points
    weit_avg_x = weit_avgs_dict['weit_avg_x']
    weit_avg_y = weit_avgs_dict['weit_avg_y']
    weit_avg_xy = weit_avgs_dict['weit_avg_xy']
    weit_avg_x_squared = weit_avgs_dict['weit_avg_x_squared']
    weit_avg_dy_squared = weit_avgs_dict['weit_avg_dy_squared']

    #  Calculating 'a' and 'da'
    a = (weit_avg_xy - weit_avg_x * weit_avg_y) / (weit_avg_x_squared -
                                                   (weit_avg_x ** 2))
    da_squared = weit_avg_dy_squared / (n * (weit_avg_x_squared - (
                                             weit_avg_x ** 2)))
    da = da_squared ** 0.5
    a_dict = {'a': a, 'da': da}
    return a_dict


# This function takes as input 'data_dict' and returns a parameter 'b' for
# the minimum chi^2

def calc_b_for_min_chi_squared(weit_avgs_dict, number_of_points, a_dict):
    #  Extract from weit_avgs_dict the variables in order to make the
    #  equation of 'b' and 'db' shorter in the code line
    a = a_dict['a']
    n = number_of_points
    weit_avg_x = weit_avgs_dict['weit_avg_x']
    weit_avg_y = weit_avgs_dict['weit_avg_y']
    weit_avg_xy = weit_avgs_dict['weit_avg_xy']
    weit_avg_x_squared = weit_avgs_dict['weit_avg_x_squared']
    weit_avg_dy_squared = weit_avgs_dict['weit_avg_dy_squared']

    #  Calculating 'a' and 'da'
    b = weit_avg_y - (a * weit_avg_x)
    db_squared = (weit_avg_dy_squared * weit_avg_x_squared) / (n * (
        weit_avg_x_squared - (weit_avg_x ** 2)))
    db = db_squared ** 0.5
    b_dict = {'b': b, 'db': db}
    return b_dict


#  This function calculates and returns the chi squared and chi squared
#  reduced values.

def calc_chi_squared_and_reduced(data_dict, a, b, number_of_points):
    #  Extract the relevant variables for making the chi2 equation shorter
    x = data_dict['x']
    y = data_dict['y']
    dy = data_dict['dy']
    n= number_of_points

    #  Calc chi2 and chi2_reduced.
    chi2 = 0
    for index in range(number_of_points):
        chi2 = chi2 + ((y[index] - (a * x[index] + b)) / dy[index]) ** 2
    chi2_reduced = chi2 / (n - 2)

    #  Arrange both in a dictionary and return it.
    chi_and_red_dict = {'chi2': chi2, 'chi2_reduced': chi2_reduced}
    return chi_and_red_dict


#  This function plots the linear graph for the results. the input is
#  data_dict (The points) and titles_dict (The titles for the axes). The
#  output is a linear graph shown as a figure.

def plot_results_on_graph(data_dict, titles_dict, a_dict, b_dict):
    #  Extract the relevant values out of the dictionaries
    x = data_dict['x']
    dx = data_dict['dx']
    y = data_dict['y']
    dy = data_dict['dy']
    a = a_dict['a']
    b = b_dict['b']

    #  Make a new list called y_fitted which is a list that contains new y
    #  values for the plot such that every y is: y = a * x + b.
    y_fit = []
    for point in x:
        new_y = a * point + b
        y_fit.append(new_y)

    #  Extract & capitalize the titles for the plot.
    for key in titles_dict:
        titles_dict[key] = titles_dict[key].title()
        if 'y' in key:
            y_axis = titles_dict[key]
        elif 'x' in key:
            x_axis = titles_dict[key]

    #  Make the plot itself, add error bars and titles for the y axis & x axis.
    import matplotlib.pyplot as linear_graph  # Import 'PyPlot'
    linear_graph.errorbar(x, y_fit, yerr=dy, xerr=dx, color='r',
                          barsabove=True, ecolor='b')
    linear_graph.ylabel(y_axis)
    linear_graph.xlabel(x_axis)

    #  Save the figure as a SVG file with the name: 'linear_fit' and show it.
    linear_graph.savefig('linear_fit.svg', format='svg')
    linear_graph.show()

from fixed_seats_model import fixed_seats_model
from plot_results import plot_layout_result

############### Function documentation ##############
## fixed_seats_model(data_file, d0, d1 = 0, d2 = 0, d3 = 0, firstrow: bool = False, firstrow_y = 0.0,
#                    type=1, num_selection = 10, output_filename_affix='output')
# Create and solve IP model for selecting seats among a given set of fixed seats in a classroom.
## Parameters:
# data_file: str, coordinate file name of .csv or .xlsx file with 3 columns: Feature, X, Y.
# d0: float or int, social distance (inches) between seats. Required.
# d1: float or int, social distance (inches) between seats and instructor. Default is 0.
# d2: float or int, safety distance (inches) from doors. Default is 0.
# d3: float or int, safety distance (inches) from aisles. Default is 0.
# firstrow: bool, False means incorporting seats of the first row, True means eliminating seats of the first row. Default is False.
# firstrow_y: float or int, the y-coordinate of seats in the first row. Default is 0. Required if firstrow is True.
# type : int {1, 2, 3, 4}
#       if type=1: maximize number of selected seats under specified distance and prevention constraints.
#       if type=2: maximize total distance while selecting specified number of students.
#       if type=3: maximize minimum distance while selecting specified number of students.
#       if type=4: minimize number of pairs of adjacent seats (next to each other in the same row).
#       Default is 1.
# num_selection: int, the number of selected seats, required if type is 2, 3, or 4. Default is 10.
# output_filename_affix: str, adding to the end of input filename as output filename.
## Output: append coordinates of selected seats at the end of input data_file and create an output file.

## plot_layout_result(data_file, firstrow_y=0.0)
# Plot classroom layout with seat selection under possible preventions.
## Parameters:
# data_file: str, coordinate file name of .csv or .xlsx file with 3 columns: Feature, X, Y.
# firstrow_y: float, y-coordinate of firstrow. If 0, the first row is not treated as empty. Defaul is 0.
## Output: a pdf file of classroom layout plot.


############### Example run ######################

## change to your path to input file. This example excel file can be found in examples directory
file = "example_all_coordinates.xlsx"  # input file name, required parameter

## other parameters:
social_distance = 6 * 12  # inches, required parameter
door_distance = 216  # inches, optional parameter
aisle_distance = 81  # inches, optional parameter
firstrow = True  # leave first row empty, optional parameter
firstrowy = 2521.0003  # the common y-coordinate of seats in first row, optional parameter
output_filename_affix = '6ft_prevention'  # append this string at the end of input file name as output file name.

## this line will create an output file: example_all_coordinates_6ft_prevention.xlsx
fixed_seats_model(file, d0=social_distance, d2=door_distance, d3=aisle_distance, firstrow=firstrow, firstrow_y=firstrowy,
                  output_filename_affix=output_filename_affix)

## change to your path to output file. This example excel file can be found in examples directory
result_file = "example_all_coordinates_6ft_prevention.xlsx"  # file to be plotted

## this line will creat a pdf file of classroom layout plot
plot_layout_result(result_file, firstrow_y=firstrowy)
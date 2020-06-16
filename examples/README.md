# Discription of examples
In this "examples" directory, we provide a toy example to play with our "fixed_seat_model.py" and "plot_results.py".

The input file for coordinates is "example_all_coordinates.xlsx" in this directory, which is a modified layout of Clough 152 mentioned in 
the "insights" directory". For this example, we consider all preventions (instructor, doors, aisles) for the seating arrangement. Therefore, the input file includes:
* **(x,y) coordinates of all seats**
* **(x,y) coordinate of the instructor**: If you do not consider the movement of the instructor, this can be useful. In this example, we consider the movement of the instructor.
* **(x,y) coordinates of all doors**
* **(x,y) coordinates of all aisles**

Other inputs that need to be clarified in "fixed_seat_model.py" are:
* **d2**: 216(inches), the safety distance from doors.
* **d3**: 81(inches), the safety distance from aisles. This value makes sure seats exactly near the aisles will not be considered
* **firstrow_y**: 2521.0003, the y-coordinate of seats in the first row.

Anyone being interested in this example can download "example_all_coordinates.xlsx" here, "fixed_seat_model.py" and "plot_results.py"in "codes" directory. One can simply change the path of reading the input file in "fixed_seat_model.py", run the model and then get an excel file as the output, which should be exactly the same with "example_all_coordinates_6ft_prevention.xlsx" in this directory. Apart from all information contained in the input file, the output file also includes:
* **(x,y) coordinates of all selected seats**

Once getting "example_all_coordinates_6ft_prevention.xlsx" as the output, the user should change the path of reading "example_all_coordinates_6ft_prevention.xlsx" in "plot_results.py", run the model, and then get a pdf file, which plots the locations of the first row, the doors, the aisles, the selected seats and unselected seats. The pdf file should be "example_all_coordinates_6ft_prevention_plot.pdf".

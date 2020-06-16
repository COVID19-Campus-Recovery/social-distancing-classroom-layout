
# Documentation

In this folder, we provide documentation about how to use our tool. There are different types of classrooms we are considering. Below are the classroom types that have code available:

## Fixed seats model

Below are the steps to determine the optimal socially-distanced classroom layout if your classroom has fixed seats.

* **Step 1**: Generate a list of the (x,y)-coordinates 

  * See <i> Fixed Seats Model I/O</i> 
  * For instructions on how to generate the (x,y)-coordinates from a CAD file (see <i> Tutorial - Extracting coordinates from a CAD file using AutoCAD </i>)

* **Step 2**: Run <i> fixed_seat_model.py </i> in <i> code </i> to optimize selection of seats

  * Generate an output Excel file containing coordinates of selected seats together with original coordinates in the input file from **Step 1**
  * Some parameters including social distance threshold need to be specified (see <i> fixed_seat_model.py </i>)

* **Step 3**: Run <i> plot_results.py </i> in <i> code </i> to visualize selection of seats

  * Generate an output pdf file containing visualization of the classroom
  * All features in the input coordinate file will be plotted

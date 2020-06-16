
# Documentation

In this folder, we provide documentation about how to use our tool. There are different types of classrooms we are considering. Below are the classroom types that have code available:

## Fixed seats model

Below are the steps to determine the optimal socially-distanced classroom layout if your classroom has fixed seats.

* **Step 1**: Generate a list of the (x,y)-coordinates 

  * See <i> Fixed Seats Model I/O</i> 
  * For instructions on how to generate the (x,y)-coordinates from a CAD file (see <i> Tutorial - Extracting coordinates from a CAD file using AutoCAD </i>)

* **Step 2**: Run <i> main.py </i> in <i> code </i>

  **Step 2(a)**: Optimize selection of seats

  * Source <i> fixed_seats_model.py </i> in <i> code </i> to call function: <i> fixed_seats_model </i>
  * Generate an output Excel file by appending coordinates of selected seats to the end of input coordinate file from **Step 1**
  * Some parameters including social distance threshold need to be specified
  * Example usage and specification of parameters can be found in <i> main.py </i> in <i> code </i>

  **Step 2(b)**: Visualize selection of seats

  * Source <i> plot_results.py </i> in <i> code </i> to call function: <i> plot_layout_result </i>
  * Generate an output pdf file containing visualization of the classroom layout based on coordinate file generated in **Step 2(a)**
  * All features in the coordinate file will be plotted (use parameter <i>firstrow_y</i> to visualize prevention of leaving first row empty)
  * Example usage and specification of parameters can be found in <i> main.py </i> in <i> code </i>

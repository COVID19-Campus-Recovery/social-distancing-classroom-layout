import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_layout_result(data_file, firstrow_y=0.0):
    '''
    Plot classroom layout with seat selection under possible preventions.
    :param data_file: str, coordinate file name of .csv or .xlsx file with 3 columns: Feature, X, Y.
    :param firstrow_y: float, y-coordinate of firstrow.
    :return:
    '''
    ## read coordinates file.
    if '.xlsx' in data_file:
        coordinates = pd.read_excel(data_file)
        filename = data_file[:-5]
    elif '.csv' in data_file:
        coordinates = pd.read_csv(data_file)
        filename = data_file[:-4]
    seat_loc_all = np.array(coordinates.loc[coordinates['Feature'] == 'seat', ['X', 'Y']])
    seat_loc_selected = np.array(coordinates.loc[coordinates['Feature'] == 'selected_seat', ['X', 'Y']])
    aisle_loc = np.array(coordinates.loc[coordinates['Feature'] == 'aisle', ['X', 'Y']])
    door_loc = np.array(coordinates.loc[coordinates['Feature'] == 'door', ['X', 'Y']])
    instructor_loc = np.array(coordinates.loc[coordinates['Feature'] == 'instructor', ['X', 'Y']])
    if len(instructor_loc) == 1:
        instructor_loc = instructor_loc[0]

    ## create matplotlib figure.
    fig, axs = plt.subplots()
    axs.set_aspect('equal')
    fig.set_figheight(15)
    fig.set_figwidth(15)

    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        left=False,  # ticks along the left edge are off
        labelbottom=False,  # labels along the bottom edge are off
        labelleft=False)  # labels along the left edge are off

    legend_objects = []
    legend_labels = []

    ## plot instructor if input.
    if len(instructor_loc) > 0:
        axs.plot(instructor_loc[0], instructor_loc[1], "o", markersize=300, color='lightgrey')
        s2, = axs.plot(instructor_loc[0], instructor_loc[1], "s", markersize=15, color='red')
        legend_objects.append(s2)
        legend_labels.append('Instructor')

    ## plot doors if input.
    if len(door_loc) > 0:
        axs.plot(door_loc[:, 0], door_loc[:, 1], "o", markersize=380, color='lightgrey')
        s3, = axs.plot(door_loc[:, 0], door_loc[:, 1], "s", markersize=15, color='orange')
        legend_objects.append(s3)
        legend_labels.append('Doors')

    ## plot aisle if input.
    if len(aisle_loc) > 0:
        axs.plot(aisle_loc[:, 0], aisle_loc[:, 1], "o", markersize=120, color='lightgrey')
        s4, = axs.plot(aisle_loc[:, 0], aisle_loc[:, 1], "s", markersize=5, color='yellow')
        legend_objects.append(s4)
        legend_labels.append('Aisles')

    ## plot first row if input.
    if firstrow_y > 0:
        seat_firstrow = []
        for i in range(len(seat_loc_all)):
            if seat_loc_all[i, 1] == firstrow_y:
                seat_firstrow.append(seat_loc_all[i])
        seat_firstrow = np.array(seat_firstrow)
        s5, = axs.plot(seat_firstrow[:, 0], seat_firstrow[:, 1], "s", markersize=15, color='grey')
        legend_objects.append(s5)
        legend_labels.append('First row removed')

    ## plot seats and selected seats.
    s0, = axs.plot(seat_loc_all[:, 0], seat_loc_all[:, 1], "s", markersize=15, fillstyle='none', color='black')
    s1, = axs.plot(seat_loc_selected[:, 0], seat_loc_selected[:, 1], "s", markersize=15, fillstyle='full')
    legend_objects.append(s1)
    legend_labels.append('Selected seats')
    legend_objects.append(s0)
    legend_labels.append('Unselected seats')

    ## add legend.
    plt.legend(legend_objects, legend_labels, loc='lower center', ncol=len(legend_objects), bbox_to_anchor=(0.5, -0.1))

    ## save output file.
    plt.savefig(filename + "_plot.pdf", dpi=500)


if __name__ == "__main__":
    data_file = "/Users/sunyuming/Downloads/example_all_coordinates_6ft_prevention.xlsx" # change the path here on your own computers!!! delete locations of those preventions first if you do not want to plot them!
    plot_layout_result(data_file, 2521.0003)
    
    
    
    
    
    
    
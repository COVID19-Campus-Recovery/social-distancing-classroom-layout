from gurobipy import *
import numpy as np
import pandas as pd


def fixed_seats_model(data_file, d0, d1 = 0, d2 = 0, d3 = 0, firstrow: bool = False, firstrow_y = 0.0, type=1, num_selection = 10, output_filename_affix='output'):
    '''
    Create and solve IP model for selecting seats among a given set of fixed seats in a classroom.
    :param data_file: str, coordinate file name of .csv or .xlsx file with 3 columns: Feature, X, Y.
    :param d0: float or int, social distance (inches) between seats.
    :param d1: float or int, social distance (inches) between seats and instructor. Default is 0.
    :param d2: float or int, safety distance (inches) from doors. Default is 0.
    :param d3: float or int, safety distance (inches) from aisles. Default is 0.
    :param firstrow: bool, False means incorporting seats of the first row, True means eliminating seats of the first row. Default is False.
    :param firstrow_y: float or int, the y-coordinate of seats in the first row. Default is 0. Required if firstrow is True
    :param type: int {1, 2, 3, 4},
                 if type=1: maximize number of selected seats under specified distance and prevention constraints.
                 if type=2: maximize total distance while selecting specified number of students.
                 if type=3: maximize minimum distance while selecting specified number of students.
                 if type=4: minimize number of pairs of adjacent seats (next to each other in the same row).
                 Default is 1.
    :param num_selection: int, the number of selected seats, required if type is 2, 3, or 4. Default is 10.
    :param output_filename_affix: str, adding to the end of input filename as output filename.
    :return: optimal obective function value,
             array of coordinates of selected seats,
             array of index of seats being selected in the parameter seat_loc.
             If type = 1, return the minimum distance between selected seats as well.
    '''
    ## read coordinates file.
    if '.xlsx' in data_file:
        coordinates = pd.read_excel(data_file)
        filename = data_file[:-5]
    elif '.csv' in data_file:
        coordinates = pd.read_csv(data_file)
        filename = data_file[:-4]
    seat_loc = np.array(coordinates.loc[coordinates['Feature'] == 'seat', ['X', 'Y']])
    pre_selected = np.array(coordinates.loc[coordinates['Feature'] == 'selected_seat', ['X', 'Y']])
    aisles_loc = np.array(coordinates.loc[coordinates['Feature'] == 'aisle', ['X', 'Y']])
    doors_loc = np.array(coordinates.loc[coordinates['Feature'] == 'door', ['X', 'Y']])
    instructor_loc = np.array(coordinates.loc[coordinates['Feature'] == 'instructor', ['X', 'Y']])
    if len(instructor_loc) == 1:
        instructor_loc = instructor_loc[0]

    ## filering seats by preventions
    seat_set = [i for i in range(len(seat_loc))]  # contains all indexes of seats in seat_loc.
    # filtering seats by the instructor
    # We suggest if you consider the movement of instructor, then use 1)filtering by the first row; if considering instructor as a single point, then use 2)filtering by the instructor's location
    # 1)filtering by the first row.
    if firstrow == True:
        firstrow_seat_set = []
        for i in range(len(seat_loc)):
            if seat_loc[i][1] != firstrow_y:
                firstrow_seat_set.append(i)
        seat_set = list(set(seat_set).intersection(firstrow_seat_set))
    # 2)filtering by the instructor's location
    if d1 > 0:
        inst_seat_set = []
        for i in range(len(seat_loc)):
            x_inst = np.abs(seat_loc[i][0] - instructor_loc[0])
            y_inst = np.abs(seat_loc[i][1] - instructor_loc[1])
            if np.sqrt(x_inst*x_inst + y_inst*y_inst) >= d1:
                inst_seat_set.append(i)
        seat_set = list(set(seat_set).intersection(inst_seat_set))
    # filtering seats by doors
    if d2 > 0:
        doornum = len(doors_loc)
        door_seat_set = []
        for i in range(len(seat_loc)):
            dist_to_door = 0
            for j in range(doornum):
                x_door = np.abs(seat_loc[i][0] - doors_loc[j][0])
                y_door = np.abs(seat_loc[i][1] - doors_loc[j][1])
                if np.sqrt(x_door*x_door + y_door*y_door) >= d2:
                    dist_to_door += 1
            if dist_to_door >= doornum:
                door_seat_set.append(i)
        seat_set = list(set(seat_set).intersection(door_seat_set))
    # filtering seats by aisles
    if d3 > 0:
        aislenum = len(aisles_loc)
        aisle_seat_set = []
        for i in range(len(seat_loc)):
            dist_to_aisle = 0
            for j in range(aislenum):
                x_aisle = np.abs(seat_loc[i][0] - aisles_loc[j][0])
                y_aisle = np.abs(seat_loc[i][1] - aisles_loc[j][1])
                if np.sqrt(x_aisle*x_aisle + y_aisle*y_aisle) >= d3:
                    dist_to_aisle += 1
            if dist_to_aisle >= aislenum:
                aisle_seat_set.append(i)
        seat_set = list(set(seat_set).intersection(aisle_seat_set))
    # Now, we get indexes of all candidate seats after filtering by preventions
            
    pair_set = []  # define a set of seat index pair (s1, s2) for all s1 != s2.
    for s1 in range(len(seat_set) - 1):
        for s2 in range(s1 + 1, len(seat_set)):
            pair_set.append((seat_set[s1], seat_set[s2]))
    distance = {}  # compute distance between each pair of seats (s1, s2) for all s1 != s2.
    for pair in pair_set:
        x = np.abs(seat_loc[pair[0]][0] - seat_loc[pair[1]][0])
        y = np.abs(seat_loc[pair[0]][1] - seat_loc[pair[1]][1])
        distance[pair] = np.sqrt(x * x + y * y)
    d_max = np.max(list(distance.values()))  # get the largest distance between two different seats.

    neibor_set = []  # define a set of seat index neibor pair (s1, s2).
    for pair in pair_set:
        if distance[pair] <= 30:
            neibor_set.append(pair)

    model = Model('fixed_seat_layout')

    ## Set Gurobi parameters
    model.setParam('OutputFlag', False)
    ## objective 2, 3, 4 takes long time to run, so adjust some parameters.
    if type > 1:
        model.setParam('MIPGap', 0.05)
        model.setParam('MIPFocus', 3)

    ## Add variables
    # general variables for all types.
    x = model.addVars(seat_set, vtype=GRB.BINARY)
    # need for type 2, 3, 4.
    if type > 1:
        z = model.addVars(pair_set, vtype=GRB.BINARY)
        # build initial solution if input
        if len(pre_selected) > 0:
            for s in pre_selected:
                x[s].start = 1
            for i in range(len(pre_selected)-1):
                for j in range(i + 1, len(pre_selected)):
                    z[(pre_selected[i], pre_selected[j])].start = 1
    # need for type 3
    if type == 3:
        min_d = model.addVar(lb=0, vtype=GRB.CONTINUOUS)

    ## Add constraints
    if type > 1:
        # student number constraint: need for type 2, 3, 4
        model.addConstr(quicksum(x[s] for s in seat_set) == num_selection)

    ## social distancing limit constraint: need for all objectives.
    # need for type 1
    if type == 1:
        for pair in pair_set:
            if distance[pair] < d0:
                model.addConstr(x[pair[0]] + x[pair[1]] <= 1)
    # need for type 2, 3, 4
    else:
        for pair in pair_set:
            if distance[pair] < d0:
                model.addConstr(z[pair] == 0)
                model.addConstr(x[pair[0]] + x[pair[1]] <= 1)
            else:
                model.addConstr(z[pair] <= x[pair[1]])
                model.addConstr(z[pair] <= x[pair[0]])
                model.addConstr(z[pair] >= x[pair[0]] + x[pair[1]] - 1)

    # need for type 3.
    if type == 3:
        # model.addConstrs(z[pair] <= t[pair] for pair in pair_set)
        model.addConstrs(min_d - distance[pair] - d_max * (1 - z[pair]) <= 0 for pair in pair_set)

    ## Set objective function
    # type 1: maximize number of students
    if type == 1:
        model.setObjective(quicksum(x[s] for s in seat_set), GRB.MAXIMIZE)

    # type 2: maximize total distance
    if type == 2:
        model.setObjective(quicksum(distance[pair] * z[pair] for pair in pair_set) / num_selection, GRB.MAXIMIZE)

    # type 3: maximize min distance
    if type == 3:
        model.setObjective(min_d, GRB.MAXIMIZE)

    # type 4: minimize number of neibor pairs
    if type == 4:
        model.setObjective(quicksum(z[pair] for pair in neibor_set), GRB.MINIMIZE)

    ## Optimize the model
    model.optimize()

    ## Print and return the result
    status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}
    status = model.status
    print('The optimization status is {}'.format(status_code[status]))
    if status == 2:
        # Retrieve objective value
        print('Optimal objective value: {}'.format(model.objVal))
        # Retrieve variable value and record selected seats' index and coordinates.
        seat_loc_selected = []
        seat_selected = []
        for s in seat_set:
            if x[s].x > 0:
                seat_loc_selected.append(seat_loc[s])
                seat_selected.append(s)
                coordinates = coordinates.append(pd.DataFrame([['selected_seat', seat_loc[s][0], seat_loc[s][1]]],
                                                              columns=['Feature', 'X', 'Y']))
        # save the output file.
        coordinates.to_excel(filename + '_' + output_filename_affix + '.xlsx', index=False)

        if type == 1 : # for type 1, print and return the minimum distance between selected seats as well.
            selected_distance = []  # record distance between each pair of selected seats.
            for i in range(len(seat_selected) - 1):
                for j in range(i + 1, len(seat_selected)):
                    selected_distance.append(distance[seat_selected[i], seat_selected[j]])
            # print('smallest distance: {}'.format(np.min(selected_distance)))
            return model.objVal, np.array(seat_loc_selected), seat_selected, np.min(selected_distance)
        else:
            return model.objVal, np.array(seat_loc_selected), seat_selected


if __name__ == "__main__":
    data_file = "example_all_coordinates.xlsx" # change the path here on your own computers!!! the excel file can be found in examples directory
    
    ## All preventions: the first row; doors; aisles
    firstrow = True
    firstrowy = 2521.0003
    d2 = 216
    d3 = 81
    fixed_seats_model(data_file, d0=6 * 12, d2=d2, d3=d3, firstrow=firstrow, firstrow_y=firstrowy,
                      type=1, output_filename_affix='6ft_prevention')
    
    ## No prevention: if considering no prevention, please do not input locations of those features (the first row or instructor's location; doors; aisles)
    # fixed_seats_model(data_file, d0=6 * 12)





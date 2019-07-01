import numpy as np


def artillery_effects(attack_roll, coords_of_target, blast_radius):
    '''helper function to determine where an artillery
       shell lands on the battle grid and what squares
       are affected

        param attack_roll: roll to determine how close an artillery
                           shell lands to its intended target. The
                           scaling goes from attack_roll=20 being
                           dead on and attack_roll=0 being two blast
                           blast_radiuses away

        param coords_of_target: coordinates of the target on the 
                                battle space, given as a tuple of
                                (x,y)

        param blast_radius: splash radius of the artillery, given in
                            increments of 5 ft.
    '''
    increments_of_dist =  (2 * blast_radius) / 20
    # Count all attack rolls over 20 as being equivalent to 20 (can't get
    # "better" than 20)
    if attack_roll > 20: attack_roll = 20

    # calculate the amount of grids "off target" the shell lands
    dist_off_target = int(((20 - attack_roll) * increments_of_dist) // 5)

    # Calculate the number of squares that are at the edge of the 
    # circle carved with a radius equivalent to dist_off_target
    num_of_radius_edge_squares = 8 # for dist_off_target = 1
    if dist_off_target > 1:
        # Logic: the num of squares will increase for each increment of
        #        distance by the same number of squares as the previous
        #        increment of distance minus the four edge squares in the
        #        grid, which will have three new squares next to them in
        #        the next increment
        for _ in range(dist_off_target):
            num_of_radius_edge_squares = (num_of_radius_edge_squares - 4) + \
                                    (4*3)

    # Create a grid with the edge squares and assign a normal distribution to
    # it
    shell_land_dist = np.random.normal(loc=0.0, 
                               scale=1.0,
                               size=(dist_off_target, dist_off_target))
    # Get rid of the center indices
    for x in np.nditer(shell_land_dist):
    indices


    area_of_circle = np.pi * (dist_off_target) ^ 2
    area_of_square = dist_off_target^2
    
    area_differential = area_of_square - area_of_square

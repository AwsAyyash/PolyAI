import numpy as np
from numpy import ndarray


def get_stdin_data() -> (int, list[list[int]]):
    first_line = str(input()).strip().split(sep=' ')

    # N = the dimension of the city in blocks (the city has NxN blocks).

    dimension = int(first_line[0])

    # M = the number of pizzerias in the city. =~ the number of below info lines
    num_of_pizzerias = int(first_line[1])

    # get each pizzeria location and max number of moves

    info_lines = []
    for i in range(num_of_pizzerias):
        # storing: x_coordinate, y_coordinate, R, In each line as a list
        line = [int(value) for value in str(input()).strip().split(sep=' ')]
        info_lines.append(line)

    return dimension, info_lines


# making sure, that the input data meets the question constraints

def check_input(dimension: int, x_location: int, y_location: int, max_num_of_moves: int):
    if (dimension < 1) or (dimension > 10000):
        raise Exception('Dimensions should be from 1 to 10000')

    # considering the blocks in non-zero indexing
    if ((x_location < 1) or (x_location > dimension)) or \
            ((y_location < 1) or (y_location > dimension)):
        raise Exception(f'Pizzeria location must be within {dimension} x {dimension}')

    if (max_num_of_moves < 1) or (max_num_of_moves > 5000):
        raise Exception('Pizzeria range can not be less than or equals zero or exceed 5000')


# Storing the data of the Pizzeria

class Block:
    def __init__(self, dimension: int, location: list[int], max_num_of_moves: int):
        check_input(dimension, location[0], location[1], max_num_of_moves)

        self.dimension = dimension  # N in the question
        self.location = location  # list (array) of [x,y] coordinates
        self.max_num_of_moves = max_num_of_moves  # R in the question


def check_block(block_obj: Block, sum_block_list, count: int) -> int:
    """Check all the blocks that are within the range 'R' of each pizzeria
        and increment the number of pizzerias for each block.
        Returns:
            int: The maximum count among the blocks so far
     """

    # this is just a marker for each location, that if at the current pizzeria I already visited it =1 or not =0
    visited_positions = np.zeros((block_obj.dimension, block_obj.dimension))

    x = block_obj.location[0] - 1  # zero indexing
    y = block_obj.location[1] - 1  # zero indexing

    for i in range(block_obj.max_num_of_moves + 1):
        # check and set the vertical and horizontal moves
        if (x + i) < block_obj.dimension and (not is_visited(x + i, y, visited_positions)):
            sum_block_list[x + i][y] += 1
            visited_positions[x + i][y] = 1
            count = max(sum_block_list[x + i][y], count)

        if (x - i) >= 0 and (not is_visited(x - i, y, visited_positions)):
            sum_block_list[x - i][y] += 1
            visited_positions[x - i][y] = 1
            count = max(sum_block_list[x - i][y], count)

        if (y + i) < block_obj.dimension and (not is_visited(x, y + i, visited_positions)):
            sum_block_list[x][y + i] += 1
            visited_positions[x][y + i] = 1
            count = max(sum_block_list[x][y + i], count)

        if (y - i) >= 0 and (not is_visited(x, y - i, visited_positions)):
            sum_block_list[x][y - i] += 1
            visited_positions[x][y - i] = 1
            count = max(sum_block_list[x][y - i], count)

    for i in range(1, block_obj.max_num_of_moves):
        # check and set the diagonals moves
        if (x + i < block_obj.dimension) and (y + i < block_obj.dimension) and (
                not is_visited(x + i, y + i, visited_positions)):
            sum_block_list[x + i][y + i] += 1
            visited_positions[x + i][y + i] = 1
            count = max(sum_block_list[x + i][y + i], count)

        if (x - i >= 0) and (y - i >= 0) and (
                not is_visited(x - i, y - i, visited_positions)):
            sum_block_list[x - i][y - i] += 1
            visited_positions[x - i][y - i] = 1
            count = max(sum_block_list[x - i][y - i], count)

        if (x + i < block_obj.dimension) and (y - i >= 0) and (
                not is_visited(x + i, y - i, visited_positions)):
            sum_block_list[x + i][y - i] += 1
            visited_positions[x + i][y - i] = 1
            count = max(sum_block_list[x + i][y - i], count)

        if (x - i >= 0) and (y + i < block_obj.dimension) and (
                not is_visited(x - i, y + i, visited_positions)):
            sum_block_list[x - i][y + i] += 1
            visited_positions[x - i][y + i] = 1
            count = max(sum_block_list[x - i][y + i], count)

    return count


def is_visited(x_index: int, y_index: int, visited_positions: ndarray):
    return visited_positions[x_index][y_index] == 1


if __name__ == '__main__':

    # load data
    N, pizzerias_info_lines = get_stdin_data()

    sum_range = np.zeros((N, N))
    count = 0
    max_count = 0

    # Time complexity: O(M * R)
    # N= dimension, number of blocks in Z-city, M = size (the number) of pizzerias in Z-city, R= max number of moves
    for pizzeria in pizzerias_info_lines:
        block = Block(N, pizzeria[0:2], pizzeria[2])  # pizzeria = [x, y, R]
        count = check_block(block_obj=block, sum_block_list=sum_range, count=count)
        max_count = max(max_count, count)

    print(int(max_count))

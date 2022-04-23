from pickle import NONE
from cell import Cell
import consts
import random

class Board:
    def __init__(self, cols, rows) -> None:
        self.snake_cells = []
        self.snake_cells_new = []
        self.empty_cells = []
        self.cells = []
        self.cols = cols
        self.rows = rows
        self.food = NONE
        
        for i in range(rows * cols):
            cell = Cell(i, consts.CELL_TYPE_EMPTY)
            self.cells.append(cell)
            self.empty_cells.append(cell)


    def set_head(self, x, y, value):
        cell = self.cells[y * self.cols + x]
        cell.set_head(value, consts.CELL_TYPE_SNAKE)
        self.snake_cells_new = []
        self.snake_cells_new.append(cell)
        if len(self.snake_cells) > 0:
            self.snake_cells[0].clear_head()
        self.empty_cells.remove(cell)


    def update(self):
        for cell in self.snake_cells:
            cell.update()
            status = cell.get_type()
            if (status[1] == 0):
                cell.set_type(consts.CELL_TYPE_EMPTY)
                self.empty_cells.append(cell)
            else:
                self.snake_cells_new.append(cell)
        self.snake_cells = self.snake_cells_new


    def get_free_cells(self):
        return self.empty_cells
    

    def get_snake_cells(self):
        return self.snake_cells


    def get_cell_status(self, x, y):
        return self.cells[y * self.cols + x].get_type()[0]


    def get_snake_cells_pos(self):
        loc_array = []
        for cell in self.snake_cells:
            row = cell.get_id() // self.cols
            col = cell.get_id() % self.cols 
            pos = (col,  row, cell.is_head())
            loc_array.append(pos)
        return loc_array

    def check_pos(self, x, y):
        if (x < 0) or (x >= self.cols) or (y < 0) or (y >= self.rows):
            return consts.RESULT_INVALID_POS
        state = self.cells[y * self.cols + x].get_type()
        print(f'state = {state} id = {y * self.cols + x}')
        if state[0] == consts.CELL_TYPE_SNAKE:
            return consts.RESULT_INVALID_POS
        if state[0] == consts.CELL_TYPE_FOOD:
            return consts.RESULT_FOOD
        return consts.RESULT_EMPTY


    def generate_food(self):
        while 1:    
            i = random.randint(0, len(self.empty_cells)-1)
            self.food = self.empty_cells[i]
            if self.food.get_type()[0] == consts.CELL_TYPE_FOOD:
                continue
            self.food.set_type(consts.CELL_TYPE_FOOD)
            print(f'selected cell id {self.food.get_id()}')
            return


    def get_food(self):
        row = self.food.get_id() // self.cols
        col = self.food.get_id() % self.cols 
        pos = (col,  row)
        return pos
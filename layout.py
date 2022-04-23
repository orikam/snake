class Layout:
    def __get_cell_rect_func(cell_width, cell_height):
        def ret_func(x, y, center):
            if center:
                return (x * cell_width + cell_width // 2 , y * cell_height + cell_height // 2, cell_width, cell_height)
            return (x * cell_width, y * cell_height, cell_width, cell_height)
        return ret_func

    def __get_scale_function(base_size):
        def ret_func(size):
            return base_size / size
        return ret_func

    def __init__(self, screen_size, num_cols, num_rows) -> None:
        self.screen_size = screen_size
        self.header_height = 100
        width, height = screen_size
        
        self.cell_width = width // num_cols
        self.cell_height = (height - self.header_height) // num_rows
        
        self.board_rect = (0 , height - self.header_height, width, height - self.header_height)
        self.get_cell_rect = Layout.__get_cell_rect_func(self.cell_width, self.cell_height)
        
        self.get_scale_factor = Layout.__get_scale_function(self.cell_width)
        self.num_of_cols = num_cols
        self.num_of_rows = num_rows
        self.header_rect = (0, 0, width, self.header_height)



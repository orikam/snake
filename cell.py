class Cell:
    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type
        self.head = False
        self.cnt  = 0


    def update(self):
        if self.cnt > 0:
            self.cnt -= 1 

    def get_id(self):
        return self.id


    def set_type(self, type):
        self.type = type


    def get_type(self):
        return (self.type, self.cnt)


    def set_head(self, value, type):
        self.head = True
        self.cnt = value
        self.type = type

    def clear_head(self):
        self.head = False


    def is_head(self):
        return self.head

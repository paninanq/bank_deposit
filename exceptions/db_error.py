class DatabaseError(Exception):
    def __init__(self):
        super().__init__("Error while working with the database")



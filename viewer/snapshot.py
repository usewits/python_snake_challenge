class Snapshot:

    def __init__(self, filename = None):
        self.bogusData()

    def bogusData(self):
        self.width = 5
        self.height = 5
        self.content = [['.', '.', '#', '.', '.'],
                        ['#', '.', '.', '.', '#'],
                        ['#', '.', '#', '.', '#'],
                        ['.', '.', '.', '.', '.'],
                        ['#', '#', '#', '#', '#']]
        self.food = [[1, 1], [3, 2]]

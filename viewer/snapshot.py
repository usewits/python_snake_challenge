class Snapshot:

    def __init__(self, filename = None):
        self.bogusData()

    def bogusData(self):
        self.width = 5
        self.height = 5
        self.content = [['.', '.', '#', '.', '.'],
                        ['#', 'x', '.', '.', '#'],
                        ['#', '.', '#', 'x', '#'],
                        ['.', '.', '.', '.', '.'],
                        ['#', '#', '#', '#', '#']]

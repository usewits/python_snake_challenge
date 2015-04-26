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
        self.names = ['Player 1', 'Player 2', 'Player 3']
        self.scores = [100, 50, 10]
        self.status = ['', '', 'dead']
        self.snakes = [[[1, 2], [1, 3], [2, 3], [3, 3]],
                       [[3, 1], [3, 0], [4, 0], [0, 0]],
                       []]

import random

class Level:
    def __init__(self, size, wall, floor):
        self.width = size[0]
        self.height = size[1]
        self.wall = wall
        self.floor = floor
        self.genBoard()

    def genBoard(self):
        self.board = self.genEmpty()
        self.rooms = self.genRooms()
        self.corridors = self.genCorridors()

    def genEmpty(self):
        return [[self.wall for x in range(self.width)] for y in range(self.height)]

    def genRooms(self):
        numRooms = (self.width * self.height) // random.randint(50, 100)
        rooms = []
        
        for i in range(numRooms):
            while True:
                x1 = random.randint(1, self.width - 2)
                y1 = random.randint(1, self.height - 2)

                x2 = x1 + random.randint(2, 5)
                y2 = y1 + random.randint(2, 5)

                if x2 in range(0, self.width - 1) and y2 in range(0, self.height - 1):
                    valid = True
                    for y in range(y1, y2 + 1):
                        for x in range( x1, x2 + 1):
                            if self.board[y][x] != self.wall:
                                valid = False
                    if valid:
                        break

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    self.board[y][x] = self.floor

            rooms.append([(x1, y1), (x2, y2)])

        return rooms

    def genCorridors(self):
        corridors = []
        
        for i in range(len(self.rooms)):
            if i == len(self.rooms) - 1:
                break
            
            r1 = self.rooms[i]          
            r2 = self.rooms[i + 1]
            
            r1c = (((r1[0][0] + r1[1][0]) // 2), ((r1[0][1] + r1[1][1]) // 2))
            r2c = (((r2[0][0] + r2[1][0]) // 2), ((r2[0][1] + r2[1][1]) // 2))

            x = r1c[0]
            for y in range(min(r1c[1], r2c[1]), max(r1c[1], r2c[1]) + 1):
                self.board[y][x] = self.floor

            y = r2c[1]
            for x in range(min(r1c[0], r2c[0]), max(r1c[0], r2c[0]) + 1):
                self.board[y][x] = self.floor

    def displayBoard(self):
        for y in self.board:
            for x in y:
                print(x, end="")
            print()

    def placeEntity(self, roomID, char):
        x = random.randint(self.rooms[roomID][0][0], self.rooms[roomID][1][0])
        y = random.randint(self.rooms[roomID][0][1], self.rooms[roomID][1][1])

        self.board[y][x] = char
        
def placeAllEntities(level):
    for i in range(len(level.rooms)):
        char = "z"
        if i == 0:
            char = "p"
        level.placeEntity(i, char)
    
if __name__ == "__main__":
    while True:
        level = Level((40, 30), "#", " ")
        placeAllEntities(level)
        level.displayBoard()
        input()
    
    

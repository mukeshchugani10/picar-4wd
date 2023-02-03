import copy


class Utils:

    def valid_index(self, x, y):
        if (x < 0 or y < 0 or x >= self.n or y >= self.n or (x, y) in self.visited or self.grid[x][y] == 1):
            return False

        return True

    def bfs(self, queue):

        while len(queue) != 0:
            x, y, d, path = queue.pop(0)
            if x == self.n - 1:
                return path

            if self.valid_index(x - 1, y) :
                new_path = copy.copy(path)
                self.visited[(x - 1, y)] = True
                ng = (x - 1, y, d + 1, new_path + [(x - 1 , y)])

                queue.append(ng)
            if self.valid_index(x + 1, y) :
                new_path = copy.copy(path)
                self.visited[(x + 1, y)] = True
                ng = (x + 1, y, d + 1, new_path + [( x + 1, y)])
                queue.append(ng)
            if self.valid_index(x, y - 1) :
                new_path = copy.copy(path)
                self.visited[(x, y - 1)] = True
                ng = (x, y - 1, d + 1, new_path + [( x, y - 1)])
                queue.append(ng)
            if self.valid_index(x, y + 1) :
                new_path = copy.copy(path)
                self.visited[(x, y + 1)] = True
                ng = (x, y + 1, d + 1, new_path + [( x, y + 1)])
                queue.append(ng)

        return -1

    def shortestPath(self, map, start) :
        self.n = len(map)
        self.grid = map
        self.visited = {}
        x = start[0]
        y = start[1]
        self.visited[(x, y)] = True
        queue = [(start)]

        return self.bfs(queue)
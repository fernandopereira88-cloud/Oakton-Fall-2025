import random
from collections import deque

class DisjointSet:
    def __init__(self, n):
        self.parent = [-1] * n
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] < 0:
            return u
        self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            elif self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

    def print_disjoint_set_tree(self):
        print("Disjoint Set Tree:")
        for i in range(len(self.parent)):
            print(f"Node {i}: Parent -> {self.parent[i]}")


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # For each cell, store walls: N, E, S, W as booleans (True = wall present)
        # Start with all walls present.
        self.walls = [
            [{"N": True, "E": True, "S": True, "W": True} for _ in range(cols)]
            for _ in range(rows)
        ]

    def index(self, r, c):
        """Map 2D coordinates to 1D index."""
        return r * self.cols + c

    def coordinates(self, idx):
        """Map 1D index back to 2D coordinates."""
        r = idx // self.cols
        c = idx % self.cols
        return r, c

    def neighbors(self, r, c):
        """Return valid neighbor cells as (nr, nc, direction) triplets."""
        dirs = []
        if r > 0:           # up
            dirs.append((r - 1, c, "N"))
        if c < self.cols - 1:  # right
            dirs.append((r, c + 1, "E"))
        if r < self.rows - 1:  # down
            dirs.append((r + 1, c, "S"))
        if c > 0:           # left
            dirs.append((r, c - 1, "W"))
        return dirs

    def generate_kruskal(self):
        """Generate the maze using Kruskal's algorithm and a DisjointSet."""
        n_cells = self.rows * self.cols
        ds = DisjointSet(n_cells)
        # ? initialize minimum spanning tree?
        
        # Build edge list: edges between neighboring cells (no duplicates).
        edges = []
        for r in range(self.rows):
            for c in range(self.cols):
                u = self.index(r, c)
                # Only add right and down neighbors to avoid duplicate edges
                if c + 1 < self.cols:
                    v = self.index(r, c + 1)
                    edges.append((u, v))
                if r + 1 < self.rows:
                    v = self.index(r + 1, c)
                    edges.append((u, v))

        # Randomize edges for random maze
        random.shuffle(edges)

        mst_edges = 0  # number of edges added to spanning tree
        # Kruskal: process edges until we have a spanning tree
        for (u, v) in edges:
            if mst_edges >= n_cells - 1:
                break
            if ds.find(u) != ds.find(v):
                ds.union(u, v)
                mst_edges += 1
                # Remove the wall between u and v in our maze representation
                r1, c1 = self.coordinates(u)
                r2, c2 = self.coordinates(v)
                self.remove_wall_between(r1, c1, r2, c2)

        # Make entrance and exit openings
        # Entrance: remove north wall of (0,0)
        self.walls[0][0]["N"] = False
        # Exit: remove south wall of (rows-1, cols-1)
        self.walls[self.rows - 1][self.cols - 1]["S"] = False

    def remove_wall_between(self, r1, c1, r2, c2):
        """Remove the shared wall between two neighboring cells."""
        if r1 == r2:
            # same row -> horizontal neighbor
            if c1 < c2:
                # c1 is left of c2
                self.walls[r1][c1]["E"] = False
                self.walls[r2][c2]["W"] = False
            else:
                self.walls[r1][c1]["W"] = False
                self.walls[r2][c2]["E"] = False
        elif c1 == c2:
            # same column -> vertical neighbor
            if r1 < r2:
                # r1 is above r2
                self.walls[r1][c1]["S"] = False
                self.walls[r2][c2]["N"] = False
            else:
                self.walls[r1][c1]["N"] = False
                self.walls[r2][c2]["S"] = False

    def to_ascii(self, path=None):
        """
        Convert maze to ASCII art.
        `path` is optional set of (r, c) coordinates for solution highlighting.
        """
        if path is None:
            path = set()
        lines = []

        # Top border (special-cased entrance)
        top_line = "+"
        for c in range(self.cols):
            if c == 0 and not self.walls[0][0]["N"]:
                top_line += "   +"  # entrance opening
            else:
                top_line += "---+"
        lines.append(top_line)

        for r in range(self.rows):
            # Row with vertical walls and cell interiors
            row_line = ""
            # Left border for the row: based on west wall of first cell
            if self.walls[r][0]["W"]:
                row_line += "|"
            else:
                row_line += " "

            for c in range(self.cols):
                # Cell interior: mark path if present
                if (r, c) in path:
                    cell_content = " . "
                else:
                    cell_content = "   "

                # Right wall of cell
                if self.walls[r][c]["E"]:
                    row_line += cell_content + "|"
                else:
                    row_line += cell_content + " "
            lines.append(row_line)

            # Row with horizontal walls (between this row and the next)
            bottom_line = "+"
            for c in range(self.cols):
                if self.walls[r][c]["S"]:
                    bottom_line += "---+"
                else:
                    bottom_line += "   +"
            lines.append(bottom_line)

        return "\n".join(lines)

    def solve_bfs(self):
        """
        Solve the maze from (0,0) to (rows-1, cols-1) using BFS.
        Returns the list of (r, c) coordinates along the solution path.
        """
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        q = deque()
        q.append(start)
        visited = set([start])
        parent = {start: None}

        # Directions: (dr, dc, direction_from_current_to_neighbor)
        directions = [
            (-1, 0, "N"),
            (0, 1, "E"),
            (1, 0, "S"),
            (0, -1, "W")
        ]

        while q:
            r, c = q.popleft()
            if (r, c) == goal:
                break

            for dr, dc, d in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    # Check that there is NO wall between (r,c) and (nr,nc)
                    if not self.has_wall_between(r, c, nr, nc):
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            parent[(nr, nc)] = (r, c)
                            q.append((nr, nc))

        # Reconstruct path if goal reached
        if goal not in parent:
            return None  # unsolvable (shouldn't happen in a perfect maze)

        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path

    def has_wall_between(self, r1, c1, r2, c2):
        """Check if a wall exists between two neighboring cells."""
        if r1 == r2:
            if c1 < c2:
                return self.walls[r1][c1]["E"] or self.walls[r2][c2]["W"]
            else:
                return self.walls[r1][c1]["W"] or self.walls[r2][c2]["E"]
        elif c1 == c2:
            if r1 < r2:
                return self.walls[r1][c1]["S"] or self.walls[r2][c2]["N"]
            else:
                return self.walls[r1][c1]["N"] or self.walls[r2][c2]["S"]
        else:
            # Not neighbors; treat as wall
            return True


def main():
    rows = 3
    cols = 3

    maze = Maze(rows, cols)    
    
    maze.generate_kruskal()
    
    # Write unsolved maze
    maze_ascii = maze.to_ascii()
    with open("maze.maz", "w") as f:
        f.write(maze_ascii)

    # Solve using BFS
    path = maze.solve_bfs()
    if path is None:
        print("Not solvable.")
    else:
        path_set = set(path)
        maze_solved_ascii = maze.to_ascii(path=path_set)
        with open("maze_solved.maz", "w") as f:
            f.write(maze_solved_ascii)

        # Optionally also print to console
        print("Unsolved maze:\n")
        print(maze_ascii)
        print("\nSolved maze:\n")
        print(maze_solved_ascii)


if __name__ == "__main__":
    main()

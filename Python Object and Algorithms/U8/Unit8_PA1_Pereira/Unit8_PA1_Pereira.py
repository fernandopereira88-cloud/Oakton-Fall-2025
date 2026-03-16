'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/07/2025
############################################################################################################################
ASSIGNMENT: Graphs, Mazes, and Kruskal's Algorithm
================================================================================================================================================================================================================        

1) How many walls separate the cells of an NxN grid? 
    - 2*N*(N-1) walls because there are N*(N-1) internal vertical and N*(N-1) internal horizontal walls
    
    
2) Given an NxN maze with no cycles (a perfect maze), how many walls separate the cells? 
    - 2*N*(N-1) - (N^2-1) in which (N^2-1) are the number of walls removed in order to connect the vertices 
    
3) What is the runtime complexity of the find operation of the disjoint set data structure? 
    - Considering the application of Union by Rank and Path Compression, the runtime complexity for the find operations for the disjoint set should be O(alpha(n)) in which alpha is the 
      inverse Ackermann function, which grows very slowsly and behaves as a constant for practical consideration.
    
4) Intuitively, without a detailed analysis, how might we generalize the runtime complexity of the find operation. Hint: How are the cells stored? 
    - The cells are stored in a simple array that conceptually represents a tree. Each find operation traverses the tree, which is designed to be shallow, and should run almost at O(1) amortized given the tree shalowness.
    
5) Why do the paths created when generating a maze represent a minimum spanning tree? [1 point]
    - Kruskal's algorithm connects vertices by prioritizing the edges with the smallest weights. The fact that all edges have the same weight in the maze problem also makes this prioritization more straightforward and yield that every spanning tree in the maze is actually a minimum spanning tree.
    - The algorithm also prevents the formation of cycles in the graph. 
    - The combination of these two approaches converge to making a minimum spanning tree because it yields the lowest weighted connected path among vertices without creating a cycle
    
'''

from disjointsets import DisjointSet 
import random
from collections import deque

class Maze:
    '''
    Description: Holds the class definiton for Maze
    - Data attributes: 
        - _rows, _cols, and _walls (described in the constructor method)
    '''
    def __init__(self,rows,cols):
        '''
        Description: Constructor for Maze class constructor 
        Inputs:
            - rows: the number of rows in the maze provided by the user
            - cols: the number of columns in the maze provided by the user
        Outputs:
            - None back to the user   
            - Data attributes:
                - _rows: the number of rows in the maze
                - _cols: the number of columns in the maze
                - _walls: a dictionary for each element in a lists of lists describing the walls surrounding a space in the maze. 
                          True means that there is a wall in a particular direction (N - North, E - East, S - South, W - West).
                          At initialization, all spaces are completely surrounded by walls              
        '''
        self._rows = rows
        self._cols = cols
        
        # For each tile in the maze, initializes a dictionary mapping the alls, and starting with all walls equal true.
        # Walls will be removed while executing Kruskal's algorithm
        self._walls = [
            [{"N": True, "E": True, "S": True, "W": True} for _ in range(cols)]
            for _ in range(rows)
            ]
    
    def generate_kruskal_maze(self):
        '''
        Description: 
            - Applies the Kruskal algorithm to form the maze using a graph structure, and forming a path with edges while preventing the formation of cycles, and adjusting maze walls.
        Inputs: 
            - None required from the user, but will use _rows and _cols to determine the maze size and shape
        Outputs:
            - None returned to the user, but will adjust self._walls to form the maze structure
        '''
        n_cells = self._rows * self._cols
        ds = DisjointSet(n_cells) 
        
        
        # Initializes and constructs the list of neighbouring edges 
        # (down and right is fine given that the graph in undirected).
        edges = []        
        for r in range(self._rows):
            for c in range(self._cols):
                u = r*self._cols + c 
                
                #--add the edge between i and j to the edges array if cell i and cell j are neighbors.    
                if c + 1 < self._cols:
                    v = r*self._cols + c +1
                    edges.append((u,v))
                if r + 1 < self._rows:
                    v = (r+1)*self._cols + c
                    edges.append((u,v))
                    
        #--simulate a random maze generation, i.e., allow random edges to be selected.
        random.shuffle(edges)        
        
        mst = []         
        while len(mst) < n_cells -1:
            # (u, v) = remove an edge from edges
            edge = edges.pop()
            u = edge[0]
            v = edge[1]
            
            if ds.find(u) != ds.find(v): # Prevent the formation of cycles
                mst.append(edge) #----Add the edge to the minimum spanning tree; remove this wall --> Used to prevent infinite loop
                
                # Modify M by removing the wall connecting cell u and cell v.
                
                #### Get coordinates to remove wall
                ru = u // self._cols
                cu = u % self._cols
                rv = v // self._cols
                cv = v % self._cols
                
                #### Remove walls
                if ru == rv: # Same row                    
                    if cu < cv: # u is left neighbour of v
                        self._walls[ru][cu]["E"] = False
                        self._walls[rv][cv]["W"] = False
                    else: 
                        self._walls[ru][cu]["W"] = False
                        self._walls[rv][cv]["E"] = False
                if cu == cv: # Same column
                    if ru < rv: # u is above v
                        self._walls[ru][cu]["S"] = False
                        self._walls[rv][cv]["N"] = False
                    else:
                        self._walls[ru][cu]["N"] = False
                        self._walls[rv][cv]["S"] = False
                
                ds.union(u,v) # --Merge the sets containing u and v
                
        # Adjust entrance and Exit walls
        self._walls[0][0]["N"] = False
        self._walls[self._rows-1][self._cols-1]["S"] = False
        
    def create_maze_string(self, path=None):
        '''
        Description: Generates a string with the maze and path (if provided)
        Inputs:
            - path: Optional (default is None). A list of coordinates that have been visited when attempting to solve the maze.
        Outputs:
            - A string that can be stored in a file or printed by the user, containing a graphic visual of the maze and any paths navigated
        '''
        
        if path is None:
            path = set()
        lines = []
        
        # Top border
        top_line = "+"
        for c in range(self._cols):
            if c == 0 and not self._walls[0][0]["N"]:
                top_line += "   +"  # entrance
            else:
                top_line += "---+"
        lines.append(top_line)
                
        for r in range(self._rows):
            # Spaces and vertical walls
            row_line = ""
            # Draw left walls based on info within _walls
            if self._walls[r][0]["W"]:
                row_line += "|"
            else:
                row_line += " "
            
            for c in range(self._cols):
                
                if (r,c) in path: # Draw a path if it has been drawn
                    cell_content = " . "
                else: # Draw a space otherwise
                    cell_content = "   "
            
                # Draw right wall
                if self._walls[r][c]["E"]:
                    row_line += cell_content + "|"
                else:
                    row_line += cell_content + " "
            lines.append(row_line)
            
            # Horizontal lines
            bottom_line = "+"
            for c in range(self._cols):
                if self._walls[r][c]["S"]:
                    bottom_line += "---+"
                else: # Exit
                    bottom_line += "   +"
            lines.append(bottom_line)
            
         
        return "\n".join(lines)
    
    def solve_bfs(self):
        '''
        Description:
            - Solves the maze by using a Breadth-First search approach, exploring all nodes in the immediate level, before moving deeper into the maze.
            - Uses a deque (double-ended queue) that captures all surrounding nodes, tests for walls, and move deeper afterwards
            - Relationships between coordinates are stored in a dictionary an passed to a list for the user
        Inputs:
            - None from the user, but will use _rows and _cols and maze start and exit assumptions
        Outputs:
            - A list containing the ordered sequence of maze coordinates to be followed in order to get to the maze exit            
        '''
        start = (0,0)
        goal = (self._rows-1, self._cols-1)
        
        q = deque()
        q.append(start)
        visited = set([start])
        parent = {start : None}
        
        # Directions
        directions = [
            (-1,0,"N"),
            (0,1,"E"),
            (1,0,"S"),
            (0,-1,"W")
        ]
        
        while q:
            r, c = q.popleft()
            if (r,c) == goal:
                break
            
            for dr, dc, d in directions: # get direction row, direction col, and direction
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < self._rows and 0 <= nc < self._cols:
                    # Check for walls
                    if not self.check_walls(r,c,nr,nc):
                        if (nr,nc) not in visited:
                            visited.add((nr,nc))
                            parent[(nr,nc)] = (r,c)
                            q.append((nr,nc))
        
        
        # Reconstruct path         
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path
        
        
    def check_walls(self,r1,c1,r2,c2):
        """
        Description:
            - Check for the existance of wall between two coordinates (r1,c1) and (r2,c2)
        Inputs:
            - r1: row of coordinate 1
            - c1: column of coordinate 1
            - r2: row of coordinate 2
            - c2: column of coordinate 2
        Outputs:
            - Returns Boolean --> True means there is a wall between coordinates, False means there is no wall.
        """
        if r1 == r2:
            if c1 < c2:
                return self._walls[r1][c1]["E"] or self._walls[r2][c2]["W"]
            else:
                return self._walls[r1][c1]["W"] or self._walls[r2][c2]["E"]      
        elif c1 == c2:
            if r1 < r2:
                return self._walls[r1][c1]["S"] or self._walls[r2][c2]["N"]
            else:
                return self._walls[r1][c1]["N"] or self._walls[r2][c2]["S"]
        else:
            return True                                                

def main():
    '''
    Description:
        - Main Driver function for the assigment. 
        - Generates a maze using Kruksal's algorithm, solves it using a BFS method
        - Stores both maze and solution into separate files
        - Prints maze and solution to the user
    '''
    
    rows = 20
    cols = 20
    maze = Maze(rows,cols)
    
    # Generate maze
    maze.generate_kruskal_maze()
    maze_string = maze.create_maze_string()
    
    # Print generated maze
    print("Maze:")
    print(maze_string)
    
    # Stores maze in a file
    with open("maze.maz","w") as writeFile:
        writeFile.write(maze_string)
    
    # Solve maze using BFS
        
    path = maze.solve_bfs()
    maze_solved_string = maze.create_maze_string(path=path)    
    # Print solved maze
    print("\nSolved Maze:")
    print(maze_solved_string)

    # Stores solved maze in a file
    with open("maze_solved.maz","w") as writeFile:
        writeFile.write(maze_solved_string)    

if __name__ == "__main__":
    main()
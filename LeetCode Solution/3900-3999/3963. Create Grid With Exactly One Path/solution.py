class Solution:
    def createGrid(self, m: int, n: int) -> list[str]:
        # Fill the entire grid with obstacles '#'
        g = [['#' * n for _ in range(m)]]  # placeholder, let's write properly below:
        
        g = [['#' for _ in range(n)] for _ in range(m)]
        
        # Set all elements in the first row to '.'
        for j in range(n):
            g[0][j] = '.'
            
        # Set all elements in the last column to '.'
        for i in range(m):
            g[i][n - 1] = '.'
            
        return ["".join(row) for row in g]
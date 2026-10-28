class Solution:
    def minCost(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        
        # dp[i][j] will store a set of all possible XOR values to reach (i, j)
        dp = [[set() for _ in range(n)] for _ in range(m)]
        
        # Base case
        dp[0][0].add(grid[0][0])
        
        for i in range(m):
            for j in range(n):
                # If we can come from the top cell
                if i > 0:
                    for val in dp[i - 1][j]:
                        dp[i][j].add(val ^ grid[i][j])
                # If we can come from the left cell
                if j > 0:
                    for val in dp[i][j - 1]:
                        dp[i][j].add(val ^ grid[i][j])
                        
        # Return the minimum XOR value found at the bottom-right cell
        return min(dp[m - 1][n - 1])
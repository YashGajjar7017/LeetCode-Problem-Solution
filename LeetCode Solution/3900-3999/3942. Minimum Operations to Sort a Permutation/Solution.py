class Solution:
    def minOperations(self, nums: list[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0

        p0 = nums.index(0)

        # Check if nums is an INCREASING cyclic shift
        is_increasing = True
        for i in range(1, n):
            if nums[i] != (nums[0] + i) % n:
                is_increasing = False
                break

        if is_increasing:
            # Strategy 1: Rotate Left p0 times
            ops1 = p0
            
            # Strategy 2: Reverse -> Rotate -> Reverse
            # (Reverse turns it decreasing, rotate puts 0 at last position n-1, reverse puts it back increasing)
            # Reverse 1: 0 moves to index (n - 1 - p0)
            # Rotate left (n - 1 - p0 + 1) = (n - p0) times to put 0 at index n - 1
            # Reverse 2: 0 moves to index 0, array becomes sorted [0, 1, ..., n-1]
            ops2 = 1 + (n - p0) + 1
            
            return min(ops1, ops2)

        # Check if nums is a DECREASING cyclic shift
        is_decreasing = True
        for i in range(1, n):
            if nums[i] != (nums[0] - i + n) % n:
                is_decreasing = False
                break

        if is_decreasing:
            # Strategy 1: Reverse first, then rotate left until '0' is at index 0
            ops1 = 1 + (n - 1 - p0)  # = n - p0
            
            # Strategy 2: Rotate left until '0' is at index n-1, then reverse
            ops2 = ((p0 + 1) % n) + 1
            
            return min(ops1, ops2)

        return -1
class Solution:
    def minOperations(self, s: str) -> int:
        n = len(s)
        s_sorted = "".join(sorted(s))
        
        # 0 ops: already sorted
        if s == s_sorted:
            return 0
        
        # Impossible: length <= 2 and not sorted
        if n <= 2:
            return -1
        
        # 1 op: either the first or last character is already in its correct sorted position
        if s[0] == s_sorted[0] or s[-1] == s_sorted[-1]:
            return 1
        
        # 2 ops: the smallest character is present somewhere in s[0...n-2] 
        # OR the largest character is present somewhere in s[1...n-1]
        min_char = s_sorted[0]
        max_char = s_sorted[-1]
        
        if min_char in s[:-1] or max_char in s[1:]:
            return 2
        
        # 3 ops: min_char is trapped at the very end AND max_char is trapped at the very beginning
        return 3
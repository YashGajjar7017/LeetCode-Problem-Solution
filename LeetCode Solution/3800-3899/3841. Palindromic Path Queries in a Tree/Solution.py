class SegmentTree:
    def __init__(self, n, initial_masks):
        self.n = n
        self.tree = [0] * (4 * n)
        self.build(1, 0, n - 1, initial_masks)

    def build(self, node, l, r, initial_masks):
        if l == r:
            self.tree[node] = initial_masks[l]
            return
        mid = (l + r) // 2
        self.build(2 * node, l, mid, initial_masks)
        self.build(2 * node + 1, mid + 1, r, initial_masks)
        self.tree[node] = self.tree[2 * node] ^ self.tree[2 * node + 1]

    def update(self, node, l, r, idx, val):
        if l == r:
            self.tree[node] = val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self.update(2 * node, l, mid, idx, val)
        else:
            self.update(2 * node + 1, mid + 1, r, idx, val)
        self.tree[node] = self.tree[2 * node] ^ self.tree[2 * node + 1]

    def query(self, node, l, r, ql, qr):
        if qr < l or ql > r:
            return 0
        if ql <= l and r <= qr:
            return self.tree[node]
        mid = (l + r) // 2
        return self.query(2 * node, l, mid, ql, qr) ^ self.query(2 * node + 1, mid + 1, r, ql, qr)


class Solution:
    def palindromePath(self, n: int, edges: list[list[int]], s: str, queries: list[str]) -> list[bool]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        parent = [0] * n
        depth = [0] * n
        heavy = [-1] * n
        head = [0] * n
        pos = [0] * n
        
        # 1st DFS: compute subtree sizes, depth, parent, heavy child
        def dfs1(u, p, d):
            parent[u] = p
            depth[u] = d
            size = 1
            max_sub_size = 0
            for v in adj[u]:
                if v != p:
                    sub_size = dfs1(v, u, d + 1)
                    size += sub_size
                    if sub_size > max_sub_size:
                        max_sub_size = sub_size
                        heavy[u] = v
            return size

        dfs1(0, -1, 0)

        # 2nd DFS: build HLD chains and position mapping
        cur_pos = 0
        def dfs2(u, h):
            nonlocal cur_pos
            head[u] = h
            pos[u] = cur_pos
            cur_pos += 1
            
            if heavy[u] != -1:
                dfs2(heavy[u], h)
                
            for v in adj[u]:
                if v != parent[u] and v != heavy[u]:
                    dfs2(v, v)

        dfs2(0, 0)

        # Initialize segment tree with masks based on flattened positions
        masks = [0] * n
        chars = list(s)
        for i in range(n):
            masks[pos[i]] = 1 << (ord(chars[i]) - ord('a'))

        seg = SegmentTree(n, masks)

        def query_path(u, v):
            res = 0
            while head[u] != head[v]:
                if depth[head[u]] < depth[head[v]]:
                    u, v = v, u
                h = head[u]
                res ^= seg.query(1, 0, n - 1, pos[h], pos[u])
                u = parent[h]
            if depth[u] > depth[v]:
                u, v = v, u
            res ^= seg.query(1, 0, n - 1, pos[u], pos[v])
            return res

        ans = []
        for q in queries:
            parts = q.split()
            if parts[0] == "update":
                node = int(parts[1])
                new_char = parts[2]
                chars[node] = new_char
                new_mask = 1 << (ord(new_char) - ord('a'))
                seg.update(1, 0, n - 1, pos[node], new_mask)
            else:
                u = int(parts[1])
                v = int(parts[2])
                mask = query_path(u, v)
                # Check if at most one bit is set
                is_palindrome = (mask == 0 or (mask & (mask - 1)) == 0)
                ans.append(is_palindrome)

        return ans
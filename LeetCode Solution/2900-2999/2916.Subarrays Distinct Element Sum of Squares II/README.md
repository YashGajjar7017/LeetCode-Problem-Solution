---
comments: true
difficulty: 困难
edit_url: https://github.com/doocs/leetcode/edit/main/solution/2900-2999/2916.Subarrays%20Distinct%20Element%20Sum%20of%20Squares%20II/README.md
rating: 2816
source: 第 116 场双周赛 Q4
tags:
    - 树状数组
    - 线段树
    - 数组
    - 动态规划
---

<!-- problem:start -->

# [2916. 子数组不同元素数目的平方和 II](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-ii)

[English Version](/solution/2900-2999/2916.Subarrays%20Distinct%20Element%20Sum%20of%20Squares%20II/README_EN.md)

## 题目描述

<!-- description:start -->

<p>给你一个下标从 <strong>0</strong>&nbsp;开始的整数数组&nbsp;<code>nums</code>&nbsp;。</p>

<p>定义 <code>nums</code>&nbsp;一个子数组的 <strong>不同计数</strong>&nbsp;值如下：</p>

<ul>
	<li>令&nbsp;<code>nums[i..j]</code>&nbsp;表示 <code>nums</code> 中所有下标在 <code>i</code> 到 <code>j</code> 范围内的元素构成的子数组（满足 <code>0 &lt;= i &lt;= j &lt; nums.length</code> ），那么我们称子数组&nbsp;<code>nums[i..j]</code>&nbsp;中不同值的数目为&nbsp;<code>nums[i..j]</code>&nbsp;的不同计数。</li>
</ul>

<p>请你返回 <code>nums</code>&nbsp;中所有子数组的 <strong>不同计数</strong>&nbsp;的 <strong>平方</strong>&nbsp;和。</p>

<p>由于答案可能会很大，请你将它对&nbsp;<code>10<sup>9</sup> + 7</code>&nbsp;<strong>取余</strong>&nbsp;后返回。</p>

<p>子数组指的是一个数组里面一段连续 <strong>非空</strong>&nbsp;的元素序列。</p>

<p>&nbsp;</p>

<p><strong class="example">示例 1：</strong></p>

<pre>
<b>输入：</b>nums = [1,2,1]
<b>输出：</b>15
<b>解释：</b>六个子数组分别为：
[1]: 1 个互不相同的元素。
[2]: 1 个互不相同的元素。
[1]: 1 个互不相同的元素。
[1,2]: 2 个互不相同的元素。
[2,1]: 2 个互不相同的元素。
[1,2,1]: 2 个互不相同的元素。
所有不同计数的平方和为 1<sup>2</sup> + 1<sup>2</sup> + 1<sup>2</sup> + 2<sup>2</sup> + 2<sup>2</sup> + 2<sup>2</sup> = 15 。
</pre>

<p><strong class="example">示例 2：</strong></p>

<pre>
<b>输入：</b>nums = [2,2]
<b>输出：3</b>
<strong>解释：</strong>三个子数组分别为：
[2]: 1 个互不相同的元素。
[2]: 1 个互不相同的元素。
[2,2]: 1 个互不相同的元素。
所有不同计数的平方和为 1<sup>2</sup> + 1<sup>2</sup> + 1<sup>2</sup> = 3 。
</pre>

<p>&nbsp;</p>

<p><strong>提示：</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>5</sup></code></li>
</ul>

<!-- description:end -->

## 解法

<!-- solution:start -->

### 方法一

<!-- tabs:start -->

#### Python3

```python
class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree_sum = [0] * (4 * n)
        self.tree_sq = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
        self.MOD = 10**9 + 7

    def _apply(self, node, l, r, val):
        length = r - l + 1
        val %= self.MOD
        
        # new_sq = sq + 2 * val * sum + length * val^2
        self.tree_sq[node] = (
            self.tree_sq[node] 
            + 2 * val * self.tree_sum[node] 
            + length * val * val
        ) % self.MOD
        
        self.tree_sum[node] = (self.tree_sum[node] + length * val) % self.MOD
        self.lazy[node] = (self.lazy[node] + val) % self.MOD

    def _push(self, node, l, r):
        if self.lazy[node] != 0:
            mid = (l + r) // 2
            self._apply(2 * node, l, mid, self.lazy[node])
            self._apply(2 * node + 1, mid + 1, r, self.lazy[node])
            self.lazy[node] = 0

    def update(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self._apply(node, l, r, val)
            return
        
        self._push(node, l, r)
        mid = (l + r) // 2
        
        if ql <= mid:
            self.update(2 * node, l, mid, ql, qr, val)
        if qr > mid:
            self.update(2 * node + 1, mid + 1, r, ql, qr, val)
            
        self.tree_sum[node] = (self.tree_sum[2 * node] + self.tree_sum[2 * node + 1]) % self.MOD
        self.tree_sq[node] = (self.tree_sq[2 * node] + self.tree_sq[2 * node + 1]) % self.MOD


class Solution:
    def sumCounts(self, nums: list[int]) -> int:
        n = len(nums)
        MOD = 10**9 + 7
        st = SegmentTree(n)
        
        last_pos = {}
        total_ans = 0
        
        for i, val in enumerate(nums):
            prev_idx = last_pos.get(val, -1)
            
            # Range add +1 to all subarrays starting from index (prev_idx + 1) to i
            st.update(1, 0, n - 1, prev_idx + 1, i, 1)
            
            # Add the sum of squares of distinct counts for all subarrays ending at index i
            total_ans = (total_ans + st.tree_sq[1]) % MOD
            
            # Update last seen position of the element
            last_pos[val] = i
            
        return total_ans
```

#### Java

```java

```

#### C++

```cpp

```

#### Go

```go

```

<!-- tabs:end -->

<!-- solution:end -->

<!-- problem:end -->

from functools import reduce

count_sum = lambda nums: reduce(lambda next, prev: next + prev, nums)

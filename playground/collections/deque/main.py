from collections import deque

if __name__ == "__main__":
    stack = deque()

    stack.append(1)
    stack.appendleft(2)
    stack.append(3)
    assert stack.pop() == 3
    assert stack.pop() == 1
    assert stack.pop() == 2
    assert len(stack) == 0

    stack.extend([1, 2, 3])
    stack.rotate(2)
    assert stack.pop() == 1
    assert stack.popleft() == 2
    assert len(stack) == 1
    stack.appendleft(1)
    stack.insert(1, 2)
    assert [3, 2, 1] == [stack.pop() for _ in range(3)]

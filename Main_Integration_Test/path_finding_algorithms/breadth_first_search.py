def bfs(maze, start, end):
    rows, cols = maze.shape
    queue = deque([(start, [])])  # (current position, path_taken)
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == end:
            return path + [(x, y)]

        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx, ny] == 255:
                queue.append(((nx, ny), path + [(x, y)]))

    return []

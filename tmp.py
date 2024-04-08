def find_path(self, start, goal):
    open_set = set()
    closed_set = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: self.heuristic(start, goal)}

    open_set.add(start)

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == goal:
            return self.reconstruct_path(came_from, goal)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in self.neighbors(current):
            move_direction = (neighbor[0] - current[0], neighbor[1] - current[1])
            if move_direction == (-self.last_move[0], -self.last_move[1]):
                continue

            tentative_g_score = g_score[current] + self.cost(current, neighbor)

            if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                if neighbor not in open_set:
                    open_set.add(neighbor)

        self.last_move = (goal[0] - current[0], goal[1] - current[1])

    return None
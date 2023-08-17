import random
import curses

# Set up the screen
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()
w = stdscr.subwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Initialize the snake and food
snake_x = sw // 4
snake_y = sh // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_PI)

# Initial direction and score
key = curses.KEY_RIGHT
score = 0

# Game loop
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Check if snake hit the wall or itself
    if (
        snake[0][0] in [0, sh] or
        snake[0][1] in [0, sw] or
        snake[0] in snake[1:]
    ):
        curses.endwin()
        quit()

    new_head = [snake[0][0], snake[0][1]]

    # Move the snake based on the key
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)

    # Check if snake ate the food
    if snake[0] == food:
        score += 1
        food = None
        while food is None:
            nf = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    # Display score
    w.addstr(0, 2, f"Score: {score}")

    # Increase game speed as score increases
    if score >= 5:
        w.timeout(80)
    if score >= 10:
        w.timeout(60)
    if score >= 15:
        w.timeout(40)

    # Game over condition
    if score >= 20:
        w.addstr(sh // 2, sw // 2 - 5, "GAME OVER")
        w.refresh()
        curses.napms(2000)
        break

# Clean up
curses.endwin()

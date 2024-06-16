import random
import curses

# Game settings
board_width = 40  # Doubled width
board_height = 20  # Doubled height
snake = [(10, 10)]  # Adjusted initial position of the snake
direction = 'RIGHT'
food = (random.randint(1, board_height - 2), random.randint(1, board_width - 2))
score = 0

def main(stdscr):
    global direction, snake, food, score

    # Curses setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Don't wait for user input
    stdscr.timeout(200)  # Lowered speed by increasing timeout to 200 milliseconds

    while True:
        # Get user input
        key = stdscr.getch()
        if key == curses.KEY_UP and direction != 'DOWN':
            direction = 'UP'
        elif key == curses.KEY_DOWN and direction != 'UP':
            direction = 'DOWN'
        elif key == curses.KEY_LEFT and direction != 'RIGHT':
            direction = 'LEFT'
        elif key == curses.KEY_RIGHT and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        head_y, head_x = snake[0]

        if direction == 'UP':
            new_head = (head_y - 1, head_x)
        elif direction == 'DOWN':
            new_head = (head_y + 1, head_x)
        elif direction == 'LEFT':
            new_head = (head_y, head_x - 1)
        elif direction == 'RIGHT':
            new_head = (head_y, head_x + 1)

        # Check for collisions
        if (new_head in snake or
                new_head[0] in [0, board_height - 1] or
                new_head[1] in [0, board_width - 1]):
            stdscr.addstr(board_height // 2, board_width // 2 - 5, 'Game Over!')
            stdscr.refresh()
            stdscr.nodelay(0)  # Wait for user input before exiting
            stdscr.getch()
            break

        snake = [new_head] + snake[:-1]

        # Check if food is eaten
        if new_head == food:
            snake.append(snake[-1])  # Grow the snake
            score += 1
            while food in snake:
                food = (random.randint(1, board_height - 2), random.randint(1, board_width - 2))

        # Display the game board
        stdscr.clear()
        stdscr.addstr(0, 0, f'Score: {score}')
        for y, x in snake:
            if 0 <= y < board_height and 0 <= x < board_width:
                stdscr.addstr(y, x, 'S')
        if 0 <= food[0] < board_height and 0 <= food[1] < board_width:
            stdscr.addstr(food[0], food[1], 'F')
        stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)

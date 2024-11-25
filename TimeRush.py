import tkinter as tk
import random
import time

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 20

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()
        
        self.score = 0
        self.time_left = 15
        self.delay = 100  # Milliseconds
        
        # Create score and timer text
        self.score_text = self.canvas.create_text(340, 10, anchor='nw', text="Score: 0", font='Helvetica 12 bold')
        self.timer_text = self.canvas.create_text(200, 10, anchor='nw', text="15", font='Helvetica 20 bold')

        # Player initialization
        self.player = self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="blue")
        self.current_direction = None

        # Initialize goals and obstacles
        self.goals = []
        self.obstructions = []
        self.create_objects()

        # Bind keys for movement
        self.root.bind("<Left>", lambda _: self.change_direction('left'))
        self.root.bind("<Right>", lambda _: self.change_direction('right'))
        self.root.bind("<Up>", lambda _: self.change_direction('up'))
        self.root.bind("<Down>", lambda _: self.change_direction('down'))

        # Start the game loop
        self.start_time = time.time()
        self.update_game()

    def change_direction(self, direction):
        self.current_direction = direction

    def create_objects(self):
        # Create goals and obstructions
        exclude_positions = [self.canvas.coords(self.player)]
        for _ in range(3):
            self.goals.append(self.create_goal(exclude_positions))
            exclude_positions.append(self.canvas.coords(self.goals[-1]))

        for _ in range(3):
            self.obstructions.append(self.create_obstruction(exclude_positions))
            exclude_positions.append(self.canvas.coords(self.obstructions[-1]))

    def create_goal(self, exclude_positions):
        x1, y1, x2, y2 = self.random_position(exclude_positions)
        goal = self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
        return goal

    def create_obstruction(self, exclude_positions):
        x1, y1, x2, y2 = self.random_position(exclude_positions)
        obs = self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        return obs

    def random_position(self, exclude_positions):
        while True:
            x1 = random.randint(0, CANVAS_WIDTH - SIZE)
            y1 = random.randint(0, CANVAS_HEIGHT - SIZE)
            x2 = x1 + SIZE
            y2 = y1 + SIZE
            if all(not self.check_collision((x1, y1, x2, y2), pos) for pos in exclude_positions):
                return x1, y1, x2, y2

    def check_collision(self, rect1, rect2):
        x1, y1, x2, y2 = rect1
        ox1, oy1, ox2, oy2 = rect2
        return x1 < ox2 and x2 > ox1 and y1 < oy2 and y2 > oy1

    def move_player(self):
        if self.current_direction == 'left':
            self.canvas.move(self.player, -SIZE, 0)
        elif self.current_direction == 'right':
            self.canvas.move(self.player, SIZE, 0)
        elif self.current_direction == 'up':
            self.canvas.move(self.player, 0, -SIZE)
        elif self.current_direction == 'down':
            self.canvas.move(self.player, 0, SIZE)

    def update_game(self):
        # Update time
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1:
            self.time_left -= 1
            self.canvas.itemconfig(self.timer_text, text=str(self.time_left))
            self.start_time = time.time()

        if self.time_left <= 0:
            self.end_game()
            return

        # Move player
        self.move_player()

        # Check for collisions
        px1, py1, px2, py2 = self.canvas.coords(self.player)

        for goal in self.goals:
            if self.check_collision((px1, py1, px2, py2), self.canvas.coords(goal)):
                self.score += 10
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                self.canvas.delete(goal)
                self.goals.remove(goal)
                self.goals.append(self.create_goal([]))

        for obs in self.obstructions:
            if self.check_collision((px1, py1, px2, py2), self.canvas.coords(obs)):
                self.end_game()
                return

        # Schedule next update
        self.root.after(self.delay, self.update_game)

    def end_game(self):
        self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="Game Over!", font='Helvetica 20 bold', fill="red")
        self.root.update()

def main():
    root = tk.Tk()
    root.title("Python Game with tkinter")
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()

from tkinter import *
import random
import statistics

# Game Constants
WIDTH, HEIGHT, SPACE = 600, 600, 20
SPEED = 120
SNAKE_COLOR = "#FF69B4"
FOOD_COLOR = "#DA70D6"
BG_COLOR = "#FFF0F5"
TEXT_COLOR = "#800080"

# Analytics & Score
scores = []

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game - Main Menu")
        self.frame = Frame(root, bg=BG_COLOR)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="🐍 Snake - Lavender Edition", font=('Consolas', 30),
              fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=40)
        Button(self.frame, text="Start Game", font=('Consolas', 20), bg=FOOD_COLOR,
               command=self.start_game).pack(pady=20)
        Button(self.frame, text="Quit", font=('Consolas', 18), bg="#ffcccc",
               command=root.destroy).pack(pady=10)

    def start_game(self):
        self.frame.destroy()
        SnakeGame(self.root)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake - Lavender Edition")
        # Canvas & Score Label
        self.canvas = Canvas(root, bg=BG_COLOR, height=HEIGHT, width=WIDTH)
        self.canvas.pack()
        self.label = Label(root, text="Score: 0", font=('Consolas', 20),
                           fg=TEXT_COLOR, bg=BG_COLOR)
        self.label.pack()

        # Game State
        self.score = 0
        self.direction = 'Right'
        self.body = [[SPACE*3, SPACE*3]]
        self.squares = [self.draw_square(*self.body[0])]
        self.food = self.spawn_food()

        # Controls & Loop
        self.setup_bindings()
        self.root.after(SPEED, self.next_turn)

    def draw_square(self, x, y):
        return self.canvas.create_rectangle(x, y, x+SPACE, y+SPACE, fill=SNAKE_COLOR)

    def spawn_food(self):
        while True:
            x = random.randint(0, (WIDTH - SPACE)//SPACE) * SPACE
            y = random.randint(0, (HEIGHT - SPACE)//SPACE) * SPACE
            if [x, y] not in self.body:
                oval = self.canvas.create_oval(x, y, x+SPACE, y+SPACE, fill=FOOD_COLOR)
                return (oval, [x, y])

    def setup_bindings(self):
        for key, dir in [("<Up>", "Up"), ("<Down>", "Down"), ("<Left>", "Left"), ("<Right>", "Right")]:
            self.root.bind(key, lambda e, d=dir: self.change_direction(d))

    def change_direction(self, new_dir):
        opposites = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
        if new_dir != opposites[self.direction]:
            self.direction = new_dir

    def next_turn(self):
        dx, dy = {'Up':(0,-SPACE),'Down':(0,SPACE),'Left':(-SPACE,0),'Right':(SPACE,0)}[self.direction]
        new_head = [self.body[0][0]+dx, self.body[0][1]+dy]

        if self.collided(new_head):
            return self.game_over()

        # Move snake
        self.body.insert(0, new_head)
        self.squares.insert(0, self.draw_square(*new_head))

        # Eat food?
        if new_head == self.food[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete(self.food[0])
            self.food = self.spawn_food()
        else:
            self.canvas.delete(self.squares.pop())
            self.body.pop()

        self.root.after(SPEED, self.next_turn)

    def collided(self, head):
        x, y = head
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or head in self.body[1:]

    def game_over(self):
        scores.append(self.score)
        # Show Game Over text & stats
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER",
                                fill=TEXT_COLOR, font=('Consolas',40))
        self.canvas.create_text(WIDTH/2, HEIGHT/2+50,
                                text=f"Your Score: {self.score}",
                                fill=TEXT_COLOR, font=('Consolas',20))
        self.show_stats()

        # Add on-screen buttons
        self.btn_frame = Frame(self.root, bg=BG_COLOR)
        self.btn_frame.pack(pady=10)
        Button(self.btn_frame, text="Restart", font=('Consolas',15),
               command=self.restart).pack(side=LEFT, padx=5)
        Button(self.btn_frame, text="Quit", font=('Consolas',15),
               command=self.root.destroy).pack(side=LEFT, padx=5)

    def show_stats(self):
        if len(scores) > 1:
            avg = statistics.mean(scores)
            med = statistics.median(scores)
            rng = max(scores) - min(scores)
            cnt = len(scores)
            text = f"Games: {cnt}, Avg: {avg:.1f}, Median: {med}, Range: {rng}"
            self.canvas.create_text(WIDTH/2, HEIGHT/2+90,
                                    text=text, fill=TEXT_COLOR,
                                    font=('Consolas',12))

    def restart(self):
        # Remove buttons
        if hasattr(self, 'btn_frame'):
            self.btn_frame.destroy()
        # Clear canvas and reset state
        self.canvas.delete("all")
        self.score = 0
        self.direction = 'Right'
        self.body = [[SPACE*3, SPACE*3]]
        self.squares = [self.draw_square(*self.body[0])]
        self.label.config(text="Score: 0")
        self.food = self.spawn_food()
        # Resume game loop
        self.root.after(SPEED, self.next_turn)

# Run Game
if __name__ == "__main__":
    root = Tk()
    MainMenu(root)
    root.mainloop()

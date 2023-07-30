from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random

INITIAL_SPEED = 7
GOAL_SCORE = 10

class PongPaddle(Widget):
    score = NumericProperty(0)
    color_red = NumericProperty(0)
    color_green = NumericProperty(0)
    color_blue = NumericProperty(0)
    color = ReferenceListProperty(color_red, color_green, color_blue)


    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset



class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    gameover = BooleanProperty(False)

    def serve_ball(self, vel):
        self.ball.center = self.center
        self.ball.velocity = vel

    def reset(self):
        self.player1.score = 0
        self.player2.score = 0
        self.gameover = False
        self.serve_ball(Vector(INITIAL_SPEED, 0).rotate(random.randint(0, 360)))


    def update(self, dt):
        if not self.gameover:
            self.ball.move()

            self.player1.bounce_ball(self.ball)
            self.player2.bounce_ball(self.ball)

            # bounce off top or bottom of screen
            if (self.ball.y < 0) or (self.ball.top > self.height):
                self.ball.velocity_y *= -1

            # hit vertical edge - point scored for other player
            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball((INITIAL_SPEED, 0))
            if self.ball.x > self.width:
                self.player1.score += 1
                self.serve_ball((-INITIAL_SPEED, 0))
            
            if self.player1.score >= GOAL_SCORE or self.player2.score >= GOAL_SCORE:  
                self.gameover = True

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball(Vector(INITIAL_SPEED, 0).rotate(random.randint(0, 360)))
        Clock.schedule_interval(game.update, 1.0 / 120.0)
        return game


if __name__ == "__main__":
    PongApp().run()

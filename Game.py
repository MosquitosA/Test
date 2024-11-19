from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
import random

class Enemy(Image):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.speed = 2
        self.missile_speed = 3
        self.health = 1
        self.size_hint = (None, None)
        self.size = (50, 50)

    def move(self):
        self.x -= self.speed

    def drop_missile(self, shooter):
        missile = Missile()
        missile.center_x = self.center_x
        missile.y = self.y
        shooter.add_widget(missile)
        Animation(center_y=Window.height, duration=2).start(missile)

class Missile(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Missile, self).__init__(**kwargs)
        self.source = 'missile.png'
        self.size_hint = (None, None)
        self.size = (20, 20)
        self.allow_stretch = True
        self.keep_reference = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.remove_widget(self)
        return super(Missile, self).on_touch_down(touch)

class Shooter(Image):
    def __init__(self, **kwargs):
        super(Shooter, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 50)
        self.source = 'shooter.png'

    def move(self, touch):
        if touch:
            self.center_x = touch.x

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.shooter = Shooter()
        self.layout.add_widget(self.shooter)
        self.enemies = []
        self.missiles = []
        self.score = 0
        self.add_widget(self.layout)
        self.bind(size=self.resize)
        self.setup_enemies()
        Clock.schedule_interval(self.update, 1/60.)

    def setup_enemies(self):
        for _ in range(5):
            enemy = Enemy(source='enemy.png')
            enemy.x = Window.width
            enemy.y = random.randint(50, Window.height - 50)
            self.layout.add_widget(enemy)
            self.enemies.append(enemy)

    def update(self, dt):
        self.move_enemies()
        self.move_missiles()
        self.check_collisions()

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
            if enemy.x < 0:
                self.layout.remove_widget(enemy)
                enemy.x = Window.width
                enemy.y = random.randint(50, Window.height - 50)
                self.enemies.append(enemy)

    def move_missiles(self):
        for missile in self.missiles:
            missile.y -= missile.missile_speed
            if missile.y < 0:
                self.layout.remove_widget(missile)

    def check_collisions(self):
        for enemy in self.enemies:
            for missile in self.missiles:
                if enemy.collide_widget(missile):
                    self.layout.remove_widget(enemy)
                    self.layout.remove_widget(missile)
                    self.enemies.remove(enemy)
                    self.missiles.remove(missile)
                    self.score += 1
                    self.update_score()

    def update_score(self):
        self.score_label = Label(text=f'Score: {self.score}', size_hint=(None, None), size=(100, 50), pos=(10, 10))
        self.layout.add_widget(self.score_label)

    def resize(self, instance, value):
        self.shooter.size = (100, 50)
        self.shooter.center_x = self.center_x
        self.shooter.center_y = self.center_y - 150

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        game_screen = GameScreen(name='game')
        sm.add_widget(game_screen)
        return sm

if __name__ == '__main__':
    GameApp().run()

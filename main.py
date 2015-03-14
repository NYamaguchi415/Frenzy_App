
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, OptionProperty, ObjectProperty
from kivy.graphics import Color, BorderImage
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.utils import platform
from kivy.factory import Factory
from random import choice, random, randint
from kivy.logger import Logger
from functools import partial
from kivy.uix.popup import Popup

class Game(Widget):

	cube_size = NumericProperty(10)
	cube_padding = NumericProperty(10)
	score = NumericProperty(0)
	press_x = NumericProperty(0)
	press_y = NumericProperty(0)

	def __init__(self, **kwargs):
		super(Game, self).__init__()
		self.grid = [
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None]]

		# Bind window on_key_down to self.on_key_down (Your own function)
		#Window.bind(on_key_down = self.on_key_down)
		# Suppress windows on_keyboard function
		#Window.on_keyboard = lambda *x: None

		self.restart()

	def restart(self, *args):
		print self.grid
		print 'ononon'
		
		self.grid = [
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None]]
		self.reposition()
		Clock.schedule_once(partial(self.spawn_char,2,2), 1)
		self.score = 0
		#self.ids.end.opacity = 0 #????????? left out spawn number

	def reposition(self, *args):
		self.rebuild_background()
		# calculate the size of a number
		l = min(self.width, self.height)
		padding = (l / 4.) / 8.
		cube_size = (l - (padding * 5)) / 4.
		self.cube_size = cube_size
		self.cube_padding = padding

		for ix, iy, number in self.iterate():
		    number.size = cube_size, cube_size
		    number.pos = self.index_to_pos(ix, iy)

	def iterate(self):
		for ix, iy in self.iterate_pos():
			child = self.grid[ix][iy]
			if child:
				yield ix, iy, child

	def iterate_empty(self):
		for ix, iy in self.iterate_pos():
			child = self.grid[ix][iy]
			if not child:
				yield ix, iy

	def iterate_pos(self):
		for ix in range(5):
			for iy in range(5):
				yield ix, iy

	def reposition(self, *args):
		self.rebuild_background()
		l = min(self.width, self.height)
		padding = (l / 4.) / 100.
		cube_size = (l - (padding * 5)) / 5.
		self.cube_size = cube_size
		self.cube_padding = padding

	def rebuild_background(self):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(0xbb / 255., 0xad / 255., 0xa0 / 255.)
			BorderImage(pos=self.pos, size=self.size, source='data/round.png')
			Color(0xcc / 255., 0xc0 / 255., 0xb3 / 255.)
			csize = self.cube_size, self.cube_size
			for ix, iy in self.iterate_pos():
				BorderImage(pos=self.index_to_pos(ix, iy), size=csize,
				source='data/round.png')

	def index_to_pos(self, ix, iy):
		padding = self.cube_padding
		cube_size = self.cube_size
		return [
			(self.x + padding) + ix * (cube_size + padding),
			(self.y + padding) + iy * (cube_size + padding)]

	def spawn_char(self, ix, iy, *args):
		char = Character(
				size = (self.cube_size, self.cube_size),
				pos = self.index_to_pos(ix, iy))
		self.grid[ix][iy] = char
		self.add_widget(char)

	def on_touch_up(self, touch):
		x_dist = touch.psx - touch.osx
		y_dist = touch.psy - touch.osy

		if abs(x_dist) > abs(y_dist):
			if abs(x_dist) > .05:
				self.move_x(x_dist)
		elif abs(x_dist) < abs(y_dist):
			if abs(y_dist) > .05:
				self.move_y(y_dist)
		else:
			pass

	def move_x(self, x_dist):
		new_x = 10
		grid = self.grid
		char_loc = self.char_loc()
		char_x = char_loc[0]
		char_y = char_loc[1]
		char = grid[char_x][char_y]

		if x_dist > 0:
			if char_x == 4:
				return
			else:
				new_x = char_x + 1
		elif x_dist < 0:
			if char_x == 0:
				return
			else:
				new_x = char_x - 1
		pos = self.index_to_pos(new_x, char_y)
		char.move_to(pos)
		grid[char_x][char_y] = None
		if isinstance(grid[new_x][char_y], Cannon):
			grid[new_x][char_y] = char
			self.end_game()
		else:
			grid[new_x][char_y] = char
			char_loc = self.char_loc()
	
	def move_y(self, y_dist):
		new_y = 0
		grid = self.grid
		char_loc = self.char_loc()
		char_x = char_loc[0]
		char_y = char_loc[1]
		char = grid[char_x][char_y]

		if y_dist > 0:
			if char_y == 4:
				return
			else:
				new_y = char_y + 1
		elif y_dist < 0:
			if char_y == 0:
				return
			else:
				new_y = char_y - 1
		pos = self.index_to_pos(char_x, new_y)
		char.move_to(pos)
		grid[char_x][char_y] = None
		if isinstance(grid[char_x][new_y], Cannon):
			grid[char_x][new_y] = char
			self.end_game()
		else:
			grid[char_x][new_y] = char

	def char_loc(self):
		grid = self.grid
		for ix in range(5):
			for iy in range(5):
				if isinstance(grid[ix][iy],Character) :
					return ix, iy

	def spawn_cannon(self, *args):
		grid = self.grid
		ix = randint(0,4)
		iy = randint(0,4)
		cannon = Cannon(
				size = (self.cube_size, self.cube_size),
				pos = self.index_to_pos(ix, iy))
		
		self.add_widget(cannon)
		#Use lambda to drop dt argument
		Clock.schedule_once(lambda dt: self.remove_widget(cannon),1.5)
		if self.grid[ix][iy] == None:
			self.grid[ix][iy] = cannon
			Clock.schedule_once(lambda dt: self.grid_clear(ix, iy),1)
		elif isinstance(grid[ix][iy], Character):
				self.end_game()

	def grid_clear(self, a, b, *args):
		self.grid[a][b] = None

	def start_game(self, *args):
		Clock.schedule_interval(self.spawn_cannon,1)

	def unschedule_all(self, *args):
		Clock.unschedule(self.spawn_cannon)

	def end_game(self, *args):
		self.unschedule_all()
		s = Scorepop()
		s.score = 0
		s.open()
		s.bind(on_dismiss = self.restart)
		for ix, iy, child in self.iterate():
			child.destroy()

class Character(Image):
	def __init__(self, **kwargs):
		super(Character, self).__init__(**kwargs)

	def move_to(self, pos):
		if self.pos == pos:
			return
		Animation(pos=pos, d=.3).start(self)

	def destroy(self, *args):
		self.parent.remove_widget(self)

class Knight(Image):
	def __init__(self, **kwargs):
		super(Knight, self).__init__(**kwargs)


class Cannon(Image):
	def __init__(self, **kwargs):
		super(Cannon, self).__init__(**kwargs)

	def destroy(self, *args):
		self.parent.remove_widget(self)

class Scorepop(Popup):
	score = NumericProperty(0)

class FrenzyApp(App):
	def build(self):
		global app
		app = self

if __name__ == '__main__':
	FrenzyApp().run()





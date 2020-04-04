import json
import time

from GUI import UserInterface
from rgb_handler import RGB

class Main:
	def __init__(self):
		self.config_path = "./config.json"
		self.config = self.load_config()
		self.RGB = RGB(self)
		self.GUI = UserInterface(self)

		self.com_frequency = 60		# Hz

		self.GUI.root.mainloop()

	def com_loop(self):
		self.GUI.root.after(int(1000/self.com_frequency), self.com_loop)
		if self.RGB.animation_active:
			self.RGB.animation_rgb_t()

	def load_config(self):
		with open(self.config_path, "r") as f:
			return json.load(f)

	def save_config(self):
		pass


if __name__ == "__main__":
	App = Main()
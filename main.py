import json
import time

from GUI import UserInterface
from rgb_handler import RGB
from wc_handler import WC
from arduino_com import Arduino

class Main:
	def __init__(self):
		self.config_path = "./config.json"
		self.config = self.load_config()
		self.Arduino = Arduino(self)
		self.RGB = RGB(self)
		self.WC = WC(self)
		self.GUI = UserInterface(self)

		self.srl = self.Arduino.open_com_port()

		self.Arduino.fill_values_to_send()
		print(self.Arduino.values_to_send)

		self.com_frequency = 120		# Hz

		self.GUI.root.after(10, self.com_loop)

		self.GUI.root.mainloop()

	def com_loop(self):
		self.GUI.root.after(int(1000/self.com_frequency), self.com_loop)
		if self.RGB.animation_active:
			self.RGB.animation_set_rgb()
			self.GUI.rgb_handle_animation()

		self.Arduino.send()

	def load_config(self):
		with open(self.config_path, "r") as f:
			return json.load(f)

	def save_config(self):
		pass


if __name__ == "__main__":
	App = Main()
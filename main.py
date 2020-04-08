import json
import time
import datetime

from GUI import UserInterface
from rgb_handler import RGB
from wc_handler import WC
from shutter_handler import Shutter
from arduino_com import Arduino

class Main:
	def __init__(self):
		self.config_path = "./config.json"
		self.config = self.load_config()
		self.Arduino = Arduino(self)
		self.RGB = RGB(self)
		self.WC = WC(self)
		self.Shutter = Shutter(self)

		self.Arduino.srl = self.Arduino.open_com_port()
		print(str(self.Arduino.srl.read(self.Arduino.srl.in_waiting), encoding="ascii"))

		self.GUI = UserInterface(self)


		self.Arduino.fill_values_to_send()
		print(self.Arduino.values_to_send)

		self.com_frequency = 150		# Hz

		self.GUI.root.after(10, self.com_loop)
		self.GUI.after(10, self.second_loop)

		self.GUI.root.mainloop()

	def com_loop(self):
		self.GUI.root.after(int(1000/self.com_frequency), self.com_loop)
		if self.RGB.animation_active:
			self.RGB.animation_set_rgb()
			self.GUI.rgb_handle_animation()

		self.Arduino.send()

	def second_loop(self):
		self.GUI.after(int(datetime.datetime.now().microsecond/1000), self.second_loop)

		self.GUI.TopBar_lblClock.config(text=datetime.datetime.now().strftime("%H:%M"))

		if time.time() > self.GUI.last_unblank + self.GUI.blank_time_intervall:
			self.GUI.blank_screen()

	def load_config(self):
		with open(self.config_path, "r") as f:
			return json.load(f)

	def save_config(self):
		pass

	def close(self):
		# Set Mask
		self.Arduino.reset_values()

		self.GUI.root.destroy()


if __name__ == "__main__":
	App = Main()
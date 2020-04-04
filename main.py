from GUI import UserInterface
from rgb_handler import RGB

class Main:
	def __init__(self):
		self.RGB = RGB(self)
		self.GUI = UserInterface(self)

		self.GUI.root.mainloop()

	def load_config(self):
		pass

	def save_config(self):
		pass


if __name__ == "__main__":
	App = Main()
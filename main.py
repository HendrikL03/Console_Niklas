from GUI import UserInterface


class Main:
	def __init__(self):
		self.GUI = UserInterface(self)

		self.GUI.root.mainloop()

	def load_config(self):
		pass

	def save_config(self):
		pass


if __name__ == "__main__":
	App = Main()
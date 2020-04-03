import numpy as np


class RGB:
	rgbm_values = np.array([  # first column: RGB1, second column: RGB2
		[0, 0],
		[0, 0],
		[0, 0],
		[0, 0]
	])  # access via rgbm_values[:3, column]

	relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1
	btn_relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1

	def __init__(self, mainInst):
		self.mainInst = mainInst

	def set_relay_values(self):
		self.relay_values[0], self.relay_values[2] = (np.any((self.rgbm_values[:3, 0] * self.rgbm_values[3][0] > 0)),)*2
		self.relay_values[1] = np.any((self.rgbm_values[:3, 1] * self.rgbm_values[3][1] > 0))


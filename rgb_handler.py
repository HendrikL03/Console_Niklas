import numpy as np

class RGB:
	rgbm_values = np.array([  # first column: RGB1, second column: RGB2
		[0, 0],
		[0, 0],
		[0, 0],
		[0, 0]
	], dtype=np.int)  # access via rgbm_values[:3, column]

	relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1
	btn_relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1

	def __init__(self, mainInst):
		self.mainInst = mainInst

	def set_relay_values(self):
		self.relay_values[0], self.relay_values[2] = (np.any((self.rgbm_values[:3, 0] * self.rgbm_values[3][0]/255 > 0)),)*2
		self.relay_values[1] = np.any((self.rgbm_values[:3, 1] * self.rgbm_values[3][1]/255 > 0))

	### GUI Events ###
	def scl_event(self, idx, value, mask):
		"""
		:param idx: 0-red, 1-green, 2-blue, 3-master
		:param value: value of scale
		:param mask: rgb-channel mask [bool, bool]
		:return: None
		"""
		self.rgbm_values[idx, mask] = value

		self.set_relay_values()

		# TODO Send values to arduino

	def btn_channel_selection(self, idx):
		copy_from = self.rgbm_values[:, idx]
		if idx == 0:
			self.rgbm_values[:, 1] = copy_from
		elif idx == 1:
			self.rgbm_values[:, 0] = copy_from


	def btn_relays_event(self, idx):
		self.btn_relay_values[idx] = not self.btn_relay_values[idx]

	### Utils ###
	def get_rgbm_from_channel(self, idx):
		return self.rgbm_values[:, idx]
		pass
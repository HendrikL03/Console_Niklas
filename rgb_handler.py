import numpy as np
import time

class RGB:

	def __init__(self, mainInst):
		self.mainInst = mainInst
		self.GUI_config = mainInst.config["RGB"]

		# Initialize RGB Values and Relaybools
		self.rgbm_values = np.zeros((4, 2), dtype=np.uint)  # access via rgbm_values[:3, column]
		self.relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1
		self.btn_relay_values = np.array([False, False, False])  # RGB1, RGB2, RGB1
		self.gui_selected_channels = [True, True]

		# Animation
		self.animation_active = False
		self.animation_data = None
		self.animation_time = -1

	def set_relay_values(self):
		self.relay_values[0], self.relay_values[2] = (np.any((self.rgbm_values[:3, 0] * self.rgbm_values[3][0]/255 > 0)),)*2
		self.relay_values[1] = np.any((self.rgbm_values[:3, 1] * self.rgbm_values[3][1]/255 > 0))

	### GUI Events ###
	def scl_event(self, idx, value):
		"""
		:param idx: 0-red, 1-green, 2-blue, 3-master
		:param value: value of scale
		:param mask: rgb-channel mask [bool, bool]
		:return: None
		"""
		self.rgbm_values[idx, self.gui_selected_channels] = value

		self.set_relay_values()

		# TODO Send values to arduino

	def btn_channel_selection(self, channels, idx=None):
		"""
		:param channels: list of two booleans, True if RGB channel is selected
		:param idx: previously selected RGB channels
		:return:
		"""
		self.gui_selected_channels = channels
		if channels == [True, True]:
			# Copy RGB values if Both Channels are selected
			copy_from = self.rgbm_values[:, idx]
			if idx == 0:
				self.rgbm_values[:, 1] = copy_from
			elif idx == 1:
				self.rgbm_values[:, 0] = copy_from


	def btn_relays_event(self, idx):
		self.btn_relay_values[idx] = not self.btn_relay_values[idx]

	### Animations ###
	def animation_set_rgb(self):
		"""
		:param t: time from time.time()
		:return:
		"""
		if self.animation_data is None:
			return
		data = self.animation_data["data"]
		if t > max(data[:, 3]) and not self.animation_data["loop"]:
			# If there are no more Keycolors and the Preset does not loop, reset animation related things to default
			self.animation_active = False
			self.animation_data = None
			self.animation_time = -1
		if t >= max(data[:, 3]) and self.animation_data["loop"]:
			# If there are no more Keycolors but the Preset loops, reset animation_time
			self.animation_time = time.time()

		t = time.time()
		idx = 0
		for i, d in enumerate(self.animation_data):
			if d[3] > t - self.animation_time:
				idx = i
				break

		timebase = data[idx - 1][3]
		delta = data[idx] - data[idx - 1]

		rgb = (t - timebase) / delta[3] * delta[:3] + data[idx - 1][:3]
		rgb = np.round(rgb).astype(np.uint)

		# Set values
		for idx, selected in enumerate(self.gui_selected_channels):
			if selected:
				self.rgbm_values[:, idx] = np.concatenate((rgb, [255]))


	### Utils ###
	def get_rgbm_from_channel(self):
		idx = self.gui_selected_channels.index(True)
		return self.rgbm_values[:, idx]
		pass
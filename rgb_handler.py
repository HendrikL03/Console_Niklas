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

		# Presets
		self.preset_type = "Presets"	# 0: static, 1: animation
		# Animation
		self.animation_active = False
		self.animation_data = None		# Contains whole Animation Preset with name, data and loop bool
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

	def switch_preset_type(self):
		self.preset_type = "Animations" if self.preset_type == "Presets" else "Presets"

	def select_preset(self, idx):
		preset = self.GUI_config[self.preset_type][idx]
		if self.preset_type == "Presets":
			if self.gui_selected_channels[0]:
				self.rgbm_values[:, 0] = preset["data"]
			if self.gui_selected_channels[1]:
				self.rgbm_values[:, 1] = preset["data"]

		elif self.preset_type == "Animations":
			if self.gui_selected_channels[0]:
				self.rgbm_values[:, 0] = preset["data"][0]
			if self.gui_selected_channels[1]:
				self.rgbm_values[:, 1] = preset["data"][0]

			self.animation_data = preset

		self.set_relay_values()
		# TODO Send Values to ARduino
		pass

	### Animations ###
	def animation_set_rgb(self):
		"""
		:return: None
		negative timevalues indicate, that the related color shall be set without transition, therefore abs(data[3]) is
		needed sometimes
		"""
		if self.animation_data is None:
			return
		data = np.array(self.animation_data["data"])
		t = time.time()
		if t > max(data[:, 3])+self.animation_time and not self.animation_data["loop"]:
			# If there are no more Keycolors and the Preset does not loop, reset animation related things to default
			self.animation_active = False
			self.animation_data = None
			self.animation_time = -1
			return
		if (t-self.animation_time) >= max(abs(data[:, 3])) and self.animation_data["loop"]:
			# If there are no more Keycolors but the Preset loops, reset animation_time
			print("reset animation time")
			self.animation_time = time.time()

		t = time.time()
		rel_t = t - self.animation_time
		idx = 0
		for i, d in enumerate(data):
			if abs(d[3])> rel_t:
				idx = i
				break

		timebase = data[idx - 1][3]
		if timebase >= 0:
			delta = data[idx] - data[idx - 1]
			delta[3] = abs(delta[3])

			rgb = data[idx-1][:3] + (rel_t - abs(data[idx-1][3]))/delta[3] * delta[:3] #(t - abs(timebase)) / abs(delta[3]) * delta[:3] + data[idx - 1][:3]
			rgb = np.round(rgb).astype(np.uint)
		else:
			rgb = data[idx-1][:3]

		# Set values
		for idx, selected in enumerate(self.gui_selected_channels):
			if selected:
				self.rgbm_values[:, idx] = np.concatenate((rgb, [255]))

	def animation_start(self):
		if self.animation_time == -1:
			self.animation_time = time.time()
		self.animation_active = True

	def animation_stop(self, reset = False):
		self.animation_active = False
		if reset:
			self.animation_time = -1
			self.animation_data = None

	### Utils ###
	def get_rgbm_from_channel(self):
		idx = self.gui_selected_channels.index(True)
		return self.rgbm_values[:, idx]
		pass
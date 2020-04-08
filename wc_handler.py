import numpy as np

class WC:
	# WC: WarmCold white
	def __init__(self, mainInst):
		self.mainInst = mainInst
		self.WC_config = mainInst.config["WC"]

		self.wcm_values = np.array([255, 255, 0])
		self.relay_value = False
		self.btn_relay_value = False

		# Animation
		self.animation_active = False
		self.animation_data = None		# Contains whole Animation Preset with name, data and loop bool
		self.animation_time = -1
		self.animation_pause_time = -1

	def set_relay_value(self):
		self.relay_value = np.any((self.wcm_values[:2] * self.wcm_values[2]/255 > 0))

	def relay_btn(self):
		self.btn_relay_value = not self.btn_relay_value
		self.set_arduino_mask()

	def balance_to_values(self, balance):
		self.wcm_values[0] = 255 + balance if balance < 0 else 255
		self.wcm_values[1] = 255 - balance if balance > 0 else 255

		self.set_relay_value()
		self.set_arduino_mask()

	def brightness_to_value(self, brightness):
		self.wcm_values[2] = brightness

		self.set_relay_value()

		self.set_arduino_mask()

	### Animation ###
	def animation_set_wc(self):
		"""
		:return: None
		negative timevalues indicate, that the related color shall be set without transition, therefore abs(data[3]) is
		needed sometimes
		"""
		if self.animation_data is None:
			return
		data = np.array(self.animation_data["data"])
		t = time.time()
		if t > max(data[:, 2])+self.animation_time and not self.animation_data["loop"]:
			# If there are no more Keycolors and the Preset does not loop, reset animation related things to default
			self.animation_active = False
			self.animation_data = None
			self.animation_time = -1
			return
		if (t-self.animation_time) >= max(abs(data[:, 2])) and self.animation_data["loop"]:
			# If there are no more Keycolors but the Preset loops, reset animation_time
			self.animation_time = time.time()

		t = time.time()
		rel_t = t - self.animation_time
		idx = 0
		for i, d in enumerate(data):
			if abs(d[2])> rel_t:
				idx = i
				break

		timebase = data[idx - 1][2]
		if data[idx][2] >= 0:#timebase >= 0:
			delta = data[idx] - data[idx - 1]
			delta[2] = abs(delta[2])

			wc = data[idx-1][:2] + (rel_t - abs(data[idx-1][2]))/delta[2] * delta[:2] #(t - abs(timebase)) / abs(delta[3]) * delta[:3] + data[idx - 1][:3]
			#rgb = np.round(rgb).astype(np.uint)
		else:
			wc = data[idx-1][:2]

		# Set values
		self.wcm_values[:2] = wc

		self.set_relay_value()
		self.set_arduino_mask()

	def animation_start(self):
		if self.animation_time == -1:
			self.animation_time = time.time()
			self.animation_pause_time = -1
		elif self.animation_pause_time != -1:
			self.animation_time = time.time() - (self.animation_pause_time - self.animation_time)
			self.animation_pause_time = -1
		self.animation_active = True

	def animation_stop(self, reset = False):
		self.animation_active = False
		if reset:
			self.animation_time = -1
			self.animation_data = None
		else:
			self.animation_pause_time = time.time()


	### Utils ###
	def set_arduino_mask(self):
		idx_color = self.mainInst.Arduino.mask_idx_wc
		self.mainInst.Arduino.values_to_send_mask[idx_color: idx_color+2] = True

		idx_relay = self.mainInst.Arduino.mask_idx_wcrls
		self.mainInst.Arduino.values_to_send_mask[idx_relay: idx_relay+2] = True

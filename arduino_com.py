import numpy as np
import serial

# Values: r1, g1, b1, r2, g2, b2, w, c, rgbrls1, rgbrls2, rgbrls3, wcrls1, cwrls2, shutterup, shutterdown
# Total: 15

class Arduino:
	def __init__(self, mainInst):
		self.mainInst = mainInst
		self.values_to_send = np.zeros((15,))
		self.values_to_send_mask = np.full((15,), False)

		# Mask access
		self.mask_idx_rgb = 0
		self.mask_idx_wc = 6
		self.mask_idx_rgbrls = 8
		self.mask_idx_wcrls = 11
		self.mask_idx_shutter = 13

	def open_com_port(self, portname="/dev/ttyACM0", baudrate=115200):
		srl=None
		try:
			srl = serial.Serial(portname, baudrate, timeout=10)
		except serial.serialutil.SerialException as e:
			print(e)
			print("Wrong portname, probably on wrong machine?")
		except  serial.serialutil.Timeout as e:
			print(e)
			print("Serial timed out")

		if not isinstance(srl, serial.Serial):
			return None
		return srl

	def send(self):
		# Two Bytes Header: high bits encode, that this value shall be set
		if not True in self.values_to_send_mask:# or not isinstance(self.srl, serial.Serial):
			return

		self.fill_values_to_send()

		header = bytearray([0, 0])
		for i, bit in enumerate(self.values_to_send_mask):
			header[i//8] += 0x80*bit >> i%8

		data = self.values_to_send[self.values_to_send_mask].astype(np.uint8)

		# Send values
		if isinstance(self.srl, serial.Serial):
			self.srl.write(header + data)
		# print(self.values_to_send_mask, data)

		self.reset_mask()

	### Utils ###
	def fill_values_to_send(self):
		self.values_to_send[:3] = self.mainInst.RGB.rgbm_values[:3, 0] * self.mainInst.RGB.rgbm_values[3, 0]/255
		self.values_to_send[3:6] = self.mainInst.RGB.rgbm_values[:3, 1] * self.mainInst.RGB.rgbm_values[3, 0]/255
		self.values_to_send[6:8] = self.mainInst.WC.wcm_values[:2] * self.mainInst.WC.wcm_values[2]
		self.values_to_send[8:11] = (True^(self.mainInst.RGB.relay_values * self.mainInst.RGB.btn_relay_values))*255
		self.values_to_send[11:13] = ((True^(self.mainInst.WC.relay_value * self.mainInst.WC.btn_relay_value))*255,)*2
		self.values_to_send[13:15] = 255, 255

		# Apply function to color values
		self.values_to_send[:8] = self.color_exp_function(self.values_to_send[:8])

	def reset_mask(self):
		self.values_to_send_mask = np.full((15,), False)

	def reset_values(self):
		header = bytearray([0xff, 0xfe])
		data = bytearray([0x00]*8 + [0xff]*7)

		# Send
		if isinstance(self.srl, serial.Serial):
			self.srl.write(header + data)
		print(header, data)

	@staticmethod
	def color_exp_function(x: np.array):
		b = 255**(1/255)
		M = x>0
		x[M] = b**x[M]
		x = np.round(x)
		return x

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

		data = bytearray(self.values_to_send[self.values_to_send_mask].astype(np.uint8))

		# Send values
		# for b in (header + data):
		# 	print(bin(b), end="\t")
		# print("\n", header + data)
		# print(header + data)
		if isinstance(self.srl, serial.Serial):
			self.srl.write(header + data)

			# print(str(self.srl.read(self.srl.in_waiting), encoding="ascii"))

		self.reset_mask()

	### Utils ###
	def fill_values_to_send(self):
		rgbm_values = self.mainInst.RGB.rgbm_values
		rgb_bools = self.mainInst.RGB.relay_values * self.mainInst.RGB.btn_relay_values
		# Values * master * relay_bools
		self.values_to_send[:3] = rgbm_values[:3, 0] * rgbm_values[3, 0]/255 * (True in (rgb_bools[0], rgb_bools[2]))
		self.values_to_send[3:6] = rgbm_values[:3, 1] * rgbm_values[3, 1]/255 * rgb_bools[1]

		wcm_values = self.mainInst.WC.wcm_values
		wc_bool = self.mainInst.WC.relay_value * self.mainInst.WC.btn_relay_value
		self.values_to_send[6:8] = wcm_values[:2] * wcm_values[2]/255 * wc_bool

		self.values_to_send[8:11] = (True ^ rgb_bools) * 255
		self.values_to_send[11:13] = ((True ^ wc_bool) * 255,) * 2
		self.values_to_send[13:15] = self.mainInst.Shutter.relay_states

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
		print("reset:")
		for b in (header + data):
			print(bin(b), end="\t")
		print()

	@staticmethod
	def color_exp_function(x: np.array):
		k = 8
		b = 1.1156707339947467		# ((255+k-1)/k)**(k/255); 1.1156... für k=8

		M = x>0
		# print(x[M])
		x[M] = k * b**(x[M]/k) - k + 1
		x = np.round(x)
		return x

import tkinter as tk
import sys
from functools import partial

class UserInterface(tk.Frame):
	def __init__(self):
		self.root = tk.Tk()
		super().__init__(self.root)
		if sys.platform == "linux":
			self.root.attributes("-fullscreen", True)
			self.width, self.height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		else:
			self.config(width=800, height=480)
			self.grid_propagate(0)
			self.width, self.height = 800, 480
		self.root.bind("<Configure>", self.root_config_evt)
		self.root.bind("<Control-r>", self.reset_window_size)
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)
		print(self.winfo_width(), self.winfo_height())

		self.build()

		self.grid_config_UI()

		self.grid()


	def build(self):
		# Global configurations
		self.root.tk_setPalette(background="#323232",
								activeBackground="#323232",
								foreground="#c0c0c0",
								activeForeground="#c0c0c0",
								highlightBackground="#c0c0c0",
								troughColor="#323232")

		default_font = "Lato 14"
		self.rel_menu_height = 0.12
		self.rel_panel_height = 0.88

		# Base Frames

		self.FrameTopBar = tk.Frame(self)
		self.FrameMenu = tk.Frame(self)
		self.FrameHome = tk.Frame(self)
		self.FrameRGB = tk.Frame(self)
		self.FrameAlarms = tk.Frame(self)

		self.FrameTopBar.grid(row=0, column=0, pady=1, padx=1, sticky=tk.NSEW)
		self.FrameHome.grid(row=1, column=0, pady=1, padx=1, sticky=tk.NSEW)


		###################################################################################################
		# TOP BAR
		###################################################################################################
		self.FrameTopBar.config(highlightthickness=1)

		self.TopBar_btnMenu = tk.Button(self.FrameTopBar, text="menu", highlightthickness=1, relief=tk.FLAT,
										command=self.TopBar_btnMenu_event)
		self.TopBar_lblClock = tk.Label(self.FrameTopBar, text="00:00", font=default_font)
		self.TopBar_btnDpb = tk.Button(self.FrameTopBar, text="dpb", highlightthickness=1, relief=tk.FLAT,
									   command=self.TopBar_btnDpb_event)

		self.TopBar_btnMenu.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.TopBar_lblClock.grid(row=0, column=1, sticky=tk.NSEW)
		self.TopBar_btnDpb.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NSEW)

		###################################################################################################
		# MENU FRAME
		###################################################################################################
		self.FrameMenu.config(highlightthickness=1)

		self.Menu_btnHome = tk.Button(self.FrameMenu, text="Home", font=default_font,
									  highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnRGB = tk.Button(self.FrameMenu, text="RGB", font=default_font,
									  highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnAlarms = tk.Button(self.FrameMenu, text="Wecker", font=default_font,
									  highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnClose = tk.Button(self.FrameMenu, text="Schließen", font=default_font, compound=tk.RIGHT,
									  highlightthickness=1, relief=tk.FLAT)

		self.Menu_btnHome.grid(row=0, sticky=tk.NSEW)
		self.Menu_btnRGB.grid(row=1, sticky=tk.NSEW)
		self.Menu_btnAlarms.grid(row=2, sticky=tk.NSEW)
		self.Menu_btnClose.grid(row=3, sticky=tk.S + tk.EW)

		###################################################################################################
		# HOME FRAME
		###################################################################################################
		# WC Frame takes one half
		self.FrameHome.config(bg="#191919", highlightthickness=1)

		self.fHomeShutter = tk.Frame(self.FrameHome)
		self.fHomeRGB = tk.Frame(self.FrameHome)
		self.fHomeWC = tk.Frame(self.FrameHome)

		# Shutter
		self.sclShutterVar = tk.IntVar()
		self.Home_sclShutter = tk.Scale(self.fHomeShutter, from_=100, to=0, width=45, borderwidth=3, sliderlength=50,
										variable=self.sclShutterVar)
		self.Home_btnSetShutter = tk.Button(self.fHomeShutter, text="Set", font=default_font,
											highlightthickness=1, relief=tk.FLAT)
		self.Home_btnShutterUp = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT)
		self.Home_btnShutterStop = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT)
		self.Home_btnShutterDown = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT)

		self.Home_btnSetShutter.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)
		self.Home_sclShutter.grid(row=0, rowspan=3, column=0, sticky=tk.NSEW)
		self.Home_btnShutterDown.grid(row=0, column=1, sticky=tk.NSEW)
		self.Home_btnShutterStop.grid(row=1, column=1, sticky=tk.NSEW)
		self.Home_btnShutterUp.grid(row=2, column=1, sticky=tk.NSEW)

		# RGB
		self.Home_btnRGBChannel1 = tk.Button(self.fHomeRGB, highlightthickness=1, relief=tk.FLAT,
											 command=partial(self.Home_btnRGB_event, 0))
		self.Home_btnRGBChannel2 = tk.Button(self.fHomeRGB, highlightthickness=1, relief=tk.FLAT,
											 command=partial(self.Home_btnRGB_event, 1))
		self.Home_btnRGBChannel3 = tk.Button(self.fHomeRGB, highlightthickness=1, relief=tk.FLAT,
											 command=partial(self.Home_btnRGB_event, 2))

		self.Home_btnRGBChannel1.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_btnRGBChannel2.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_btnRGBChannel3.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NSEW)

		# WC
		self.sclWCBrightnessVar, self.sclWCBalanceVar = tk.IntVar(), tk.IntVar()
		self.Home_btnWC = tk.Button(self.fHomeWC, relief=tk.FLAT)
		self.Home_sclWCBrightness = tk.Scale(self.fHomeWC, from_=255, to=0, width=45, borderwidth=3, sliderlength=50,
											 variable=self.sclWCBrightnessVar, command=self.Home_sclBrightness_event)
		self.Home_sclWCBalance = tk.Scale(self.fHomeWC, from_=-255, to=255, width=45, borderwidth=3, sliderlength=50,
										  orient=tk.HORIZONTAL, variable=self.sclWCBalanceVar,
										  command=self.Home_sclBalance_event)

		self.Home_btnWC.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_sclWCBrightness.grid(row=0, rowspan=2, column=1, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_sclWCBalance.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)

		# Grid Part frames
		self.fHomeShutter.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
		self.fHomeRGB.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)
		self.fHomeWC.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)


	# Top Bar Events
	def TopBar_btnDpb_event(self):
		pass

	def TopBar_btnMenu_event(self):
		if self.FrameMenu.grid_info() != {}:
			self.FrameMenu.grid_forget()
		else:
			self.FrameMenu.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NS + tk.W)
			self.FrameMenu.lift()

	# Home Frame Events
	def Home_btnSetShutter_event(self):
		pass

	def Home_btnShutterUp_event(self):
		pass

	def Home_btnShutterStop_event(self):
		pass

	def Home_btnShutterDown_event(self):
		pass

	def Home_btnRGB_event(self, idx):
		pass

	def Home_btnWC_event(self):
		pass

	def Home_sclBrightness_event(self, evt):
		pass

	def Home_sclBalance_event(self, evt):
		pass

	def root_config_evt(self, evt):
		if isinstance(evt.widget, tk.Tk) and (evt.width != self.width or evt.height != self.height):
			self.width, self.height = evt.width, evt.height
			self.grid_config_UI()

	def reset_window_size(self, evt):
		self.width, self.height = 800, 480
		self.root.geometry("{}x{}".format(self.width, self.height))
		self.grid_config_UI()

	def grid_config_UI(self):
		self.config(width=self.width, height=self.height)

		# BaseFrame
		self.grid_rowconfigure(0, weight=1, minsize=int(self.height * self.rel_menu_height))
		self.grid_rowconfigure(1, weight=2, minsize=int(self.height * self.rel_panel_height))
		self.grid_columnconfigure(0, weight=2, minsize=self.width)

		# FrameTopBar
		self.FrameTopBar.columnconfigure(0, weight=0, minsize=int(self.height * self.rel_menu_height))
		self.FrameTopBar.columnconfigure(1, weight=1)
		self.FrameTopBar.columnconfigure(2, weight=0, minsize=int(self.height * self.rel_menu_height))
		self.FrameTopBar.rowconfigure(0, weight=1)

		### Menu ###
		self.FrameMenu.grid_rowconfigure(0, weight=0)
		self.FrameMenu.grid_rowconfigure(1, weight=0)
		self.FrameMenu.grid_rowconfigure(2, weight=0)
		self.FrameMenu.grid_rowconfigure(3, weight=1)
		self.FrameMenu.grid_columnconfigure(0, minsize=int(self.width*0.3))

		### Home ###
		self.FrameHome.grid_rowconfigure(0, weight=1)
		self.FrameHome.grid_columnconfigure(0, weight=2)
		self.FrameHome.grid_columnconfigure(1, weight=2)
		self.FrameHome.grid_columnconfigure(2, weight=2)
		self.fHomeWC.config(width=int(self.height * 0.5))

		# Shutter
		self.fHomeShutter.grid_rowconfigure(0, weight=1)
		self.fHomeShutter.grid_rowconfigure(1, weight=1)
		self.fHomeShutter.grid_rowconfigure(2, weight=1)
		self.fHomeShutter.grid_rowconfigure(3, weight=1)
		self.fHomeShutter.grid_columnconfigure(0, weight=0)	# Scale does not expand when possible
		self.fHomeShutter.grid_columnconfigure(1, weight=2)

		# RGB
		self.fHomeRGB.grid_rowconfigure(0, weight=1)
		self.fHomeRGB.grid_rowconfigure(1, weight=1)
		self.fHomeRGB.grid_rowconfigure(2, weight=1)
		self.fHomeRGB.grid_columnconfigure(0, weight=1)

		# WC
		self.fHomeWC.grid_columnconfigure(0, minsize=int(self.fHomeWC.cget("width")*0.75), weight=1)
		self.fHomeWC.grid_rowconfigure(0, minsize=int(self.fHomeWC.cget("width")*0.75), weight=1)




if __name__ == "__main__":
	UI = UserInterface()
	UI.root.mainloop()
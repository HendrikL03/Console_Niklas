import tkinter as tk
import sys
from functools import partial
import time
# from tkinter.messagebox import askquestion


class UserInterface(tk.Frame):
	def __init__(self, mainInst):
		self.mainInst = mainInst

		self.root = tk.Tk()
		super().__init__(self.root)
		if sys.platform == "linux":
			self.root.attributes("-fullscreen", True)
			self.root.config(cursor=tk.NONE)
			self.width, self.height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		else:
			self.config(width=800, height=480)
			self.grid_propagate(0)
			self.width, self.height = 800, 480
		self.root.bind("<Configure>", self.root_config_evt)
		self.root.bind("<Control-r>", self.reset_window_size)
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		# Build GUI
		self.load_pictures()
		self.build()
		self.grid_config_UI()

		# Setup other things
		self.rgb_fill_listbox()
		self.blank_time_intervall = 30
		self.last_unblank = time.time()

		self.grid()

	def build(self):
		# Global configurations
		self.palette = {
			"background": "#323232",
			"activeBackground": "#323232",
			"foreground": "#c0c0c0",
			"activeForeground": "#c0c0c0",
			"highlightBackground": "#c0c0c0",
			"troughColor": "#323232"
		}
		self.root.tk_setPalette(background=self.palette["background"],
								activeBackground=self.palette["activeBackground"],
								foreground=self.palette["foreground"],
								activeForeground=self.palette["activeForeground"],
								highlightBackground=self.palette["highlightBackground"],
								troughColor=self.palette["troughColor"])
		fonts = {
			"default": "Lato 14",
			"clock": "Lato 32",
			"menu": "Lato 18",
			"rgb": "Lato 14",
			"rgb_scales": "Century 12 bold",
			"presets_font": "Century 20 italic"
		}

		default_font = "Lato 14"
		self.rel_menu_height = 0.12
		self.rel_panel_height = 0.88

		# Base Frames

		self.FrameTopBar = tk.Frame(self)
		self.FrameMenu = tk.Frame(self)
		self.FrameHome = tk.Frame(self)
		self.FrameRGB = tk.Frame(self)
		self.FrameAlarms = tk.Frame(self)
		self.FrameBlank = tk.Frame(self, bg="black")
		self.FrameBlank.bind("<Button-1>", self.unblank_screen)

		self.FrameTopBar.grid(row=0, column=0, pady=1, padx=1, sticky=tk.NSEW)
		self.FrameHome.grid(row=1, column=0, pady=1, padx=1, sticky=tk.NSEW)
		self.displayed_frame = self.FrameHome

		###################################################################################################
		# TOP BAR
		###################################################################################################
		self.FrameTopBar.config(highlightthickness=1)

		self.TopBar_btnMenu = tk.Button(self.FrameTopBar, text="menu", highlightthickness=1, relief=tk.FLAT,
										image=self.btn_pictures["MenuSymbol"])
		self.TopBar_lblClock = tk.Label(self.FrameTopBar, text="00:00", font=fonts["clock"])
		self.TopBar_btnDpb = tk.Button(self.FrameTopBar, text="dpb", highlightthickness=1, relief=tk.FLAT,
									   image=self.btn_pictures["DpbSymbol"])

		self.TopBar_btnMenu.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.TopBar_lblClock.grid(row=0, column=1, sticky=tk.NSEW)
		self.TopBar_btnDpb.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NSEW)

		# Commands
		self.TopBar_btnMenu.config(command=self.topBar_btnMenu_event)
		self.TopBar_btnDpb.config(command=self.topBar_btnDpb_event)

		###################################################################################################
		# MENU FRAME
		###################################################################################################
		self.FrameMenu.config(highlightthickness=1)

		self.Menu_btnHome = tk.Button(self.FrameMenu, text="Home", font=fonts["menu"],
									  highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnRGB = tk.Button(self.FrameMenu, text="RGB", font=fonts["menu"],
									 highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnAlarms = tk.Button(self.FrameMenu, text="Wecker", font=fonts["menu"],
										highlightthickness=1, relief=tk.FLAT)
		self.Menu_btnClose = tk.Button(self.FrameMenu, text="Schließen", font=fonts["menu"], justify=tk.RIGHT,
									   highlightthickness=1, relief=tk.FLAT)

		self.Menu_btnHome.grid(row=0, padx=2, pady=2, sticky=tk.NSEW)
		self.Menu_btnRGB.grid(row=1, padx=2, pady=2, sticky=tk.NSEW)
		self.Menu_btnAlarms.grid(row=2, padx=2, pady=2, sticky=tk.NSEW)
		self.Menu_btnClose.grid(row=3, padx=2, pady=2, sticky=tk.S + tk.EW)

		# Commands
		self.Menu_btnHome.config(command=partial(self.menu_DisplayFrame_event, self.FrameHome))
		self.Menu_btnRGB.config(command=partial(self.menu_DisplayFrame_event, self.FrameRGB))
		self.Menu_btnAlarms.config(command=partial(self.menu_DisplayFrame_event, self.FrameAlarms))
		self.Menu_btnClose.config(command=self.mainInst.close)

		###################################################################################################
		# HOME FRAME
		###################################################################################################
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
		self.Home_btnShutterUp = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT,
										   image=self.btn_pictures["ShutterUp"])
		self.Home_btnShutterStop = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT,
											 image=self.btn_pictures["ShutterStop"])
		self.Home_btnShutterDown = tk.Button(self.fHomeShutter, highlightthickness=1, relief=tk.FLAT,
											 image=self.btn_pictures["ShutterDown"])

		self.Home_btnSetShutter.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)
		self.Home_sclShutter.grid(row=0, rowspan=3, column=0, sticky=tk.NSEW)
		self.Home_btnShutterUp.grid(row=0, column=1, sticky=tk.NSEW)
		self.Home_btnShutterStop.grid(row=1, column=1, sticky=tk.NSEW)
		self.Home_btnShutterDown.grid(row=2, column=1, sticky=tk.NSEW)
		# RGB
		self.Home_btnRGBRelayChannels = []
		for i in range(3):
			self.Home_btnRGBRelayChannels.append( tk.Button(self.fHomeRGB, highlightthickness=1, relief=tk.FLAT,
															image=self.btn_pictures["RGBOff"]))

			self.Home_btnRGBRelayChannels[-1].grid(row=i, column=0, padx=1, pady=1, sticky=tk.NSEW)

		# WC
		self.sclWCBrightnessVar, self.sclWCBalanceVar = tk.IntVar(), tk.IntVar()
		self.Home_btnWC = tk.Button(self.fHomeWC, relief=tk.FLAT, image=self.btn_pictures["WCOff"])
		self.Home_sclWCBrightness = tk.Scale(self.fHomeWC, from_=255, to=0, width=45, borderwidth=3, sliderlength=50,
											 variable=self.sclWCBrightnessVar, command=self.home_sclBrightness_event)
		self.Home_sclWCBalance = tk.Scale(self.fHomeWC, from_=-255, to=255, width=45, borderwidth=3, sliderlength=50,
										  orient=tk.HORIZONTAL, variable=self.sclWCBalanceVar)

		self.Home_btnWC.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_sclWCBrightness.grid(row=0, rowspan=2, column=1, padx=1, pady=1, sticky=tk.NSEW)
		self.Home_sclWCBalance.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)

		# Grid Part frames
		self.fHomeShutter.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
		self.fHomeRGB.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)
		self.fHomeWC.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)

		# Commands
		self.Home_btnShutterUp.config(command=self.home_btnShutterUp_event)
		self.Home_btnShutterStop.config(command=self.home_btnShutterStop_event)
		self.Home_btnShutterDown.config(command=self.home_btnShutterDown_event)
		for i in range(3):
			self.Home_btnRGBRelayChannels[i].config(command = partial(self.home_btnRGB_event, i))
		self.Home_sclWCBalance.config(command=self.home_sclBalance_event)
		self.Home_sclWCBrightness.config(command=self.home_sclBrightness_event)
		self.Home_btnWC.config(command=self.home_btnWC_event)

		###################################################################################################
		# RGB FRAME
		###################################################################################################
		self.FrameRGB.config(highlightthickness=1)
		self.selected_RGB_channel_palette = {
			"bg": self.palette["foreground"],
			"activebackground": self.palette["activeForeground"],
			"fg": self.palette["background"],
			"activeforeground": self.palette["activeBackground"]
		}
		# Channel Selection Buttons
		self.RGB_btnChannelBoth = tk.Button(self.FrameRGB, text="Kanal 1+2", relief=tk.FLAT,
											font=fonts["rgb"], highlightthickness=1,
											cnf=self.selected_RGB_channel_palette)
		self.RGB_btnChannelOne = tk.Button(self.FrameRGB, text="Kanal 1", font=fonts["rgb"],
										   relief=tk.FLAT, highlightthickness=1)
		self.RGB_btnChannelTwo = tk.Button(self.FrameRGB, text="Kanal 2", font=fonts["rgb"],
										   relief=tk.FLAT, highlightthickness=1)

		# Scales
		self.RGB_scalesVars = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

		self.RGB_sclRed = tk.Scale(self.FrameRGB, font=fonts["rgb_scales"], variable=self.RGB_scalesVars[0],
								   borderwidth=3, width=45, from_=255, to=0, sliderlength=50,
								   highlightthickness=0, bg="red", activebackground="red", troughcolor="red",
								   fg="white")
		self.RGB_sclGreen = tk.Scale(self.FrameRGB,  font=fonts["rgb_scales"], variable=self.RGB_scalesVars[1],
									 borderwidth=3, width=45, from_=255, to=0, sliderlength=50,
									 highlightthickness=0, bg="green", activebackground="green", troughcolor="green",
									 fg="black")
		self.RGB_sclBlue = tk.Scale(self.FrameRGB, font=fonts["rgb_scales"], variable=self.RGB_scalesVars[2],
									borderwidth=3, width=45, from_=255, to=0, sliderlength=50,
									highlightthickness=0, bg="blue", activebackground="blue", troughcolor="blue",
									fg="white")
		self.RGB_sclMaster = tk.Scale(self.FrameRGB, bg="black", font=fonts["rgb_scales"],
									  variable=self.RGB_scalesVars[3], borderwidth=3, width=45, from_=255, to=0,
									  sliderlength=50, troughcolor="black", highlightthickness=0,
									  fg="white")

		# Presets
		self.RGB_btnPresetType = tk.Button(self.FrameRGB, text="Farbe", font=fonts["rgb"], relief=tk.FLAT,
										   highlightthickness=1)
		self.RGB_scbPresets = tk.Scrollbar(self.FrameRGB, width=20, highlightthickness=0)
		self.RGB_lbxPresets = tk.Listbox(self.FrameRGB, font=fonts["presets_font"],
										 selectborderwidth=4, activestyle=tk.NONE, highlightthickness=0,
										 yscrollcommand=self.RGB_scbPresets.set)
		self.RGB_scbPresets.config(command=self.RGB_lbxPresets.yview)

		self.fRGBPresetBtns = tk.Frame(self.FrameRGB)
		self.RGB_btnSelect = tk.Button(self.fRGBPresetBtns, text="Auswählen", font=fonts["rgb"],
									   relief=tk.FLAT, highlightthickness=1)
		self.RGB_btnAdd = tk.Button(self.fRGBPresetBtns, text="Hinzufügen", font=fonts["rgb"],
									relief=tk.FLAT, highlightthickness=1)
		self.RGB_btnDelete = tk.Button(self.fRGBPresetBtns, text="Löschen", font=fonts["rgb"],
									   relief=tk.FLAT, highlightthickness=1)
		self.RGB_btnStart = tk.Button(self.fRGBPresetBtns, text="Start", font=fonts["rgb"], state=tk.DISABLED,
									  relief=tk.FLAT, highlightthickness=1)
		self.RGB_btnStop = tk.Button(self.fRGBPresetBtns, text="Stop", font=fonts["rgb"], state=tk.DISABLED,
									 relief=tk.FLAT, highlightthickness=1)

		# Grid
		self.RGB_btnChannelBoth.grid(row=0, column=0, sticky=tk.NSEW)
		self.RGB_btnChannelOne.grid(row=0, column=1, sticky=tk.NSEW)
		self.RGB_btnChannelTwo.grid(row=0, column=2, sticky=tk.NSEW)
		self.RGB_sclRed.grid(row=1, column=0, sticky=tk.NSEW)
		self.RGB_sclGreen.grid(row=1, column=1, sticky=tk.NSEW)
		self.RGB_sclBlue.grid(row=1, column=2, sticky=tk.NSEW)
		self.RGB_sclMaster.grid(row=1, column=3, sticky=tk.NSEW)

		self.RGB_btnPresetType.grid(row=0, column=5, sticky=tk.NSEW)
		self.RGB_lbxPresets.grid(row=1, column=5, sticky=tk.NSEW)
		self.RGB_scbPresets.grid(row=1, column=5, sticky=tk.NS + tk.E); self.RGB_scbPresets.lift()

		self.RGB_btnSelect.grid(row=0, pady=1, sticky=tk.NSEW)
		self.RGB_btnAdd.grid(row=1, pady=1, sticky=tk.NSEW)
		self.RGB_btnDelete.grid(row=2, pady=1, sticky=tk.EW)
		self.RGB_btnStart.grid(row=3, pady=1, sticky=tk.NSEW)
		self.RGB_btnStop.grid(row=4, pady=1, sticky=tk.NSEW)

		self.fRGBPresetBtns.grid(row=1, column=6, padx=5, sticky=tk.NSEW)

		# Commands
		self.RGB_btnChannelBoth.config(command=partial(self.rgb_btnChannelSelection_event, [True, True]))
		self.RGB_btnChannelOne.config(command=partial(self.rgb_btnChannelSelection_event, [True, False]))
		self.RGB_btnChannelTwo.config(command=partial(self.rgb_btnChannelSelection_event, [False, True]))

		self.RGB_sclRed.config(command=partial(self.rgb_scales_event, 0))
		self.RGB_sclGreen.config(command=partial(self.rgb_scales_event, 1))
		self.RGB_sclBlue.config(command=partial(self.rgb_scales_event, 2))
		self.RGB_sclMaster.config(command=partial(self.rgb_scales_event, 3))

		self.RGB_btnPresetType.config(command=self.rgb_btnPresetType_event)
		self.RGB_btnSelect.config(command=self.rgb_btnPresetSelect_event)
		self.RGB_btnAdd.config(command=self.rgb_btnPresetAdd_event)
		self.RGB_btnDelete.config(command=self.rgb_btnPresetDelete_event)
		self.RGB_btnStart.config(command=self.rgb_btnPresetStart_event)
		self.RGB_btnStop.config(command=self.rgb_btnPresetStop_event)

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

		### BaseFrame
		self.grid_rowconfigure(0, weight=1, minsize=int(self.height * self.rel_menu_height))
		self.grid_rowconfigure(1, weight=2, minsize=int(self.height * self.rel_panel_height))
		self.grid_columnconfigure(0, weight=2, minsize=self.width)

		### FrameTopBar
		self.FrameTopBar.columnconfigure(0, weight=0, minsize=int(self.height * self.rel_menu_height))
		self.FrameTopBar.columnconfigure(1, weight=1)
		self.FrameTopBar.columnconfigure(2, weight=0, minsize=int(self.height * self.rel_menu_height))
		self.FrameTopBar.rowconfigure(0, weight=1)

		### Menu ###
		self.FrameMenu.grid_rowconfigure(3, weight=1)
		self.FrameMenu.grid_columnconfigure(0, minsize=int(self.width * 0.3))

		### Home ###
		self.FrameHome.config(width=self.width, height=int(self.height * self.rel_panel_height))

		self.FrameHome.grid_rowconfigure(0, weight=1)
		self.FrameHome.grid_columnconfigure(0, weight=1)
		self.fHomeWC.config(width=int(self.FrameHome.cget("width") * 0.5) - self.fHomeWC.grid_info()["padx"] * 2,
							height=self.FrameHome.cget("height"))

		# Shutter
		self.fHomeShutter.grid_rowconfigure(0, weight=1)
		self.fHomeShutter.grid_rowconfigure(1, weight=2)
		self.fHomeShutter.grid_rowconfigure(2, weight=1)
		self.fHomeShutter.grid_rowconfigure(3, weight=1)
		self.fHomeShutter.grid_columnconfigure(1, weight=1)

		# RGB
		self.fHomeRGB.grid_rowconfigure(0, weight=1)
		self.fHomeRGB.grid_rowconfigure(1, weight=1)
		self.fHomeRGB.grid_rowconfigure(2, weight=1)
		self.fHomeRGB.grid_columnconfigure(0, minsize=int(self.FrameHome.cget("height") * 0.33), weight=1)

		# WC
		self.fHomeWC.grid_propagate(0)
		self.fHomeWC.grid_columnconfigure(0, minsize=int(self.fHomeWC.cget("width") * 0.75), weight=0)
		self.fHomeWC.grid_columnconfigure(1, weight=1)
		self.fHomeWC.grid_rowconfigure(0, minsize=int(self.fHomeWC.cget("height") * 0.75), weight=0)
		self.fHomeWC.grid_rowconfigure(1, weight=1)

		### RGB ###
		self.FrameRGB.config(width=self.width, height=int(self.height * self.rel_panel_height))
		self.FrameRGB.grid_rowconfigure(0, weight=1, minsize=int(self.FrameRGB.cget("height")*0.11))
		self.FrameRGB.grid_rowconfigure(1, weight=1)
		self.FrameRGB.grid_columnconfigure(4, minsize=int(0.05*self.width), weight=1)
		self.FrameRGB.grid_columnconfigure(5, weight=1)
		self.FrameRGB.grid_columnconfigure(6, weight=1, minsize=int(self.width*0.15))

		self.fRGBPresetBtns.grid_columnconfigure(0, weight=1)
		self.fRGBPresetBtns.grid_rowconfigure(2, weight=1)

	def load_pictures(self):
		path = "./Img/"
		self.btn_pictures = {"DpbSymbol": tk.PhotoImage(file=path + "DpbSun50x50.png"),
							 "MenuSymbol": tk.PhotoImage(file=path + "MenuSym50x50.png"),
							 "RGBOff": tk.PhotoImage(file=path + "RGBOff100x100.png"),
							 "RGBOn": tk.PhotoImage(file=path + "RGBOn100x100.png"),
							 "ShutterDown": tk.PhotoImage(file=path + "RlldDown100x100.png"),
							 "ShutterStop": tk.PhotoImage(file=path + "RlldStop100x50.png"),
							 "ShutterUp": tk.PhotoImage(file=path + "RlldUp100x100.png"),
							 "WCOff": tk.PhotoImage(file=path + "WCOff235x235.png"),
							 "WCOn": tk.PhotoImage(file=path + "WCOn235x235.png"),
							 "TimeDown": tk.PhotoImage(file=path + "TimeDown50x50.png"),
							 "TimeUp": tk.PhotoImage(file=path + "TimeUp50x50.png")}

#################################################################
# Events and other Functions
#################################################################

	#### Fill Listbox
	def rgb_fill_listbox(self):
		presets = self.mainInst.RGB.RGB_config[self.mainInst.RGB.preset_type]

		self.RGB_lbxPresets.delete(0, tk.END)
		for preset in presets:
			self.RGB_lbxPresets.insert(tk.END, preset["name"])

			rgb = preset["data"][:3] if self.mainInst.RGB.preset_type == "Presets" else preset["data"][0][:3]
			bg_color = self.hex_from_rgb(rgb)
			self.RGB_lbxPresets.itemconfig(tk.END, background=bg_color, selectbackground=bg_color)

			fg_color = "#000000" if max(rgb) > 128 else "#ffffff"
			self.RGB_lbxPresets.itemconfig(tk.END, foreground=fg_color, selectforeground=fg_color)

	### Blank
	def blank_screen(self):
		self.FrameBlank.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)
		self.FrameBlank.lift()
		if sys.platform == "linux":
			with open("/sys/class/backlight/rpi_backlight/bl_power", "w") as f:
				print("blank_writefile")
				f.write("1")

	def unblank_screen(self, evt=None):
		self.last_unblank = time.time()
		self.FrameBlank.grid_forget()
		if sys.platform == "linux":
			with open("/sys/class/backlight/rpi_backlight/bl_power", "w") as f:
				print("unblank_writefile")
				f.write("0")

	#### Top Bar Events
	def topBar_btnDpb_event(self):
		pass

	def topBar_btnMenu_event(self):
		if self.FrameMenu.grid_info() != {}:
			self.FrameMenu.grid_forget()
		else:
			self.FrameMenu.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NS + tk.W)
			self.FrameMenu.lift()

	### Menu Frame Events
	def menu_DisplayFrame_event(self, frame):
		if frame.grid_info() == {}:
			self.displayed_frame.grid_forget()
			self.displayed_frame = frame
			frame.grid(row=1, column=0, pady=1, padx=1, sticky=tk.NSEW)
		self.FrameMenu.grid_forget()

	### Home Frame Events
	def home_btnSetShutter_event(self):
		pass

	def home_btnShutterUp_event(self):
		# Shutter Module
		self.mainInst.Shutter.shutter_up()

	def home_btnShutterStop_event(self):
		# Shutter Module
		self.mainInst.Shutter.shutter_stop()

		# Update Scale
		self.sclShutterVar.set(round(self.mainInst.Shutter.value/self.mainInst.Shutter.max_value * 100))

	def home_btnShutterDown_event(self):
		# Shutter Module
		self.mainInst.Shutter.shutter_down()

	def home_btnRGB_event(self, idx):
		# RGB Module
		self.mainInst.RGB.btn_relays_event(idx)

		# GUI Updates
		if self.mainInst.RGB.btn_relay_values[idx]:
			self.Home_btnRGBRelayChannels[idx].config(image=self.btn_pictures["RGBOn"])
		else:
			self.Home_btnRGBRelayChannels[idx].config(image=self.btn_pictures["RGBOff"])
		# TODO Load rgb picture

	def home_btnWC_event(self):
		# WC Module
		self.mainInst.WC.relay_btn()

		# GUI Update
		if self.mainInst.WC.btn_relay_value:
			self.Home_btnWC.config(image=self.btn_pictures["WCOn"])
		else:
			self.Home_btnWC.config(image=self.btn_pictures["WCOff"])

	def home_sclBrightness_event(self, value):
		# WC Module
		self.mainInst.WC.brightness_to_value(brightness=int(value))

	def home_sclBalance_event(self, value):
		# WC Module
		self.mainInst.WC.balance_to_values(balance=int(value))
		# GUI Update
		# TODO adjust troughcolor

	### RGB Frame Events
	def rgb_scales_event(self, index, value):
		# RGB Module
		self.mainInst.RGB.scl_event(index, int(value))

		# GUI Update
		self.rgb_set_master_bg()

	def rgb_btnChannelSelection_event(self, channels: list):
		# RGB Module and values
		self.mainInst.RGB.btn_channel_selection(channels, self.mainInst.RGB.gui_selected_channels.index(True))

		# GUI Update
		# Set Button background
		idx = [[True, True], [True, False], [False, True]].index(channels)
		not_selected_dict = {
			"fg": self.palette["foreground"],
			"activeforeground": self.palette["activeForeground"],
			"bg": self.palette["background"],
			"activebackground": self.palette["activeBackground"]
		}

		for i, btn in enumerate((self.RGB_btnChannelBoth, self.RGB_btnChannelOne, self.RGB_btnChannelTwo)):
			if i == idx:
				btn.config(cnf=self.selected_RGB_channel_palette)
			else:
				btn.config(cnf=not_selected_dict)

		# Set Scales according to selected RGB channel
		rgbm_values = self.mainInst.RGB.get_rgbm_from_channel()
		for sclvar, value in zip(self.RGB_scalesVars, rgbm_values):
			sclvar.set(value)

		# Master background
		self.rgb_set_master_bg()

	def rgb_btnPresetType_event(self):
		# RGB Module
		self.mainInst.RGB.switch_preset_type()

		# GUI Update
		if self.mainInst.RGB.preset_type == "Animations":
			self.RGB_btnPresetType.config(text="Animationen")
			self.RGB_btnStart.config(state=tk.NORMAL)
			self.RGB_btnStop.config(state=tk.NORMAL)
			self.RGB_btnAdd.config(state=tk.DISABLED)
			self.RGB_btnDelete.config(state=tk.DISABLED)
		else:
			self.RGB_btnPresetType.config(text="Farbe")
			self.RGB_btnAdd.config(state=tk.NORMAL)
			self.RGB_btnDelete.config(state=tk.NORMAL)
			if not self.mainInst.RGB.animation_active:
				self.RGB_btnStart.config(state=tk.DISABLED)
				self.RGB_btnStop.config(state=tk.DISABLED)

		self.rgb_fill_listbox()

	def rgb_btnPresetSelect_event(self):
		# RGB Module
		disable_start_stop = False
		if self.mainInst.RGB.preset_type == "Presets":
			self.mainInst.RGB.animation_stop(reset=True)
			disable_start_stop = True

		idx = self.RGB_lbxPresets.curselection()[-1]
		self.mainInst.RGB.select_preset(idx)

		# GUI Update
		if disable_start_stop:
			self.RGB_btnStart.config(state=tk.DISABLED)
			self.RGB_btnStop.config(state=tk.DISABLED)
		self.rgb_update_scales_from_values()

		self.rgb_set_master_bg()

	def rgb_btnPresetAdd_event(self):
		print("add")
		# RGB Module
		self.mainInst.RGB.add_preset()

		# GUI Update
		self.rgb_update_scales_from_values()
		self.rgb_fill_listbox()

	def rgb_btnPresetDelete_event(self):
		# RGB Module
		idx = self.RGB_lbxPresets.curselection()[-1]
		self.mainInst.RGB.delete_preset(idx)

		# GUI Update
		self.rgb_fill_listbox()
		pass

	def rgb_btnPresetStart_event(self):
		# RGB Module
		self.mainInst.RGB.animation_start()
		pass

	def rgb_btnPresetStop_event(self):
		# RGB Module
		# reset = False if self.mainInst.RGB.preset_type == "Animations" else True
		self.mainInst.RGB.animation_stop()

	def rgb_update_scales_from_values(self):
		values = self.mainInst.RGB.get_rgbm_from_channel()
		for i in range(4):
			self.RGB_scalesVars[i].set(values[i])

	### Utils ###
	def rgb_handle_animation(self):
		self.rgb_update_scales_from_values()
		self.rgb_set_master_bg()

	def rgb_set_master_bg(self):
		rgb = self.mainInst.RGB.get_rgbm_from_channel()[:3]
		bg_color = self.hex_from_rgb(rgb)
		fg_color = "#000000" if max(rgb) >= 128 else "#ffffff"
		self.RGB_sclMaster.config(bg=bg_color, activebackground=bg_color, fg=fg_color, troughcolor=bg_color)

	@staticmethod
	def hex_from_rgb(rgb):
		hexcode = '#%02x%02x%02x' % tuple(rgb)
		return hexcode


if __name__ == "__main__":
	UI = UserInterface()
	print(UI.hex_from_rgb((255, 128, 10)))
	UI.root.mainloop()

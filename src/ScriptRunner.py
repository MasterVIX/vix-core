# for localized messages
from . import _

from Screens.Screen import Screen
from Screens.Console import Console
from Screens.Setup import Setup
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigYesNo
from IPKInstaller import IpkgInstaller

config.scriptrunner = ConfigSubsection()
config.scriptrunner.close = ConfigYesNo(default=False)


class VIXScriptRunner(IpkgInstaller):
	def __init__(self, session, list=None):
		if not list: list = []
		IpkgInstaller.__init__(self, session, list)
		Screen.setTitle(self, _("Script Runner"))
		self.skinName = "IpkgInstaller"
		self["key_green"] = StaticText(_("Run"))

		self['myactions'] = ActionMap(["MenuActions"],
									  {
									  "menu": self.createSetup,
									  }, -1)

	def createSetup(self):
		self.session.open(Setup, 'vixscriptrunner', 'SystemPlugins/ViX')

	def install(self):
		list = self.list.getSelectionsList()
		cmdList = []
		for item in list:
			cmdList.append('chmod +x /usr/script/' + item[0] + ' && . ' + '/usr/script/' + str(item[0]))
		if len(cmdList) < 1 and len(self.list.list):
			cmdList.append('chmod +x /usr/script/' + self.list.getCurrent()[0][0] + ' && . ' + '/usr/script/' + str(self.list.getCurrent()[0][0]))
		if len(cmdList) > 0:
			self.session.open(Console, cmdlist=cmdList, closeOnSuccess=config.scriptrunner.close.value)

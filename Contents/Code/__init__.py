import sports_streams_core as core
import datetime
from dateutil import tz

###############################################



SPORT_KEYWORD = "hockey"
#STREAM_FORMAT = "http://nlds{server}.cdnak.neulion.com/nlds/nhl/{streamName}/as/live/{streamName}_hd_{q}.m3u8?t={title}&l={logo}&d={desc}"
STREAM_FORMAT = "http://nlds{server}.cdnak.neulion.com/nlds/nhl/{streamName}/as/live/{streamName}_hd_{q}.m3u8"


###############################################

# This function is initially called by PMS to inialize the plugin

def Start():

	# Initialize the plugin
	Plugin.AddPrefixHandler(core.VIDEO_PREFIX, MainMenu, core.NAME, core.ICON, core.ART)
	Plugin.AddViewGroup("List", viewMode = "InfoList", mediaType = "items")
		
	ObjectContainer.title1 = core.NAME
	
	#core.Init(NAME, SPORT_KEYWORD, STREAM_FORMAT, TEAMS, DEFAULT_TEAM_ICON)
	
	Log.Debug("Plugin Start")

def MainMenu():
	dir = ObjectContainer(title2 = L("MainMenuTitle"), art=R(core.ART), view_group = "List")
	
	#try:
	core.BuildMainMenu(dir, ScheduleMenu, ArchiveMenu)
	#except core.NoGamesException:
	#	Log.Debug("no games")
	#	return ObjectContainer(header=L("MainMenuTitle"), message=L("ErrorNoGames")) 
	
	Log.Debug("View Groups")
	
	for item in Plugin.ViewGroups:
		Log.Debug(str(item))
	
	return dir
	 	
def ScheduleMenu(date, title):	
	dir = ObjectContainer(title2 = title, art=R(core.ART), view_group = "List")
	
	try:
		core.BuildScheduleMenu(dir, date, GameMenu, MainMenu)
	except core.NoGamesException:
		dir.add(DirectoryObject(
			key = Callback(ScheduleMenu, date=date), # call back to itself makes it go nowhere - in some clients anyway.
			title = L("ErrorNoGames"),
			thumb = R(core.DEFAULT_TEAM_ICON)
		))
		
	
	return dir

################################################################################
# 
# Archive Menus
#
################################################################################
	
def ArchiveMenu():
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	core.BuildArchiveMenu(dir, ArchiveTeamMenu, ArchiveDayMenu, ArchiveWeekMenu, ArchiveDateMenu)
	# this should allow users to select older dates than the main menu shows.
	return dir

def ArchiveTeamMenu():
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	core.BuildArchiveTeamMenu(dir, ArchiveMenuForTeam)
	# this should allow users to select older dates than the main menu shows.

	
	return dir

def ArchiveMenuForTeam(team):
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	try:
		core.BuildArchiveMenuForTeam(dir, team, GameMenu)
	except core.NoGamesException:
		dir.add(DirectoryObject(
			key = Callback(ArchiveMenuForTeam, team=team), # call back to itself makes it go nowhere - in some clients anyway.
			title = L("ErrorNoGames"),
			thumb = R(core.DEFAULT_TEAM_ICON)
		))
	
	# this should allow users to select older dates than the main menu shows.
	return dir

def ArchiveDayMenu():
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	# this should allow users to select older dates than the main menu shows.
	return dir

def ArchiveWeekMenu():
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	# this should allow users to select older dates than the main menu shows.
	return dir

def ArchiveDateMenu():
	dir = ObjectContainer(title2 = "Archive", art=R(core.ART))

	# this should allow users to select older dates than the main menu shows.
	return dir

################################################################################
	
def GameMenu(gameId, title):
	dir = ObjectContainer(title2 = title, art=R(core.ART))
	
	core.BuildGameMenu(dir, gameId, HighlightsMenu, SelectQualityMenu)
	
	return dir
	
def HighlightsMenu(gameId, title):
	dir = ObjectContainer(title2 = "TEMP", art=R(core.ART))
	
	return dir
	
def SelectQualityMenu(url, title, logo, available):
	dir = ObjectContainer(title2 = title, art=R(core.ART))
	
	if available == False:
		#show error message instead
		message = str(L("ErrorStreamsNotReady"))
		return ObjectContainer(header=L("MainMenuTitle"), message=message)	
	else:
		core.BuildQualitySelectionMenu(dir, url, logo)
	
	return dir
	
	
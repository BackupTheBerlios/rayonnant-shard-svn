"""
/*
 * Rayonnant Scripts
 * Copyright 2004 by holders identified in shard/docs/authors.xml
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Palace - Suite 330, Boston, MA 02111-1307, USA.
 *
 * In addition to that license, if you are running this program or modified
 * versions of it on a public system you HAVE TO make the complete source of
 * the version used by you available or provide people with a location to
 * download it.
 *
 * Rayonnant Shard Home: http://developer.berlios.de/projects/rayonnant-shard/
 * Official Shard: http://shard.rayonnant.net/
 */
"""

import wolfpack
from wolfpack.consts import *
from wolfpack.gumps import *
from wolfpack.time import *

upseconds = 0
upminutes = 0
uphours = 0

def onLogin( char ):
	socket = char.socket
	socket.sysmessage( "Welcome to Rayonnant." )
	socket.sysmessage( "Use the 'notices command for server notices!" )
	socket.sysmessage( "Other important commands are: " )
	socket.sysmessage( "   'reload python and 'reload xml" )
	return

def snotices( socket, command, arguments ):
	char = socket.player
	version = wolfpack.serverversion()
	uptime = wolfpack.serveruptime()
	upseconds = uptime
	upminutes = uptime/60
	upseconds -= upminutes*60
	if upseconds <= 9:
		upseconds = '0%s' % (upseconds)
	uphours = upminutes/60
	upminutes -= uphours*60
	if upminutes <= 9:
		upminutes = '0%s' % (upminutes)
	if uphours <= 9:
		uphours = '0%s' % (uphours)

	versionstring = 'Version: %s' % ( version )
	timestring = 'Uptime: %s:%s:%s' % ( uphours, upminutes, upseconds )

	gump = cGump( x=60, y=60)
	gump.addBackground( id=0x2436, width=350, height=400 )
	text = '<basefont color="#FFFF00"><center><h3>SHARD WIDE NOTICES</h3></center><br><basefont color="#FEFEFE">Welcome to Rayonnant: <basefont color="#00FFFF">%s<br><basefont color="#FEFEFE">   * The shard is running on Wolfpack CVS.<br>   * So crashes <b>WILL</b> happen!<br><br>Script testing is <basefont color="#00FF00">ALLOWED<br><basefont color="#FEFEFE">World building is <basefont color="#00FF00">ALLOWED<br><br><basefont color="#FEFEFE">When building:<br>    Save often and \'export when finished.<br>    Adding is in hex, but without the leading 0x.<br>      Example: \'add f51 will add a dagger.<br>    Tile format: \'tile Z ID [,IDN]<br>      Example: \'tile 20 4c6,4c7,4c8,4c9<br><br>Server Information:<br>    %s<br>    %s' % ( char.name, versionstring, timestring )
	gump.addHtmlGump( x=20, y=20, width=310, height=360, html=text )
	gump.send( char )

def onLoad():
	wolfpack.registercommand( "notices", snotices )
	#wolfpack.registerglobal( EVENT_LOGIN, "commands.server_notices" )
	return

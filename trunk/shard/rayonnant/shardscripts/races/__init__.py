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
from shardscripts.races.raceselection import RACE_TABLE, \
	selectBaseRace, selectAdvancedRace
from wolfpack.gumps import cGump

def onLoad():
	wolfpack.registercommand( "pickrace", onCommand )
	wolfpack.registercommand( "fixrace", onCommand )
	wolfpack.registercommand( "raceinfo", onCommand )
	wolfpack.registercommand( "evolverace", onCommand )
	return

def onLogin( char ):
	if ( not char.hastag( 'race' ) ) or ( not char.gettag( 'race' ) in RACE_TABLE ):
		selectBaseRace( char )

def onShowTooltip(viewer, object, tooltip):
	if object.ischar and object.hastag( 'race' ):
		race = str( object.gettag( 'race' ) )

		if race in RACE_TABLE:
			text = "Race:\t<basefont color='%s'>%s</basefont>" % ( RACE_TABLE[ race ][ 4 ], race )
			tooltip.add( 1053099, text )
			return True

		else:
			text = "Race:\t<basefont color='%s'>%s</basefont>" % ( '#bbbb00', 'Invalid' )
			tooltip.add( 1053099, text )
			return True


def onCommand( socket, command, arguments ):
	char = socket.player
	command = command.lower()

	if not char.hasscript( 'shardscripts.races' ):
		char.addscript( 'shardscripts.races' )

	if command == 'pickrace':
		selectBaseRace( char )

	elif command == 'evolverace':
		if char.gettag( 'race' ) == 'Human' or char.gettag( 'race' ) == 'Elven':
			selectAdvancedRace( char )
		else:
			socket.sysmessage( "You're not even a race to begin with!" )
			return False

	elif command == 'fixrace':
		char.deltag( 'race' )
		char.update()
		char.resendtooltip()
		socket.sysmessage( "Please run 'pickrace to select a race." )

	elif command == 'raceinfo':
		socket.sysmessage( "Your current race is: %s" % ( char.gettag( 'race' ) ) )

	return True




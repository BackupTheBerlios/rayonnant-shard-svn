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
from wolfpack.gumps import cGump

# 'Name': [ strcap, dexcap, intcap, statcap, tooltip color ]
RACE_TABLE = {
	'Human': [ 100, 100, 100, 225, '#00bbbb' ],
	'Elven': [ 85, 115, 110, 225, '#00bb00' ],
	'Undead':  [ 115, 115, 115, 250, '#bb0000' ],
	'Drow': [ 95, 125, 120, 250, '#bb00bb' ]
}

def evolution( char, args, choice ):
	socket = char.socket
	if choice.button <= 0:
		socket.sysmessage("You've chosen not to select a race!")
		return False
	else:
		evolve = choice.switches[0]
		if evolve == 1:
			char.settag( 'race', 'Human' )
			if not raceStats( char ):
				char.deltag( 'race' )
		elif evolve == 2:
			char.settag( 'race', 'Elven' )
			if not raceStats( char ):
				char.deltag( 'race' )
		elif evolve == 3:
			char.settag( 'race', 'Undead' )
			if not raceStats( char ):
				char.deltag( 'race' )
		elif evolve == 4:
			char.settag( 'race', 'Drow' )
			if not raceStats( char ):
				char.deltag( 'race' )
		else:
			socket.sysmessage( "Error: Undefined race selection!" )
			return False
	if not char.hastag( 'race' ):
		socket.sysmessage( "Error in chosen race selection!" )
		return False
	else:
		socket.sysmessage( "Your new race is: %s" % char.gettag( 'race' ) )
		return True
	return False

def selectBaseRace( char ):
	mysock = char.socket
	if char.hastag( 'race' ):
		if char.gettag( 'race' ) == 'Human':
			mysock.sysmessage("You're already Human!")
			return False
		elif char.gettag( 'race' ) == 'Elven':
			mysock.sysmessage("You're already Elven!")
			return False
		elif char.gettag( 'race' ) == 'Undead':
			mysock.sysmessage("You're already Undead!")
			return False
		elif char.gettag( 'race' ) == 'Drow':
			mysock.sysmessage("You're already Drow!")
			return False
	else:
		mysock.sysmessage("You need to select your race!")
		# Race Gump
		gump = cGump( x=40, y=40, noclose=1, callback=evolution )
		# Default Background
		gump.startPage( 0 )
		gump.startPage( 1 )
		gump.addResizeGump( 0, 0, 0x2436, 300, 285 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Race Slection</h3></center><p><basefont color="#FEFEFE">%s, Welcome to Rayonnant.<br>To continue your journey select a race.<br><br>Race Information:' % (char.name)
		gump.addHtmlGump( 20, 20, 260, 145, text )
		gump.addText( 55, 150, 'Human Information', 0x835 )
		gump.addPageButton( 180, 150, 0x26af, 0x26b1, 2 )
		gump.addText( 55, 180, 'Elf Information', 0x835 )
		gump.addPageButton( 180, 180, 0x26af, 0x26b1, 3 )
		gump.startGroup( 0 )
		# Human Button
		gump.addRadioButton( 20, 235, 0x25f8, 0x25fb, selected=1, id=1 )
		gump.addText( 55, 240, 'Human', 0x835 )
		# Elf Button
		gump.addRadioButton( 110, 235, 0x25f8, 0x25fb, id=2 )
		gump.addText( 145, 240, 'Elf', 0x835 )
		# Evolve!
		gump.addButton( 220, 240, 0xf9, 0xf8, returncode=1 ) # Okay Button
		# Human Information Page
		gump.startPage( 2 )
		gump.addResizeGump( 0, 0, 0x2436, 380, 445 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Basic Human Information</h3></center><p><basefont color="#FEFEFE">Humans are.... Blah blah blah blah blah....'
		gump.addHtmlGump( 20, 20, 340, 405, text )
		gump.addPageButton( 300, 405, 0xf9, 0xf8, 1 ) # Okay Button
		# Elf Information Page
		gump.startPage( 3 )
		gump.addResizeGump( 0, 0, 0x2436, 380, 445 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Basic Elf Information</h3></center><p><basefont color="#FEFEFE">Elves are.... Blah blah blah blah blah....'
		gump.addHtmlGump( 20, 20, 340, 405, text )
		gump.addPageButton( 300, 405, 0xf9, 0xf8, 1 ) # Okay Button
		# Send Gump!
		gump.send( char )
		return

def selectAdvancedRace( char ):
	mysock = char.socket
	if char.gettag( 'race' ) == 'Human':
		# Race Gump
		gump = cGump( x=40, y=40, noclose=1, callback=evolution )
		# Default Background
		gump.startPage( 0 )
		gump.startPage( 1 )
		gump.addResizeGump( 0, 0, 0x2436, 300, 285 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Advanced Race Evolution</h3>'
		text += '</center><br/><basefont color="#FEFEFE">You\'ve been given a chance'
		text += ' to evolve.<br/><br/>You have two options:<br/>    '
		text += '1. Remain Human<br/>    2. Turn Undead.<br/><br/>    '
		text += 'Make this decision wisely...'
		gump.addHtmlGump( 20, 20, 260, 245, text )
		gump.addText( 85, 195, 'Undead Information', 0x835 )
		gump.addPageButton( 210, 195, 0x26af, 0x26b1, 2 )
		gump.startGroup( 0 )
		# Undead Button
		gump.addRadioButton( 20, 235, 0x25f8, 0x25fb, id=3 )
		gump.addText( 55, 240, 'Undead', 0x835 )
		# Evolve!
		gump.addButton( 150, 240, 0xf3, 0xf1, returncode=0 ) # Cancel Button
		gump.addButton( 220, 240, 0xf9, 0xf8, returncode=1 ) # Okay Button
		# Undead Information Page
		gump.startPage( 2 )
		gump.addResizeGump( 0, 0, 0x2436, 380, 445 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>'
		text += 'Undead Information</h3></center><p><basefont color="#FEFEFE">'
		text += 'The Undead are.... Blah blah blah blah blah....'
		gump.addHtmlGump( 20, 20, 340, 405, text )
		gump.addPageButton( 300, 405, 0xf9, 0xf8, 1 ) # Okay Button
		# Send Gump!
		gump.send( char )
		return

	elif char.gettag( 'race' ) == 'Drow':
		gump = cGump( x=40, y=40, noclose=1, callback="shardscripts.races.raceselection.evolution" )
		# Default Background
		gump.startPage( 0 )
		gump.startPage( 1 )
		gump.addResizeGump( 0, 0, 0x2436, 300, 285 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Advanced Race Evolution</h3></center><p><basefont color="#FEFEFE">%s,<br>    You have been given a chance to evolve.<br>You have two options:<br>    Remain Human or Turn Undead.<p><i>Choose wisely...</i>' % (char.name)
		gump.addHtmlGump( 20, 20, 260, 145, text )
		gump.addText( 55, 180, 'Drow Information', 0x835 )
		gump.addPageButton( 180, 180, 0x26af, 0x26b1, 2 )
		gump.startGroup( 0 )
		# Drow Button
		gump.addRadioButton( 20, 235, 0x25f8, 0x25fb, id=4 )
		gump.addText( 55, 240, 'Drow', 0x835 )
		# Evolve!
		gump.addButton( 220, 240, 0xf3, 0xf1, returncode=0 ) # Cancel Button
		gump.addButton( 220, 240, 0xf9, 0xf8, returncode=1 ) # Okay Button
		# Human Information Page
		gump.startPage( 2 )
		gump.addResizeGump( 0, 0, 0x2436, 380, 445 ) # Background
		text = '<basefont color="#FFFF00"><center><h3>Drow Information</h3></center><p><basefont color="#FEFEFE">The Drow are.... Blah blah blah blah blah....'
		gump.addHtmlGump( 20, 20, 340, 405, text )
		gump.addPageButton( 300, 405, 0xf9, 0xf8, 1 ) # Okay Button
		# Send Gump!
		gump.send( char )
		return

def raceStats( char ):
	if char.hastag( 'race' ) and char.gettag( 'race' ) in RACE_TABLE:
		char.strengthcap = RACE_TABLE[ char.gettag( 'race' ) ][ 0 ]
		char.dexteritycap = RACE_TABLE[ char.gettag( 'race' ) ][ 1 ]
		char.intelligencecap = RACE_TABLE[ char.gettag( 'race' ) ][ 2 ]
		char.statcap = RACE_TABLE[ char.gettag( 'race' ) ][ 3 ]
		char.updatestats()
		if not char.hasscript( 'shardscripts.races' ):
			char.addscript( 'shardscripts.races' )
		char.resendtooltip()
		return True
	return False

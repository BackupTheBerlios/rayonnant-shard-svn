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

def dowipe( socket, command, arguments ):
	socket.sysmessage( "Target the upper left corner of the area you want to wipe." )
	socket.attachtarget( "shardscripts.commands.safe_wipe.callback", [] )
	return

def callback( char, args, target ):
	socket = char.socket

	# Upper left Corner
	if len( args ) == 0:
		if target.item and target.item.container:
			socket.sysmessage( "This is an invalid target." )
			return

		socket.sysmessage( "Target the lower right corner of the area you want to wipe." )
		socket.attachtarget( "shardscripts.commands.safe_wipe.callback", [ target.pos.x, target.pos.y ] )

	# Lower Right Corner
	elif len( args ) == 2:
		if target.item and target.item.container:
			socket.sysmessage( "This is an invalid target." )
			return

		# Create a gump to confirm the wipe.
		x1 = min( args[0], target.pos.x )
		x2 = max( args[0], target.pos.x )
		y1 = min( args[1], target.pos.y )
		y2 = max( args[1], target.pos.y )

		gump = cGump( 0, 0, 0, 100, 100 )
		gump.addBackground( id=0x2436, width=350, height=165 )
		text = '<basefont color="#00FF00"><h3>Wipe Selected Area</h3><br><basefont color="#FEFEFE"><u>X1</u>, <u>Y1</u>: %u, %u<br><u>X2</u>, <u>Y2</u>: %u, %u<br><br>Please confirm the wipe of the selected area.' % ( x1, y1, x2, y2 )
		gump.addHtmlGump( x=20, y=20, width=310, height=150, html=text )
		# Confirm Button
		gump.startGroup( 0 )
		gump.addRadioButton( x=20, y=115, off=0x25f8, on=0x25fb, id=1 )
		gump.addText( x=55, y=120, text='Confirm', hue=0x835 )
		# Wipe Button
		gump.addText( x=240, y=120, text='Wipe Area', hue=0x835 )
		gump.addButton( x=310, y=120, up=0x26af, down=0x26b1, returncode=1 )
		gump.setCallback( "shardscripts.commands.safe_wipe.wipe" )
		gump.setArgs( [x1, y1, x2, y2] )
		gump.send( char )
		return True

def wipe( char, args, choice ):
	if not args or not choice:
		return False

	if choice.button != 1 or len( args ) != 4:
		return False

	if len( choice.switches ) != 1:
		char.socket.sysmessage( "Error: You did not confirm your wipe." )
		char.socket.sysmessage( "Safeguard: Wipe has been canceled." )
		return False

	if len(args) == 4 and len(choice.switches) == 1 and choice.button == 1:
		format = choice.switches[0]

		iterator = wolfpack.itemregion( args[0], args[1], args[2], args[3], char.pos.map )
		item = iterator.first
		icount = 0
		while item:
			if format == 1: # Confirmed Wipe
				item.delete()
				icount += 1
			else:
				char.socket.sysmessage( "Error: You did not confirm your wipe." )
			item = iterator.next

		char.socket.sysmessage( "Deleted %i objects during the wipe." %  icount )
		return True
	else:
		return False

def onLoad():
	wolfpack.registercommand( "safewipe", dowipe )
	return

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
from wolfpack.consts import EVENT_LOGIN
from wolfpack.gumps import cGump

#VIRTUES
# Name: [name, min, max]
VIRTUES = {
	0: ['virtue_compassion', 0, 100],
	1: ['virtue_honesty', 0, 100],
	2: ['virtue_honor', 0, 100],
	3: ['virtue_humility', 0, 100],
	4: ['virtue_justice', 0, 100],
	5: ['virtue_sacrifice', 0, 100],
	6: ['virtue_spirituality', 0, 100],
	7: ['virtue_valor', 0, 100],
	8: ['virtue_chaos', 0, 100]
}

VIRTUE_DELAY = 10000 # 10 Seconds
COMPASSION = 0
HONESTY = 1
HONOR = 2
HUMILITY = 3
JUSTICE = 4
SACRIFICE = 5
SPIRITUALITY = 6
VALOR = 7
CHAOS = 8

def performVirtue( char, virtue ):
	mysock = char.socket
	if char.hastag( VIRTUES[virtue][0] ):
		if virtue == COMPASSION:
			mysock.sysmessage("Test")
			return True
		elif virtue == HONESTY:
			mysock.sysmessage("Test")
			return True
		elif virtue == HONOR:
			mysock.sysmessage("Test")
			return True
		elif virtue == HUMILITY:
			mysock.sysmessage("Test")
			return True
		elif virtue == JUSTICE:
			mysock.sysmessage("Test")
			return True
		elif virtue == SACRIFICE:
			mysock.sysmessage("Test")
			return True
		elif virtue == SPIRITUALITY:
			mysock.sysmessage("Test")
			return True
		elif virtue == VALOR:
			mysock.sysmessage("Test")
			return True
		elif virtue == CHAOS:
			mysock.sysmessage("Test")
			return True
	return False

def response( char, args, target ):
	mysock = char.socket
	mysock.sysmessage("Eeeeeep!")
	return


def virtueInfo( char, args, virtue):
	mysock = char.socket
	if virtue.button == 0: # Compassion
		mysock.sysmessage( "You've envoked the virtue Compassion." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 1: # Honesty
		mysock.sysmessage( "You've envoked the virtue Honesty." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 2: # Honor
		mysock.sysmessage( "You've envoked the virtue Honor." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 3: # Humility
		mysock.sysmessage( "You've envoked the virtue Humility." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 4: # Justice
		mysock.sysmessage( "You've envoked the virtue Justice." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 5: # Sacrifice
		mysock.sysmessage( "You've envoked the virtue Sacrifice." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 6: # Spirituality
		mysock.sysmessage( "You've envoked the virtue Spirituality." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 7: # Valor
		mysock.sysmessage( "You've envoked the virtue Valor." )
		performVirtue( char, virtue.button )
		return True
	elif virtue.button == 8: # Chaos
		mysock.sysmessage( "You've envoked the virtue Chaos." )
		performVirtue( char,virtue.button )
		return True
	return False

def virtueDisplay( socket, command, arguments ):
	char = socket.player
	# Race Gump
	gump = cGump( x=10, y=50, callback=virtueInfo )
	gump.addBackground( id=0x53, width=180, height=240 )
	#text = '<basefont color="#FFFF00"><h3>Race Selection</h3><br><basefont color="#FEFEFE">%s, Welcome to Rayonnant.<br> To continue you must select a race.' % ( char.name )
	#gump.addHtmlGump( x=20, y=20, width=310, height=150, html=text )
	gump.addText( x=20, y=15, text='Your Virtue Skill Levels', hue=0x488 )
	# Race Selection
	gump.startGroup( 0 )
	# Virtue List
	gump.addText( x=35, y=35, text='Compassion', hue=0x846 )
	gump.addText( x=35, y=55, text='Honesty', hue=0x84d )
	gump.addText( x=35, y=75, text='Honor', hue=0x42f )
	gump.addText( x=35, y=95, text='Humility', hue=0x561 )
	gump.addText( x=35, y=115, text='Justice', hue=0x24b )
	gump.addText( x=35, y=135, text='Sacrifice', hue=0x84a )
	gump.addText( x=35, y=155, text='Spirituality', hue=0x84c )
	gump.addText( x=35, y=175, text='Valor', hue=0x555 )
	gump.addText( x=35, y=195, text='Chaos', hue=0x845 )
	# Virtue Values
	gump.addText( x=135, y=35, text="%s" % char.gettag( VIRTUES[COMPASSION][0] ), hue=0x846 )
	gump.addText( x=135, y=55, text="%s" % char.gettag( VIRTUES[HONESTY][0] ), hue=0x84d )
	gump.addText( x=135, y=75, text="%s" % char.gettag( VIRTUES[HONOR][0] ), hue=0x42f )
	gump.addText( x=135, y=95, text="%s" % char.gettag( VIRTUES[HUMILITY][0] ), hue=0x561 )
	gump.addText( x=135, y=115, text="%s" % char.gettag( VIRTUES[JUSTICE][0] ), hue=0x24b )
	gump.addText( x=135, y=135, text="%s" % char.gettag( VIRTUES[SACRIFICE][0] ), hue=0x84a )
	gump.addText( x=135, y=155, text="%s" % char.gettag( VIRTUES[SPIRITUALITY][0] ), hue=0x84c )
	gump.addText( x=135, y=175, text="%s" % char.gettag( VIRTUES[VALOR][0] ), hue=0x555 )
	gump.addText( x=135, y=195, text="%s" % char.gettag( VIRTUES[CHAOS][0] ), hue=0x845 )
	# Buttons
	gump.addButton( x=15, y=37, up=0x4ba, down=0x4b9, returncode=0 )
	gump.addButton( x=15, y=57, up=0x4ba, down=0x4b9, returncode=1 )
	gump.addButton( x=15, y=77, up=0x4ba, down=0x4b9, returncode=2 )
	gump.addButton( x=15, y=97, up=0x4ba, down=0x4b9, returncode=3 )
	gump.addButton( x=15, y=117, up=0x4ba, down=0x4b9, returncode=4 )
	gump.addButton( x=15, y=137, up=0x4ba, down=0x4b9, returncode=5 )
	gump.addButton( x=15, y=157, up=0x4ba, down=0x4b9, returncode=6 )
	gump.addButton( x=15, y=177, up=0x4ba, down=0x4b9, returncode=7 )
	gump.addButton( x=15, y=197, up=0x4ba, down=0x4b9, returncode=8 )
	gump.send( char )
	return True

def virtueReset( socket, command, arguments ):
	char = socket.player
	for virtue in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
		char.settag( VIRTUES[virtue][0], VIRTUES[virtue][1] )
	return

# doCompassion
def doCompassion(char, args, target):
	mysock = char.socket
	mysock.sysmessage( "You've shown compassion for %s" % ( target.name ) )
	return

def onLoad():
	wolfpack.registerglobal( EVENT_LOGIN, "shardscripts.virtues" )
	wolfpack.registercommand( "virtues", virtueDisplay )
	wolfpack.registercommand( "virtuereset", virtueReset )
	return

def onLogin( char ):
	for virtue in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
		if not char.hastag( VIRTUES[virtue][0] ):
			char.settag( VIRTUES[virtue][0], VIRTUES[virtue][1] )
	return

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
from wolfpack.gumps import *
import os

# BaseID's not to save.
# World Gems
# Doors/Gates
nonsaves = [ \
	'gem', 'ore_gem', 'wood_gem', \
	'675','676','677','678','679','67a','67b','67c','67d','67e','67f','680','681','682', \
	'683','684','685','686','687','688','689','68a','68b','68c','68d','68e','68f','690', \
	'691','692','693','694','695','696','697','698','699','69a','69b','69c','69d','69e', \
	'69f','6a0','6a1','6a2','6a3','6a4','6a5','6a6','6a7','6a8','6a9','6aa','6ab','6ac', \
	'6ad','6ae','6af','6b0','6b1','6b2','6b3','6b4','6b5','6b6','6b7','6b8','6b9','6ba', \
	'6bb','6bc','6bd','6be','6bf','6c0','6c1','6c2','6c3','6c4','6c5','6c6','6c7','6c8', \
	'6c9','6ca','6cb','6cc','6cd','6ce','6cf','6d0','6d1','6d2','6d3','6d4','6d5','6d6', \
	'6d7','6d8','6d9','6da','6db','6dc','6dd','6de','6df','6e0','6e1','6e2','6e3','6e4', \
	'6e5','6e6','6e7','6e8','6e9','6ea','6eb','6ec','6ed','6ef','6f0','6f1','6f2','6f3','6f4', \
	'824','825','826','827','828','829','82a','82b','82c','82d','82e','82f','830','831','832', \
	'833','839','83a','83b','83c','83d','83e','83f','840','841','842','843','844','845','846', \
	'847','848','84c','84d','84e','84f','850','851','852','853','854','855','856','857','858', \
	'859','85a','85b','866','867','868','869','86a','86b','86c','86d','86e','86f','870','871', \
	'872','873','874','875','1fed','1fee','1fef','1ff0','1ff1','1ff2','1ff3','1ff4','1ff5','1ff6', \
	'1ff7','1ff8','1ff9','1ffa','1ffb','1ffc','e8','e9','ea','eb','ec','ed','ef','f0','f1','f2','f3','f4', \
	'f5','f6','f7','314','315','316','317','318','319','31a','31b','31c','31d','31e','31f','320', \
	'321','322','323','324','325','326','327','328','329','32a','32b','32c','32d','32e','32f', \
	'330','331','332','333','334','335','336','337','338','339','33a','33b','33c','33d','33e', \
	'33f','340','341','342','343','344','345','346','347','348','349','34a','34b','34c','34d', \
	'34e','34f','350','351','352','353','354','355','356','357','358','359','35a','35b','35c', \
	'35d','35e','35f','360','361','362','363' ]

"""
	\command backupworld
	\description Performs a WSC world save for easy import/export and merges.
	\usage - <code>backupworld</code>
	\notes The default path is /Buildings/world_backup.wsc
"""

def backupWorld( char, args, choice ):
	if choice.button != 1 or len( args ) != 4:
		return True

	filename = choice.text[1]

	if len( choice.switches ) != 1:
		char.socket.sysmessage( "Error: len(choice.switches) != 1." )
		return True

	format = choice.switches[0]

	if len( filename ) == 0:
		char.socket.sysmessage( "Error: You need to provide a valid filename." )
		return True

	# Open the output file
	output = open( filename, "wb" )

	iterator = wolfpack.itemregion( args[0], args[1], args[2], args[3], 0 )
	warnings = ''

	if os.name == 'posix':
		newline = "\n"
	else:
		newline = "\r\n"

	item = iterator.first
	i = 0
	while item:
		if not item.baseid in nonsaves and not item.corpse and len( item.spawnregion ) == 0:
			if format == 2: # WSC, Lonewolf Style, Compatible with Linux Worldforge
				output.write( "SECTION WORLDITEM%s" % newline )
				output.write( "{%s" % newline )
				output.write( "SERIAL %i%s" % ( item.serial, newline ) )
				output.write( "ID %i%s" % ( item.id, newline ) )
				if item.baseid != '':
					output.write( "BASEID %s%s" % ( item.baseid, newline ) )
				if item.name != '#' or item.name != '':
					output.write( "NAME %s%s" % ( item.name, newline ) )

				output.write( "X %i%s" % ( item.pos.x, newline ) )
				output.write( "Y %i%s" % ( item.pos.y, newline ) )
				output.write( "Z %i%s" % ( item.pos.z, newline ) )
				output.write( "MAP %i%s" % ( item.pos.map, newline ) )
				if item.type:
					output.write( "TYPE %i%s" % ( item.type, newline ) ) # World Freeze Requirement
				else:
					output.write( "TYPE 255%s" % newline ) # World Freeze Requirement
				output.write( "COLOR %i%s" % ( item.color, newline ) )
				output.write( "CONT -1%s" % newline )
				output.write( "}%s" % ( newline ) )

			# TXT FORMAT
			elif format == 3:
				output.write( "0x%x %i %i %i 0x%x%s" % ( item.id, item.pos.x, item.pos.y, item.pos.z, item.color, newline ) )

			# WARNINGS
			if item.amount > 1:
				warnings += 'Item %s has an amount of %i. This information will be lost when made static.<br><br>' % ( hex( item.serial ), item.amount )

			scriptlist = item.scriptlist
			if len( scriptlist ) > 0:
				warnings += 'Item %s has scripts (%s) assigned to it. It will not be usable when made static.<br><br>' % ( hex( item.serial ), scriptlist )

			if item.type != 0:
				warnings += 'Item %s is of type %i. It will not be usable when made static.<br><br>' % ( hex( item.serial ), item.type )

			i += 1

		item = iterator.next

	output.close()

	# Show a Report gump
	gump = cGump( x=100, y=100 )

	gump.addBackground( id=0x2436, width=350, height=300 )
	#gump.addCheckerTrans( 15, 15, 320, 270 )

	text = '<basefont color="#FEFEFE"><h3>Export</h3><br><basefont color="#FEFEFE">'
	text += '%d items have been exported to "%s".<br><br>' % ( i, filename )
	text += '<basefont color="#ff0000"><u>Warnings:</u><br>'
	text += '<basefont color="#FEFEFE">%s' % ( warnings )
	gump.addHtmlGump( x=20, y=20, width=310, height=200, html=text, canScroll=1 )

	gump.addText( x=265, y=250, text='Close', hue=0x835 )
	gump.addButton( x=310, y=250, up=0x26af, down=0x26b1, returncode=0 )
	gump.send( char )

	return True

def backupGump( char, args ):
	socket = char.socket
	x1 = 0
	x2 = 6144
	y1 = 0
	y2 = 4096
	gump = cGump( 0, 0, 0, 100, 100 )
	gump.addBackground( id=0x2436, width=350, height=300 )
	#gump.addCheckerTrans( 15, 15, 320, 270 )
	text = '<basefont color="#FEFEFE"><h3>Export</h3><br><basefont color="#FEFEFE">'
	text += '<u>X1</u>,<u>Y1</u>: %i,%i<br><u>X2</u>,<u>Y2</u>: %i,%i' % ( x1, y1, x2, y2 )
	text += '<br><br>Enter the name of the file for the world backup..'
	gump.addHtmlGump( x=20, y=20, width=310, height=200, html=unicode(text) )
	# Radiobuttons
	gump.startGroup( 0 )
	gump.addRadioButton( x=150, y=160, off=0x25f8, on=0x25fb, id=2, selected=1 )
	gump.addText( x=185, y=165, text=unicode('World Forge WSC'), hue=0x835 )
	gump.addResizeGump( x=20, y=210, id=0xBB8, width=310, height=25 )
	gump.addRadioButton( x=250, y=160, off=0x25f8, on=0x25fb, id=3 )
	gump.addText( x=285, y=165, text='Text', hue=0x835 )
	gump.addInputField( x=25, y=212, width=295, height=20, hue=0x834, id=1, starttext="Buildings/world_backup.wsc" )
	gump.addText( x=265, y=250, text=unicode('Export'), hue=0x835 )
	gump.addButton( x=310, y=250, up=0x26af, down=0x26b1, returncode=1 )
	gump.setArgs( [ x1, y1, x2, y2 ] )
	gump.setCallback( backupWorld )
	gump.send( char )
	return True

def backupCmd( socket, command, arguments ):
	backupGump( socket.player, [] )
	return True

def onLoad():
	wolfpack.registercommand( "backupworld", backupCmd )
	return True

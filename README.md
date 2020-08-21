# HoboEncampment
Hobo Encampment: Rules, tips, and nuances:
Hobo Encampment (HE) is a unique game in the sense that all save data is shown on screen.  You effectively are using a terminal to edit a file, with strict rules.
This means saves are very modifiable for your own experimentation.
Start a playthrough by loading an old save or making a new game.  These will be saved to the folder that your game file is in.  I recommend normal mode for a map,
as the values are optimized for a high quality world.
The first step is finding the character 'G' on your map.  This is you.  You cannot leave the map.
Once you are in, you will move with WASD, followed by the enter key.  You cannot walk on water, and moving through unimproved land ('%','&','#') will be harder than
on paths.  You will gain one log for each movement on this land, however.
You may injure yourself crossing unimproved land, but you also may find food.  Once you cross land enough, it will turn into a basic path. to 
These paths are easier to traverse, and actions can be taken from them.  The most basic action is interact, or 'i'.
This will allow you to drink from water, to finish a building project, and to take materials from a source.
You can also take a build action, which either constructs or defines an unfinished project on any land.  Building on undeveloped land will take turns to complete.
If you lack the materials for a building, it will be placed in your unfinished table.  The first entry will be the next symbol, the next two the (y,x) coords, and
the last entries the costs remaining to build.  You can build log holders to make building easier, houses to sleep in and bring people, farms and gardens to
increase people's happiness, and campfires to increase people's desire to come live with you.  To bring people in, you must build a level 3+ path to the road.
You can build quarries and metalworks to produce stone and metal, respectively, and finally dig river channels from water to your camp.
Finally, you can use 3 logs to build a bridge across water one tile at a time.  This will be a path.
Once a building or path is finished, you can use 'u' to upgrade it.  If you cannot afford the upgrade, it will be pushed to the unfinished list.
You can destroy a structure with 'x', but you will not recover anything from it, so be careful!
Very slowly, nature will take back what is rightfully hers, and tiles will revert back to a previous stage.  You can hire clearers to reverse this.
You will die if your health falls below 0, so don't let this happen.  Make sure that you keep your food and water above 0 by eating at farms/gardens and drinking
from water, respectively.
If you go too long without sleep, you will be become lost.  Sleep in beds!  This will also heal you.
Once people have come to your camp, use 'p' to assign them.
Level 3 paths must be built by a house or by another level 3 path.  These are significant because they allow road access, fast travel, and material access.
Save your game with 'c', and get a similar help blurb with 'h'.  

Recommended way to run:
Python IDLE, full screen, font size 14, dark theme (blue background, white text)
https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe


If you encounter bugs, have an idea for a feature, or have other insights into this game, please email me at ajs2290@g.rit.edu.
The code for this game is not optimized completely, and there are some obvious improvements to be made (701-737).  However, part of this game's philosophy
is that all save data should generally look like a screenshot of the game, with some changes, but suggesting the use of dataclasses and an array of houses
to make the appeal_calc() function faster is not the point of the game.  TIP: to find your character 'G' easier, change the 'G' in line 168 to the word 'YOU'.
This will go back to being a 'G' after one cycle.

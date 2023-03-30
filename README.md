# HoboEncampment

## Introduction
Hobo Encampment is a unique game where all save data is shown on screen. You effectively use a terminal to edit a file with strict rules. This means saves are highly modifiable for your own experimentation.

## Starting a Playthrough
To start a playthrough, load an old save or make a new game. These will be saved to the folder that your game file is in. It is recommended to choose normal mode for a map as the values are optimized for a high-quality world.

## Game Mechanics
### Moving and Interacting
The first step is finding the character 'G' on your map, which represents you. Note that you cannot leave the map. Once you are in, you will move with WASD, followed by the enter key. You cannot walk on water, and moving through unimproved land ('%', '&', '#') will be harder than on paths. You will gain one log for each movement on this land, however.

You may injure yourself crossing unimproved land, but you also may find food. Once you cross land enough, it will turn into a basic path. These paths are easier to traverse, and actions can be taken from them. The most basic action is interact, or 'i'. This will allow you to drink from water, to finish a building project, and to take materials from a source.

### Building
You can also take a build action, which either constructs or defines an unfinished project on any land. Building on undeveloped land will take turns to complete. If you lack the materials for a building, it will be placed in your unfinished table. The first entry will be the next symbol, the next two the (y,x) coords, and the last entries the costs remaining to build. You can build log holders to make building easier, houses to sleep in and bring people, farms and gardens to increase people's happiness, and campfires to increase people's desire to come live with you. To bring people in, you must build a level 3+ path to the road.

You can build quarries and metalworks to produce stone and metal, respectively, and finally dig river channels from water to your camp. Finally, you can use 3 logs to build a bridge across water one tile at a time. This will be a path.

### Upgrading and Destroying
Once a building or path is finished, you can use 'u' to upgrade it. If you cannot afford the upgrade, it will be pushed to the unfinished list. You can destroy a structure with 'x', but you will not recover anything from it, so be careful!

### Nature and Survival
Very slowly, nature will take back what is rightfully hers, and tiles will revert back to a previous stage. You can hire clearers to reverse this. You will die if your health falls below 0, so don't let this happen. Make sure that you keep your food and water above 0 by eating at farms/gardens and drinking from water, respectively.

If you go too long without sleep, you will become lost. Sleep in beds! This will also heal you.

### Assigning People and Building Level 3 Paths
Once people have come to your camp, use 'p' to assign them. Level 3 paths must be built by a house or by another level 3 path. These are significant because they allow road access, fast travel, and material access.

## Saving and Help
Save your game with 'c', and get a similar help blurb with 'h'.

## Recommended Way to Run
Recommended way to run: Python IDLE, full screen, font size 14, dark theme (blue background, white text)
https://www.python

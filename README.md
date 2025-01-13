# C(ard)SV Creator
Created for my own workflow of [Obsidian](https://obsidian.md) holding information and ideas for cards, and using [nanDECK](https://nandeck.com) to create the cards and decks themself. I made this to format all my Obsidian files into an CSV that could then be read by nanDECK.

# How To
All set up is handled through config.ini files.
The default config looks like this:
```
[directories]

[columns]
Name = 
Count = 1
Text =
```

[directories](#directories) and [columns](#columns) are explained further down.

All of these can be modified through a file named "custom_config.ini". "default_config.ini" should not be changed, as it can not be assured you won't lose any changes there.  
An example custom_config.ini:
```
[directories]
item_deck = C:\Obsidian\Game\Item Cards
enemy_deck = C:\Obsidian\Game\Enemy

[columns]
Count = 2
Elements = 

[item_deck.columns]
Value = 0
Type = @Dir
Actions = 

[enemy_deck.columns]
Health = 0
Actions = 0
```
**[directories]** and **[columns]** both make a return here. Any changes to matching key/values in custom_config.ini will override the original in default_config.ini.

## [directories]
Any key/value pairs listed in this section will be loaded as a new CSV. The key is the name of the CSV, while the value is an absolute path to the directory. Any number(well, until Python thinks it's too many) can be assigned and loaded.

## [columns]
Every key/value in this section will be loaded as a piece of data for the CSV. The key is the name of the column, always set to lower case regardless of casing here, and the value is the default value to assign to it.  
A few are set in default_config.ini for convenience:
- Name is a built in tag that will be set to the name of the file
- Count can be used with nanDECK's LINKMULTI directive to set the number of copies of that card in the deck
- Text is the found card description. [Explained further down.](#card-text)

These can be freely added and changed, even per a directory/deck. Anything under [columns] will apply to _every_ deck, while anything under [deckname.columns] will only apply to that deck.  
custom_config's [columns] will override default_config, which will in turn be overriden by [deckname.columns]. Only listed columns will be overriden, anything else will remain to what was previously set.

@Dir is a special built in value. If the value is set to this, the column name will still be the key. However, the column's value will be set to the folder the found file resides in. Example being, if "Super Cool Bad Guy" exists in directory "C:\Obsidian\Game\Enemy", then it will be set to "Enemy".

## Formatting the Markdown
Only defined information will be loaded from the .MD files, so to allow you to store information and ideas in the same space.  
Step 1, is leading the file with an "#include". **Any files not containing this in the very first line will be ignored and passed by.** The first line may also contain anything else but MUST contain #include. Obsidian uses leading hash for it's tagging system, so it's borrowed here.

After that, the rest may be whatever you want. Keep your thoughts about the cards, assign values, the world is yours.

The previously mentioned [columns] can be set anywhere here.  
Example:
```
>Health: 20
```
A leading ">" means it should attempt to load that line as a column value. Anything between the bracket and semicolon is the column name, case insensitive. Anything after the semicolon will be assigned to that column, any leading or trailing whitespace is trimmed so the space is optional. You can also use this to per-card set the number of them by setting the value of "Count", the default value assigned earlier.

### Card Text
At the END of the file, the line "# Card Text" can be used. Once read to, the **rest** of the file will be assigned to the previously mentioned "Text" value in [columns].  
Important details:
- Currently, it only supports using the HTMLTEXT directive in nanDECK. New lines are replaced with \<br> HTML tags. Found <h> header tags are trimmed of white space/new lines and NOT replaced with a \<br> since header tags already do a new line.
- This will go until the end of the file. So if you don't want something as the card text, this must be the LAST section.

## Creating the CSVs
Once your config is set up and markdown files formatted all that's left is to run the script.
Just open the console in this directory and run
```
py csv_creator.py
```
to create all your brand new CSV files. They will be created in the same directory as csv_creator.py. Use LINK in nanDECK and enjoy!

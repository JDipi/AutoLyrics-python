# AutoLyrics-python

### By JDipi
___

Python script that scrapes lyrics from Genius.com or Azlyrics.com and writes them to mp3 files

### [Better, GUI version made with Electron!](https://github.com/JDipi/AutoLyrics)

## Installation

1. Download the repo
2. Navigate to the downloaded repo, open cmd and run `pip install -r requirements.txt`
3. When that finishes run the script by doing `python lyrics.py` with the below requirements...

Example command: `python lyrics.py --titleMode file --dir "C:\Users\turtl\OneDrive\Desktop\test music\radiohead" --src genius`

## Arguments:
 - **-h** *Show a help message*
 - **--titleMode** *Method the script uses to find the name of the song to search for on Genius or Azlyrics*
   - **"manual"** *If the name of the song exists in the filename*
   - **"file"** *If the name of the song exists in the metadata "title" tag*
   - **"entry"** *If the above two don't apply or if you just want to manually type each file name to search for*
 - **--dir** *Path to the folder which contains the mp3 files you want to rename*
 - **--src** *The source to get lyrics from*
   - **genius** *Genius.com (usually more reliable)*
   - **azlyrics** *Azlyrics.com*

## Screenshots

<p align="center">
  General CLI
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/48573618/202013948-b4a865e3-8f92-4cf9-8b63-638f75d44cb8.png" width="700" />
</p>

<p align="center">
  "Manual" naming mode
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/48573618/202016040-31736e13-d968-4216-8a3c-98704b71f9b6.png" width="700" />
</p>

<p align="center">
  "Entry" naming mode
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/48573618/202016354-2ccb9244-d77c-4b57-a6f5-08282c8fce42.png" width="700" />
</p>

## Known issues (that I'll eventually fix)
- Script crashes when there is a non-mp3 file in the directory
- Error handling for bad user input may not work in all cases, I tried to cover them all
- I might add a mode where it scans all subdirectories of the supplied directory for mp3 files rather than only staying on the 0th level

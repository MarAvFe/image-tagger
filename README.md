Quick Image Tagger
===

Allows to easily classify cluttered image folders into keep/delete folders.

## Requirements

- `PIL`
- `tkinter`
- `pyinstaller`

## Create executable

Run:
```
$ pyinstaller --onefile tagger.py
```
And your executable will be in:
```
/dist/tagger
```

## TODOS

+ Add "Next" and "Previous" buttons for browsing (handle error when going back to classified image)
- Add previews for 5 next images and 5 previous
+ Print in UI the path being worked on.
+ Add resposiveness
- Modify GUI layout: 2 side buttons with "next" and "back". Set "keep" and "delete" buttons below. Make "browse" beautiful
- General refactoring of code (it do be a little disorganized)

# Final Project for CSC 664 Multimedia at SFSU
## Mtg card comparer: Group 8 Aaron Jacobson, Kevin Wei

### Intro
Hi! This project is the final project for Prof. Rahul Singh's Multimedia class at SFSU. Our goal was to create an application which can tell the differences between Magic: the Gathering cards. The basic idea of this project is you can take a file of Magic cards (from [mtgjson](https://www.mtgjson.com)) and transform it into another file which contains each card's "distance" from each other. This file can then be opened by an html page which will show all the cards and their distances from each other.

### How To
If all you want to do is look through the relationships of the included data on the html page no installation or software is required besides a modern browser. Just open up `app/diffGUI.html` page in your browser of choice. From there, opening any of the `*_results.json` pages by pressing the `Load Data` button will load them into the pages memory and then display them for you to see. If you click on an image it will display all the other cards in order from closest to farthest away along with their names and calculated distance. Please note that for large files (such as all the 2265 cards in the `StandardPrintings.json` file from mtgjson at the time of writing) this will take a few seconds to load and might be unstable enough to require refreshing a time or two two. (I haven't tried larger files, but I suspect they will crash pretty often or be slow enough to load to not be practically useable)

If you instead want to create your own files to browse based on the code above you will need to run `card_to_display_json.py` which will require you to have both python 3 installed on your machine and numpy. This should be run from the command line in some way like:
```sh
python3 scripts/card_to_display_json.py source_file prefix_for_output_files
```

As an example, to generate `train_results.json` and `train_results.npz` I ran `scripts/card_to_display_json.py data/train.json data/train_results`. This should work on any file of cards downloaded from mtgjson, though if your hope is to view them with the html GUI the cards will only have unique pictures if you use a file which has unique printings. (For instance the `StandardPrintings.json` file instead of the `StandardCards.json` file)

If you have python and numpy installed you can also use the `data_explorer.py` file, though I would suggest against it, since it is a simple command line tool and not very useful for data sets larger than about 20. It can be used to see the difference matrix generated for the training `.npz` file generated by `card_to_display_json.py` by running `data_explorer.py data/train_results.npz` and then entering `p` the "print" the matrix. One can also enter `dTrain` to see how far off this matrix was from the hand entered distances along with the total distance and total distance squared for all the relationships. The same can be done for the testing data just by running it on `data/test_results.npz` and using `dTest` instead.

The html page was written using [Elm](https://elm-lang.org/), a strictly typed functional programing language which (currently) transpiles to Javascript, so if you want to compile it yourself you'll need to [install elm](https://guide.elm-lang.org/install/elm.html). This project was written in 0.19.1, so I suggest installing that version to avoid any problems. Once you have elm installed you'll have to navigate to app folder in this project and then run the following command:
```sh
elm make src/Main.elm --output=diffGUI.html --optimize
```
This should make the html page which you should then be able to open like any other.

### File Explanations
#### app
This folder holds all the elm code which is used to create the GUI file. The source code can be found in `src`. `diffGUI.html` is the compiled page from all this code.

#### data
This folder contains all the data which was created for and is necessary for this project. `test.json` and `train.json` are the files which contain the card json for the training and testing sets. These were used to generate `train_results.npz`, `train_results.json`, `test_results.npz`, and `test_results.json`. `npz` stands for numpy zip and contain the feature matrix for each card along with their names, the names of all the features, and a difference matrix. This is the type of file which is opened by `data_explorer.py`. The `*_results.json` files have both a list of all the cards in the file and the difference matrix which is generated for the cards. This is the type of file which is used by `diffGUI.html`.

`train_diff_hand.txt` and `test_diff_hand.txt` are both files which contain the "ground truth" hand made difference matrices for their respective sets. These files aren't used in any scripts, but are saved here to maintain a copy.

If you are the preson grading this project then data will also have a `std_resuts.json` which is the text file created by running `card_to_display_json.py` on mtgjson's `StandardPrintings.json`. This can be displayed with `diffGui.html` to get an idea of what our project looks like for large numbers of cards. It is about 100 MB unzipped, so it will not be uploaded to github, but you can make it on your own.

#### scripts
This folder contains all the python code necessary to make the data files. `mat_processing.py` and `text_processing.py` are both files which contain the functions which make this code work. `text_processing.py` shares code with the file of the same name in [another MtG project](https://github.com/SudoSanauu/CSC620_FinalProject_MtgColor) I was working on at the same time, but `mat_processing.py` is specifically for this project. Because of the way python imports work this means that none of the other files will work if you move them out of this directory unless you take `mat_processing.py` and `text_processing.py` with them. `card_to_display_json.py` is the file which is used to generate the `.npz` and `.json` files mentioned above. `data_explorer.py` was a tool I developed before the GUI to examine my data. Its not really worth using, but I wanted to include it just in case.

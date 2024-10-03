Add email.csv to the root of the project to build a model.

**WordCompleter** provides several options to continue your prefix. It's logical and convenient as it can be unobvious how to choose only one. WordCompleter works quite accurate as to continue a word no context usually required, so we need only understand the structure of the language. There are some problems with endings (in languages like Russian it can be more crucial). It can be fixed with deep learning approach.

**WordSuggestion**. It's quite strange to predict lots of various n-length options so we'll choose one. The problem of n-gramm approach is it's limitations of what the model have seen. Increasing dataset helps but it can't be effectivly fixed without deep learning.

**Details**. Our app provides from 1 to 3 alternatives of current word completion and 1 n-size word suggestion based on the most probable word completion on each step. We build our model on only 10k emails and it works well (especially wordcompleter). We use ~2% of provided data to boost building time of the model. Using all data will enhance quality of word-suggester. **Reflex** usage to develop frontend and connect it with backend.

**Possible upgrades.** Some of them were mentioned in the upper sections. 

1. Use full dataset (expecting valuable quality growth on n-grams)
1. Use beam-search instead of gready prediction
1. DL usage (especially in a word suggester) 
1. Some highly specialized fetures (e.g. letter signature for emails)
1. Develop metrics to compare models. (most important :D)



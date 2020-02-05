# This is lyrics-analytics. 
A personal project of mine as an excuse to learn a wide range of skills and libraries.
The goal is to take what The Pudding, a data journalism site, did with their "Largest Vocabulary in Hip Hop" project and make it more interactive across any genre.
The project can be found at https://pudding.cool/projects/vocabulary/ .

How it works:
A user plugs in an artist they are interested in comparing.
Those inputs query the Spotify API for the artist's available discography.
That information is then plugged into Genius, the lyrics and music knowledge site to pull down all lyrics in the available discography.

Then the lyrics are cleaned using nltk to tokenize, remove stopwords, lemmatize, remove contractions etc. Once cleaned, the lyrics are run through a freqency distribution or ngram algorithm to find the most common words, bigrams, and trigrams in a artist's discography. 

That stuff is basically done.

What is to come:
Visualizing that analysis.
Creating a site to house all of this.
Setting up a backend server to store all the data thats pulled and analyzed either through DigitalOcean or PythonAnywhere.
Post photos of how this all works.
Write up the process so someone can replicate how to start a project like this.

Libraries Used:
pandas
nltk
requests
BeautifulSoup
Flask
re


Thanks for checking it out and please let me know if you've got any comments, questions, concerns, or confessions!

Cheers,
DK

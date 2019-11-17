# This is lyrics-analytics. 
A personal project of mine as an excuse to learn a wide range of skills and libraries.
The goal is to take what The Pudding, a data journalism site, did with their "Largest Vocabulary in Hip Hop" project and make it more interactive across any genre.
The project can be found at https://pudding.cool/projects/vocabulary/ .

How it works:
A user plugs in two artists they are interested in comparing.
Those inputs query the Spotify API for the artists available discography.
That information is then plugged into Genius, the lyrics and music knowledge site to pull down all lyrics in the available discography.

That stuff is basically done.

What is to come:
Actually cleaning the lyrics.
Running some natural language processing techniques to analyze bigrams, word frequencies etc.
Visualizing that analysis.
Creating a site to house all of this.
Setting up a backend server to store all the data thats pulled and analyzed.

Libraries Used:
pandas
nltk
requests
BeautifulSoup
Django
re


Thanks for checking it out and please let me know if you've got any comments, questions, concerns, or confessions!

Cheers,
DK

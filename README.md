# illustrAItion
**Vandyhacks V** project

By Ling Chen, Laura Colbran, and Ying Ji

## What is illustrAItion?
Have you ever had this great story that only lacked for illustrations, but were missing the will or desire to draw something? Despair no more, for we bring you **illustrAItion**, the AI-informed web tool for generating illustrations automatically. Simply enter the phrase you want to be sketched, and **illustrAItion** will assemble a matching picture from doodles generated as part of the Google QuickDraw experiment. **illustraAItion** currently support two languages, Chinese and English. 


## How It Works
### Doodle Data
**illustrAItion** is built on the back of a database assembled from doodles submitted via the Google Quick, Draw! game (`https://quickdraw.withgoogle.com/`). For this game, people are instructed to (quickly) draw the word that the game displays on the screen. The drawings were previously curated using a convolutional neural network to identify the best examples of each word, resulting in 340,000 high-quality (_or at least recognizable..._) doodles, each matched to their word. **N.B.** We do not consider the generation of this database part of **illustrAItion**, since it predates Vandyhacks V, and can be used for many other things as well.

### Frontend
We built the frontend of **illustrAItion** using the React JavaSript Library (`https://reactjs.org/`). It consists of a text box to enter your phrase, and a display area where the drawing is displayed. The drawing is animated using SVG paths assembled from the doodle database by the backend.

### Backend
The input and ouput of the API call is processed using the Django Python Library (`https://www.djangoproject.com/`). The typed phrase is processed into pairs of words connected by a positional preposition using either NLTK (`https://www.nltk.org/`) or SpaCy (`https://spacy.io/`). It then checks to make sure there is a drawing of each word in the doodle database. In the absence of one, it uses the Gensim library to fetch the most similar word. Once the individual drawing are pulled from the database in the form of SVG paths, these are combined such that the individual drawings are arranged to reflect the positional preposition connecting them. This combined path is then returned to the frontend for display.

## Challenges we ran into
- The spatial arrangement of more than two drawings (solved!)
- Converting NLP-generated trees to a more usable format (solved!)
- Support Chinese text inpu (solved!)
- Animating the drawing stroke by stroke (unsolved)

## Accomplishments that we're proud of
- We got a lot done this weekend, which is surprising given our complete lack of background in this area
- The current product looks like we imagined it
- We implemented bonus drawings hiding in the database! 
- Each other

## What we learned
- None of us knew anything about web development before planning this project
- We had not used natural language processing before either
- We learned the details of how SVGs work and how to generate them

## What's Next?
- Support for languages other than English
- Amazon Alexa voice-to-text-to-doodle
- Style transformation of the drawing to your favourite artistic style

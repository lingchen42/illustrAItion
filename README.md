# illustrAItion
<img src="https://github.com/lingchen42/illustrAItion/blob/master/frontend/src/assets/logo.svg" alt="logo" width="300"/>

A **Vandyhacks V** project by Ling Chen, Laura Colbran, and Ying Ji

## What is illustrAItion?
Have you ever had this great story that only lacked for illustrations, but were missing the will or desire to draw something? Despair no more, for we bring you **illustrAItion**, the AI-informed web tool for generating illustrations automatically. Simply enter the phrase you want to be sketched, and **illustrAItion** will assemble a matching picture from doodles generated as part of the Google QuickDraw experiment. **illustraAItion** currently support two languages, Chinese and English. 

## Demo
<p align="center">
  <img src="https://github.com/lingchen42/illustrAItion/blob/master/demo.gif" alt="logo" width="600"/>
</p>

## Install locally through conda environment.yml

1. Set up backend environment with Anaconda3 (https://www.anaconda.com/distribution/#download-section)
```
# enter the backend dir
cd backend 

# create an virtual environment with required packages
conda env create -f environment.yml

# activate the environment
source activate illustraition

# download requried dataset for language processing
python -m spacy download en
 
# Run backend server; it will load the word2vec model for ~30sec, then start server at http://127.0.0.1:8000/
python manage.py runserver
```

2. Set up frontend environment
```
# enter the frontend dir
cd ../frontend

# set npm to use python2
npm config set python python2.7   # it has to be python2

# install required packages
npm install

# run server
npm start  # http://localhost:3000/
```

3. The website will be alive at http://localhost:3000/ 


## Install locally manually
1. Install backend required python packages
```
Required packages:
django
djangorestframework
django-cors-headers
numpy
spacy
translate
nltk
gensim
pattern
```
2. Set up frontend environment
```
# enter the frontend dir
cd ../frontend

# set npm to use python2
npm config set python python2.7   # it has to be python2

# install required packages
npm install

# run server
npm start  # http://localhost:3000/
```


## How It Works
<p align="center">
  <img src="https://github.com/lingchen42/illustrAItion/blob/master/pipeline.png" width="800"/>
</p>

### Doodle Data
**illustrAItion** is built on the back of a database assembled from doodles submitted via the Google Quick, Draw! game (`https://quickdraw.withgoogle.com/`). For this game, people are instructed to (quickly) draw the word that the game displays on the screen. The drawings were previously curated using a convolutional neural network to identify the best examples of each word, resulting in 340,000 high-quality (_or at least recognizable..._) doodles, each matched to their word. **N.B.** We do not consider the generation of this database part of **illustrAItion**, since it predates Vandyhacks V, and can be used for many other things as well.

### Frontend
We built the frontend of **illustrAItion** using the React JavaSript Library (`https://reactjs.org/`). It consists of a text box to enter your phrase, and a display area where the drawing is displayed. The drawing is animated using SVG paths assembled from the doodle database by the backend.

### Backend
The input and ouput of the API call is processed using the Django Python Library (`https://www.djangoproject.com/`). The typed phrase is processed into pairs of words connected by a positional preposition using either NLTK (`https://www.nltk.org/`) or SpaCy (`https://spacy.io/`). It then checks to make sure there is a drawing of each word in the doodle database. In the absence of one, it uses the Gensim library to fetch the most similar word. Once the individual drawing are pulled from the database in the form of SVG paths, these are combined such that the individual drawings are arranged to reflect the positional preposition connecting them. This combined path is then returned to the frontend for display.

## What's Next?
- Support more languages
- Resize the objects for a better spatial arrangment
- Amazon Alexa voice-to-text-to-doodle
- Style transformation of the drawing to your favourite artistic style

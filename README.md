# illustrAItion
Project for Vandyhacks V
Ling Chen, Laura Colbran, and Ying Ji

Have you ever had this great story that only lacked for illustrations, but were missing the will or desire to draw something? Despair no more, for we bring you **illustrAItion**, the AI-informed web tool for generating illustrations automatically. Simply enter the phrase you want to be sketched, and **illustrAItion** will assemble a matching picture from doodles generated as part of the Google QuickDraw experiment. 

## The Doodles
**illustrAItion** is built on the back of a database assembled from doodles submitted via the Google Quick, Draw! game (`https://quickdraw.withgoogle.com/`). For this game, people are instructed to [quickly] draw the word that the game displays on the screen. The drawings were previously curated using a convolutional neural network to identify the best examples of each word, resulting in 340,000 high-quality (or at least recognizable...) doodles, each matched to their word. 

## Frontend (Pygame / react.js)
- React.js
  - SVG animation
  - UI design

## Backend
### Connect the backend server  <br>
Connect the local server to local run through
```
ssh -R 80:localhost:8000 ssh.localhost.run
```
Server will be available at `https://chenling.localhost.run/api/`
- Processing the API call
  - Sentence to words with positional information using NLTK
  - Use word2vec (gensim library) to fetch the closest object from database
  - Generate a plot (SVG paths) with object(s) arranged in a reasonable way
  - Return the plot as response

## Fun things to add
- Bonus SVGs triggered by words like Vanderbilt, Vandy, VH.
- Octocat + Vandy Hacks design

## Challenges I ran into
The spatial arrangement of objects.

## Accomplishments that I'm proud of

## What I learned

## What's Next?
- Support for languages other than English
- Amazon Alexa voice-to-text-to-doodle
- Style transformation to your favourite artistic style

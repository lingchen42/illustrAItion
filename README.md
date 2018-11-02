# Quick Draw Story
Project for Vandy hacks V


## Backend
### Connect the backend server through `https://chenling.localhost.run/api/` <br>
Connect the local server to local run through
```
ssh -R 80:localhost:8000 ssh.localhost.run
```
- Processing the API call
  - Sentence to words with positional information (Syntax Tree? Preposition of location?)
  - Use word2vec (gensim library) to fetch the closest object from database
  - Generate a plot (SVG pathes? PNG?) with object arrange in a reasonable way
  - Return the plot as response

## Frontend (Pygame / react.js)
- Pygame 
- React.js
  - SVG animation
  - UI design

## Major challenges
The spatial arrangement of objects.

## Fun things to add
- Language support
- Amazon Alexa control
- Style transformation of the final product (https://github.com/lengstrom/fast-style-transfer)

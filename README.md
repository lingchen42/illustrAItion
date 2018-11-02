# illustrAItrion
Project for Vandy hacks V


## Backend
### Connect the backend server  <br>
Connect the local server to local run through
```
ssh -R 80:localhost:8000 ssh.localhost.run
```
Server will be available at `https://chenling.localhost.run/api/`
- Processing the API call
  - Sentence to words with positional information (Syntax Tree? Preposition of location?) **Ying**
  - Use word2vec (gensim library) to fetch the closest object from database (Done)
  - Generate a plot (SVG pathes? PNG?) with object arrange in a reasonable way **Ying and Laura**
  - Return the plot as response **Laura**

## Frontend (Pygame / react.js)
- Pygame 
- React.js
  - SVG animation **Laura**
  - UI design **Ling**

## Major challenges
The spatial arrangement of objects.

## Fun things to add
- Bonus SVGs triggered by words like Vanderbilt, Vandy, VH. **Ling**
- Language support 
- Amazon Alexa control
- Style transformation of the final product (https://github.com/lengstrom/fast-style-transfer) **Laura**

## Maybe useful tutorials
- [using-voice-commands-to-control-a-website-with-amazon-echo-alexa](https://medium.com/@sjur/using-voice-commands-to-control-a-website-with-amazon-echo-alexa-part-2-6-966d596d80b0])
- [Embed SVG to React](https://stackoverflow.com/questions/23402542/embedding-svg-into-reactjs)
- [React fetch data async](https://github.com/reactjs/rfcs/issues/26)

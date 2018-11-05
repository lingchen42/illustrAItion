import React from 'react';
import ReactDOM from "react-dom";
import "./style.scss";
import Logo from "./logo.js"
import DrawArea from "./drawing.js"
import Input from "./input.js"


const API = "https://chenling.localhost.run/api/"

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputText: 'default',
      EnteredText: 'empty',
      strokes: []
    };
  }

  handleChangeValue = e => this.setState({inputText: e.target.value});

  handleKeyPress = e => {
    if (e.which === 13) {
      this.setState({EnteredText: this.state.inputText})
      try {
        var res = fetch(API+this.state.inputText);  
        res.then(response => {return response.json()}) 
          .then(strokes => {this.setState({strokes})})
      } catch (e) {
        console.log(e)
      }
    }
  }

  async componentDidMount() {
    try {
      var res = fetch(API+this.state.EnteredText); 
      res.then(response => {return response.json()})
         .then(strokes => {this.setState({strokes})})
     } catch (e) {
       console.log(e);
     }
  }

  render() {
    return (
      <div className='parentdiv'>
         <Logo />
         <Input
            id={1}
            label="Write something..."
            predicted=""
            locked={false}
            active={false}
            inputText={this.state.inputText}
            onChangeValue={this.handleChangeValue}
            onKeyPress={this.handleKeyPress}
          />
        <DrawArea svg_path={this.state.strokes} EnteredText={this.state.EnteredText} />
      </div>
    );
  }
}



ReactDOM.render(
  <App />,
  document.getElementById("root")
);

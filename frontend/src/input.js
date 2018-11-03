import React from 'react';

class Input extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        active: (props.locked && props.active) || false,
        error: props.error || "",
        label: props.label || "Label"
      };
    }
  
    render() {
      const { inputText } = this.props.inputText;
      const { active, error, label } = this.state;
      const { predicted, locked } = this.props;
      const fieldClassName = `field ${(locked ? active : active || inputText) &&
        "active"} ${locked && !active && "locked"}`;
  
      return (
        <div className={fieldClassName}>
          {active &&
            inputText &&
            predicted &&
            predicted.includes(inputText) && <p className="predicted">{predicted}</p>}
          <input
            id={1}
            type="text"
            inputText={inputText}
            placeholder={label}
            onChange={this.props.onChangeValue}
            onKeyPress={this.props.onKeyPress}
            onFocus={() => !locked && this.setState({ active: true })}
            onBlur={() => !locked && this.setState({ active: false })}
          />
          <label htmlFor={1} className={error && "error"}>
            {error || label}
          </label>
        </div>
      );
    }
  } 

  export default Input;
import React from 'react';
import MtSvgLines from 'react-mt-svg-lines';  
import SVG from 'react-inlinesvg';
import vandyhacklogo from './assets/vandyhack.logo.svg'


class DrawArea extends React.Component {
    state = {}

    _reset_path() {
        this.setState({profileOrError: true});
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        // Store prevUserId in state so we can compare when props change.
        // Clear out any previously-loaded user data (so we don't render stale stuff).
        console.log(nextProps.svg_path);
        console.log(prevState.svg_path);
        if (nextProps.svg_path !== prevState.svg_path) {
          return {
            svg_path: nextProps.svg_path,
            profileOrError: null,
          };
        }
    
        // No state update necessary
        return null;
    }

    componentDidMount() {
        // It's preferable in most cases to wait until after mounting to load data.
        // See below for a bit more context...
        this._reset_path();
        //this.setState({ offset: this.path.current.getTotalLength() });
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.profileOrError === null) {
          // At this point, we're in the "commit" phase, so it's safe to load the new data.
          this._reset_path();
          //this.setState({ offset: this.path.current.getTotalLength() });
        }
    }

    render() {
        if (this.state.profileOrError === null) {
            return (<div>loading...</div>);
        } 
        
        else {

            if (this.props.EnteredText.includes('hack') | this.props.EnteredText.includes('vand')) {
                return(          
                     <div className='hacklogo'>
                        <SVG className='hacklogosvg' src={vandyhacklogo}></SVG>
                    </div>
                    );
            } 
            
            else {
                return (
                    <div className='drawarea'>
                    <MtSvgLines animate={ true } duration={ 2000 }>
                        <svg className='drawsvg' x="0" y="0" viewBox="0 0 500 500" >
                            {/* <path d={this.state.svg_path}/> */}
                            {this.state.svg_path.map(item => (<path d={item} />))}
                        </svg>
                    </MtSvgLines>
                    </div>
                );
            }
        }
    }

  }

  export default DrawArea;
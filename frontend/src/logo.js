import React from 'react';
import SVG from 'react-inlinesvg';
import logosvg from './assets/logo.svg'


class Logo extends React.Component {
    render() {
        return(
            <div className='logo'>
                <SVG className='logosvg' src={logosvg}></SVG>
            </div>
        );
    }
}

export default Logo;
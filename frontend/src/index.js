import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { applyMiddleware, createStore } from 'redux';
import rootReducer from './reducers';
import { Provider } from 'react-redux';
import thunkMiddleware from 'redux-thunk';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';


const store = createStore(rootReducer, applyMiddleware(thunkMiddleware));

const theme = createMuiTheme({
    typography: {
        fontFamily: [
            'Poppins',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif'
        ].join(','),
    }
});

ReactDOM.render(


    <ThemeProvider theme={theme}>
        <Provider store={store}>
            <Router>
                <App />
            </Router>
        </Provider>
    </ThemeProvider>
    , document.getElementById('root')
);

serviceWorker.unregister();

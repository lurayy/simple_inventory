import React from 'react';
import './App.css';
import Index from './components';
import Login from './components/users/login';
import { BrowserRouter as Router, Switch , Route, Link} from 'react-router-dom';


function App() {
  return (
    <div className="App">
      <Router>
      <Link to='/'>
        Home
      </Link><br></br>
      <Link to='/login'>
        Login
      </Link>
        <Switch>
          <Route path='/login' component={Login}></Route>
          <Route path='/' exact component={Index} ></Route>
        </Switch>
        
      </Router>
    
    </div>
  );
}

export default App;

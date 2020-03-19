import React from 'react';
import './App.css';
import Index from './components';
import Login from './components/users/login';
import Logout from './components/users/logout';
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
      </Link><br></br>
      <Link to='/logout'>
      Logout
      </Link>
        <Switch>
          <Route path='/login' component={Login}></Route>
          <Route path='/logout' component={Logout}></Route>
          <Route path='/' exact component={Index} ></Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;

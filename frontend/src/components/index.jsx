import React, { Component } from 'react'
import {  connect } from 'react-redux';
// import { useSelector, useDispatch } from 'react-redux'
import { getCurrentUser } from '../api/user';
import { loggedIn } from '../actions';
import Login from './users/login';
import Logout from './users/logout';

import UserCreation from './users/userCreation';
import { BrowserRouter as Router, Switch , Route, Link} from 'react-router-dom';


class Index extends Component {
    
    async componentDidMount() { 
        var loading=true;
        console.log(loading)
        await getCurrentUser().then(data => {
            if (data['status'])
            {
                this.props.dispatch(loggedIn(data['user_data']))
            }
            loading = false
        })
    }

    render() {
        var log;
        if (this.props.user.isLoggedIn){
            log = <Link to='/logout'>Logout</Link>
          }
          else{
            log =  <Link to='/login'>Login</Link>
          }
      
        return (
            <div>
                <h1>Index page with nav bar and dashbaord</h1>
                <Router>
                    <Link to='/'>
                        Home
                    </Link><br></br>
                    {log}
                        <Switch>
                        <Route path='/login' component={Login}></Route>
                        <Route path='/logout' component={Logout}></Route>
                        <Route path='/create' component = {UserCreation}></Route>
                        </Switch>
                </Router>
            </div>
        )
    }
}

const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(Index)
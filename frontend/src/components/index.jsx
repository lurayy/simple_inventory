import React, { Component } from 'react'
import {  connect } from 'react-redux';
// import { useSelector, useDispatch } from 'react-redux'
import { getCurrentUser } from '../api/user';
import { loggedIn } from '../actions';
import Login from './users/login';
import Logout from './users/logout';

import UserCreation from './users/userCreation';
import { BrowserRouter as Router, Switch , Route, Link} from 'react-router-dom';
import Users from './users/users';
import Vendors from './inventory/vendors/vendors';


class Index extends Component {
    
    async componentDidMount() { 
        var loading=true;
        console.log(loading)
        //check redux data first
        await getCurrentUser().then(data => {
            if (data['status'])
            {
                this.props.dispatch(loggedIn(data['user_data']))
            }
        })
    }

    render() {
        var log;
        if (this.props.user.isLoggedIn){
            log = (
                    <div>
                        <Link to='/logout'>Logout</Link><br></br>
                        <Link to='/create'>Create New User</Link><br></br>
                        <Link to='/users'>Users</Link><br></br>
                        <h4>Inventory</h4>
                        <Link to='/vendors'>Vendors</Link><br></br>
                    </div>                    
                    )
          }
          else{
            log =  (
                <div>
                    <Link to='/login'>Login</Link>
                </div>
                
                )
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
                        <Route path='/users' component = {Users}></Route>
                        <Route path='/vendors' component = {Vendors}></Route>
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
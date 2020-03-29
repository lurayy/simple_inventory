import React, { Component } from 'react'
import {  connect } from 'react-redux';
// import { useSelector, useDispatch } from 'react-redux'
import { getCurrentUser } from '../api/user';
import { loggedIn } from '../actions';
import Login from './users/login';
import Logout from './users/logout';
import VendorCreation from './vendors/vendorCreation';
import UserCreation from './users/userCreation';
import { BrowserRouter as Router, Switch , Route, Link} from 'react-router-dom';
import Users from './users';
import Vendors from './vendors/index';
import swal from 'sweetalert';



class Index extends Component {
    constructor (props){
        super(props)
        this.state = {
            'loading':true
        }
    }
    async componentDidMount() { 
        await getCurrentUser().then(data => {
            if (data){
                if (data['status'])
                {
                    this.props.dispatch(loggedIn(data['user_data']))
                }
                this.state.loading=false
            }
            else{
                swal('Cannot connet to the server, make sure you have a stable internet connection.')
            }
        })
    }
    render() {
        var log;
        if (this.props.user.isLoggedIn){
            log = (
                    <div>
                        <Link to='/logout'>Logout</Link><br></br>
                        <Link to='/users'>Users</Link><br></br>
                        <Link to='/vendors'>Vendors</Link><br></br><br></br>
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
          var render_x
        // if(this.state.loading === false){
            render_x = <div>
            {/* <h1>Index page with nav bar and dashbaord</h1> */}
            <Router>
                <Link to='/'>
                    Home
                </Link><br></br>
                {log}
                    <Switch>
                    <Route path='/login' component={Login}></Route>
                    <Route path='/logout' component={Logout}></Route>
                    <Route path='/users/create' component = {UserCreation}></Route>
                    <Route path='/users' component = {Users}></Route>
                    <Route path='/vendors/create' component = {VendorCreation}></Route>
                    <Route path='/vendors' component = {Vendors}></Route>
                    </Switch>
            </Router>
        </div>
        // }
        // else{
        //     render_x = <h1>Loading</h1>
        // }
      
        return (
         <div>
             {render_x}
         </div>   
        )
    }
}

const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(Index)
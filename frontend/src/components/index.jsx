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
import Customers from './customer/index';
import CustomerCreation from './customer/customerCreation'
import swal from 'sweetalert';
import PurchaseOrders from './purchaseOrder/index'
import PurchaseOrderCreation from './purchaseOrder/purchaseOrderCreation'
import Invoices from './invoices/index';
import InvoiceCreation from './invoices/invoiceCreation';

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
                        <br></br>
                        <Link to='/vendors'>Vendors</Link><br></br>
                        <Link to='/customers'>Customers</Link><br></br>
                        <br></br>
                        <Link to='/purchaseorders'>Purchase Orders</Link><br></br>
                        <Link to='/invoices'>Invoices</Link><br></br>
                        <br></br>
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
            render_x = <div>
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
                    
                    <Route path='/customers/create' component = {CustomerCreation}></Route>
                    <Route path='/customers' component = {Customers}></Route>
                    <Route path='/purchaseorders/create' component = {PurchaseOrderCreation}></Route>
                    <Route path='/purchaseorders' component = {PurchaseOrders}></Route>
                    
                    <Route path='/invoices/create' component = {InvoiceCreation}></Route>
                    <Route path='/invoices' component = {Invoices}></Route>
                    
                    </Switch>
            </Router>
        </div>
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
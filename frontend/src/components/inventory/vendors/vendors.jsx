import React, { Component } from 'react'
import {  connect } from 'react-redux';
import { setVendors } from '../../../actions';
import { getVendors, getVendor } from '../../../api/inventory/vendorApi';


class Vendors extends Component {

    async componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        var dummy = {
            'action':'get',
            'filter':'none',
            'start':0,
            'end':10
        }
        await getVendors(JSON.stringify(dummy)).then(data => {
            console.log(data)
            if (data['status']){
                this.props.dispatch(setVendors(data['vendors']))
            }  
        })

        
        //get single user
        dummy = {
            'action':'get',
            'vendor_id':2,
        }
        await getVendor(JSON.stringify(dummy)).then(data => {
            console.log(data)
        })
        // access props with this 
        // console.log(this.props.users)
}

    render() {
        return (
            <div>
                <h1>Vendors list</h1>
            </div>
        )
    }
}



const mapStateToProps = state => ({
    user: state.user,
    users: state.users
})

export default connect(mapStateToProps)(Vendors)
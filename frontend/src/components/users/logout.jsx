import React, { Component } from 'react'
import { logoutUser } from '../../api/user';
import {  connect } from 'react-redux';
import { logout } from '../../actions';


class Logout extends Component {
    componentDidMount(){
        logoutUser().then(res => {
            this.props.dispatch(logout())
            this.props.history.push('/')

        });
    }

    render() {
        return (
            <div>
            </div>
        )
    }
}

export default connect()(Logout)
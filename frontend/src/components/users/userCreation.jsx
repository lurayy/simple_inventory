import React, { Component } from 'react'
// import { isLoggedIn, permission} from '../common.jsx'
import {  connect } from 'react-redux';


class UserCreation extends Component {

    componentDidMount() {

    }

    render() {
        return (
            <div>
                <h1>Create New User</h1>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(UserCreation)
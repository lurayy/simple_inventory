import React, { Component } from 'react'
import {  connect } from 'react-redux';


class UserCreation extends Component {

    componentDidMount() {
        if (!this.props.user.isLoggedIn){
            this.props.history.push('/')
        }
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
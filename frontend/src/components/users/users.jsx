import React, { Component } from 'react'
import { getUsers, getUser } from '../../api/user'
import {  connect } from 'react-redux';
import { setUsers } from '../../actions';


class Users extends Component {


    async componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        console.log(this.props.user.data.user_type)
        if (this.props.user.data.user_type !== "MANAGER"){
            this.props.history.push('/')
        }
        var dummy = {
            'action':'get',
            'start':0,
            'end':20
        }
        await getUsers(JSON.stringify(dummy)).then(data => {
            console.log(data)
            if (data['status']){
                this.props.dispatch(setUsers(data['users']))
            }  
        })

        
        //get single user
        dummy = {
            'action':'get',
            'user_id':2,
            'uuid':"c08c318e-4157-4426-97e3-1d0366400b86"
        }
        await getUser(JSON.stringify(dummy)).then(data => {
            console.log(data)
        })
    }

    render() {
        return (
            <div>
                <h1>Users </h1>
            </div>
        )
    }
}



const mapStateToProps = state => ({
    user: state.user,
    users: state.users
})

export default connect(mapStateToProps)(Users)
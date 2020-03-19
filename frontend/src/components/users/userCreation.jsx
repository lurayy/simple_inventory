import React, { Component } from 'react'
import {  connect } from 'react-redux';
import { createUser } from '../../api/user';


class UserCreation extends Component {

    constructor (props){
        super(props)
        
        this.onSubmit = this.onSubmit.bind(this);
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        console.log(this.props.user.data.user_type)
        if (this.props.user.data.user_type !== "MANAGER"){
            this.props.history.push('/')
        }
    }


    async onSubmit(e){
        e.preventDefault();
        var dummy_data = { 
            'password': "password234",
            'username': "someuser",
            'first_name': "somename",
            'last_name': "somelast",
            'email':"somemail",
            'user_type': 'manager',
        }
        createUser(JSON.stringify(dummy_data)).then(data=> {
            try { 
                if (data['status']){
                    alert("New User Created")
                }
                else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
            }
        })
    }

    render() {
        return (
            <div>
                <h1>Create New User</h1>
                <form onSubmit={this.onSubmit}>
                    <div>
                        </div>
                    <br></br>
                    <div>
                        </div><br></br>
                    <button type='submit'>Submit</button>
                </form>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(UserCreation)
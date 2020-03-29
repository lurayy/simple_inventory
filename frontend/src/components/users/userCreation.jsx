import React, { Component } from 'react'
import {  connect } from 'react-redux';
import { createUser } from '../../api/user';
import {Button, TextField } from '@material-ui/core';


class UserCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'udpate':{}
        }
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        if (this.props.user.data.user_type !== "MANAGER"){
            this.props.history.push('/')
        }
    }

    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value]
            }
        })
    }


    async onSubmit(e){
        e.preventDefault();
        if (this.state.update.password[0] === this.state.update.password2[0]){
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            createUser(JSON.stringify(data)).then(data=> {
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
        else {
            alert("Password didn't match")
        }
    }

    render() {
        return (
            <div>
                <h1>Create New User</h1>
                <form onSubmit={this.onSubmit}>
                            First Name: <TextField
                                id ='first_name'
                                name="first_name"
                                type='text'
                                onChange={this.onChange}  
                                required                  
                            />
                            Last Name<TextField
                                id ='last_name'
                                name="last_name"
                                type='text'
                                onChange={this.onChange}
                                required 
                            />
                            
                            <br></br>
                             Username :<TextField
                             
                                id ='username'
                                name="username"
                                type='text'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            Password <TextField
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="current-password"
                                onChange={this.onChange}
                                required 
                                />
                               Confirm Password <TextField
                                id="password2"
                                type="password"
                                name="password2"
                                autoComplete="current-password"
                                onChange={this.onChange}
                                required 
                                />
                                <br></br>
                            Email : <TextField
                                id ='email'
                                name="email"
                                type='email'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            User Post:
                            <select name='user_type' id="user_type" onChange={this.onChange} defaultValue="STAFF">
                                <option value="MANAGER">Manager</option>
                                <option value="STAFF">Staff</option>
                            </select>
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button>
                        
                </form>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(UserCreation)
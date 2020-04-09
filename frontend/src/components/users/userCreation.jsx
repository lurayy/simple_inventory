import React, { Component } from 'react'
import {  connect } from 'react-redux';
import { createUser } from '../../api/user';
import {Button, TextField, Grid } from '@material-ui/core';
import Swal from 'sweetalert2'


class UserCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'update':{
                'user_type':'STAFF'
            }
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
        if (this.state.update.password[0] === this.state.update.password2[0]){
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            createUser(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire("New User Created")
                    }
                    else{
                        Swal.fire(data['error'])
                    }
                }catch(e){
                    console.log(e)
                }
            })
        }
        else {
            Swal.fire("Password didn't match")
        }
    }

    render() {
        return (
            <div>
                <Grid container justify='center'>
                    <Grid item xm ={6}>

                    <h1>Create New User</h1><br></br>
                    <table cellSpacing={10}  cellPadding={10}>
                        <tbody>
                            <tr>
                                <td>
                                    First Name: <TextField
                                    id ='first_name'
                                    name="first_name"
                                    type='text'
                                    onChange={this.onChange}  
                                    required                  
                                />
                                </td>
                                <td>
                                    Last Name<TextField
                                    id ='last_name'
                                    name="last_name"
                                    type='text'
                                    onChange={this.onChange}
                                    required 
                                />
                                </td>
                            </tr>

                            <tr>
                                <td>
                                Username :<TextField
                                
                                id ='username'
                                name="username"
                                type='text'
                                onChange={this.onChange}
                                required 
                            />
                                </td>
                            </tr>
                            
                            <tr>
                                <td>
                                Password <TextField
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="current-password"
                                onChange={this.onChange}
                                required 
                                />
                                </td>
                                <td>
                                Confirm Password <TextField
                                id="password2"
                                type="password"
                                name="password2"
                                autoComplete="current-password"
                                onChange={this.onChange}
                                required 
                                />
                                </td>
                            </tr>
                            <tr>
                                <td>
                            Email : <TextField
                                id ='email'
                                name="email"
                                type='email'
                                onChange={this.onChange}
                                required 
                            />
                            </td>
                            <td>
                            User Post:
                            <select name='user_type' id="user_type" onChange={this.onChange} value={this.state.update.user_type}>
                                <option value="MANAGER">Manager</option>
                                <option value="STAFF">Staff</option>
                            </select>
                            </td>
                            </tr>
                            <td>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                onClick={this.onSubmit}
                                >
                                Update
                                </Button>
                            </td>

                        </tbody>

                    </table>

                    </Grid>

                </Grid>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(UserCreation)
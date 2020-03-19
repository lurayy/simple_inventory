import React, { Component } from 'react';
import { loginUser, getCurrentUser } from '../../api/user';
import {  connect } from 'react-redux';
import { loggedIn } from '../../actions';


class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            username:'',
            password:'',
        };
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(e)
    {
        this.setState({[e.target.name]: [e.target.value]})
    }


    async onSubmit(e){
        e.preventDefault();
        const data = {
            username: this.state.username[0],
            password: this.state.password[0]
        }
        loginUser(JSON.stringify(data)).then(data => {
            try{
                if (data['status']){
                    getCurrentUser().then(data => {
                        this.props.dispatch(loggedIn(data['user_data']))
                    })
                    this.props.history.push('/')
                }
                else if (data['status']=== false){
                    alert(data['msg'])
                }
            }catch(e){
                alert(e)
            }
        })       
    }


    render() {
        return (
            <div>
                <h1>Login</h1>
                <form onSubmit={this.onSubmit}>
                    <div>
                        <label> Username : </label>
                        <input type='text' name='username' onChange={this.onChange} value={this.state.username}></input>
                    </div>
                    <br></br>
                    <div>
                        <label> Password : </label>
                        <input type='password' name='password' onChange={this.onChange} value={this.state.password}></input>
                    </div><br></br>
                    <button type='submit'>Submit</button>
                </form>
                {this.props.state}
            </div>
        )
    }
}

const mapStateToProps = state => ({
    user_state: state
})

export default connect(mapStateToProps)(Login)
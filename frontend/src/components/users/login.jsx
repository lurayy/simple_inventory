import React, { Component } from 'react';
import swal from 'sweetalert';
import { loginUser } from '../../api/user';

class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            username:'',
            password:'',
            token : '',
        };
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.outputData = this.outputData.bind(this)
    }
    onChange(e)
    {
        this.setState({[e.target.name]: [e.target.value]})
    }

    onSubmit(e){
        e.preventDefault();
        const data = {
            username: this.state.username[0],
            password: this.state.password[0]
        }
        
        console.log(data)
        
    loginUser(JSON.stringify(data)).then(data => console.log(data))
    
    }

    outputData(data){
        if (data.status){
            console.log('logined')
        }
        else{
            console.log(data)
            swal(data)
        }
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
            </div>
        )
    }
}


export default Login
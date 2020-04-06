import React, { Component } from 'react';
import { loginUser, getCurrentUser } from '../../api/user';
import {  connect } from 'react-redux';
import { loggedIn } from '../../actions';

//material-ui import button
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';

import Alert from '@material-ui/lab/Alert';

class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            username:'',
            password:'',
            status:'',
        };
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }
    componentDidMount() {
        if (this.props.current_state.user.isLoggedIn === true){
          window.location.href="/"
        }
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
                    window.location.href="/"
                  }else if ((this.state.username==="" && this.state.password==="")|
                (this.state.username==="" || this.state.password==="")){
                        this.setState((state) => {
                            return {status: "Username and password empty"};
                          });
                }
                else if (data['status']=== false){
                    this.setState((state) => {
                        return {status: data['msg']};
                      });
                }
            }catch(e){
                alert(e)
            }
        })       
    }

    render() {
      
        return (
            <Container component="main" maxWidth="xs">
                
                <CssBaseline />
                <div>
                  <Avatar style={{padding:30,margin:'auto',backgroundColor:'#1a237e'}} >
                    <h3>O</h3>
                  </Avatar>
                  {/* <Typography component="h1" variant="h4" style={{textAlign:'center'}}>
                    LOGIN
                  </Typography> */}
                  <form  onSubmit={this.onSubmit} noValidate>
                    <TextField
                      variant="outlined"
                      margin="normal"
                      fullWidth
                      id="uname"
                      label="Username"
                      name="username"
                      autoComplete="email"
                      autoFocus
                      type='text'
                      onChange={this.onChange}
                      value={this.state.username}
                    />
                    {/* required */}
                    <TextField
                      variant="outlined"
                      margin="normal"
                      fullWidth
                      name="password"
                      label="Password"
                      type="password"
                      id="password"
                      autoComplete="current-password"
                      onChange={this.onChange}
                      value={this.state.password}
                    />
                    <FormControlLabel
                      control={<Checkbox value="remember" color="primary" />}
                      label="Remember me"
                    />
                    <Button
                      type='submit'
                      fullWidth
                      variant="contained"
                      color="primary"
                    >
                      Login
                    </Button>
                    <br/><br/>
                    <Alert severity="error" style={{display: this.state.status ? "":'none'}}>
                        {this.state.status}
                    </Alert>

                    <Grid container>
                      {/* <Grid item xs>
                        <Link href="#" variant="body2">
                          Forgot password?
                        </Link>
                      </Grid> */}
                      {/* <Grid item>
                        <Link href="#" variant="body2">
                          {"Don't have an account? Sign Up"}
                        </Link>
                      </Grid> */}
                    </Grid>
                  </form>
                </div>
                <Box mt={8}>
                  {/* <Copyright /> */}
                </Box>
              </Container>
        )
    }
}

const mapStateToProps = state => ({
    current_state: state
})

export default connect(mapStateToProps)(Login)
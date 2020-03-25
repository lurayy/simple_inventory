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
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

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
    componentDidMount() {
        if (this.props.current_state.user.isLoggedIn === true){
            this.props.history.push('/')
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
        const useStyles = makeStyles((theme) => ({
            paper: {
              marginTop: theme.spacing(8),
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            },
            avatar: {
              margin: theme.spacing(1),
              backgroundColor: theme.palette.secondary.main,
            },
            form: {
              width: '100%', // Fix IE 11 issue.
              marginTop: theme.spacing(1),
            },
            submit: {
              margin: theme.spacing(3, 0, 2),
            },
          }));
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
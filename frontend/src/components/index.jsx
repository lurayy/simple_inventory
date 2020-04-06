import React, { Component } from 'react'
import {  connect } from 'react-redux';
import { getCurrentUser } from '../api/user';
import { loggedIn } from '../actions';
import swal from 'sweetalert';
import Dashboard from './dashboard'
import LoadingIcon from './loading'
import Login from './users/login'

class Index extends Component {
    constructor (props){
        super(props)
        this.state = {
            'loading':true
        }
    }
    
    

    async componentDidMount() { 
        await getCurrentUser().then(data => {
            if (data){
              
              console.log(data)
                if (data['status'])
                {
                    this.props.dispatch(loggedIn(data['user_data']))
                }
                this.setState({
                  'loading':false
                })
            }
            else{
                swal('Cannot connet to the server, make sure you have a stable internet connection.')
            }
        })
    }
    render() {
        var render_x=<LoadingIcon></LoadingIcon>;
        if(this.state.loading){
          render_x = <LoadingIcon></LoadingIcon>
        }
        else{
          if (this.props.user.isLoggedIn){
            render_x = <Dashboard></Dashboard>
          }
          else{
            render_x = <Login></Login>
          }
        }
        
        return (
          <div>
            {render_x}
          </div>
          
        )
    }
}

const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(Index)
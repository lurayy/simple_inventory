import React, { Component } from 'react'
import List from '../list';
import { getUser, updateUser } from '../../api/user';
import {Button, TextField, Grid } from '@material-ui/core';

import Swal from 'sweetalert2'
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';


class UserList extends Component {
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'user_data':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }
    
    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value][0]
            }
        })
    }

    onSubmit(){
        var data = this.state.update;
        data = {
            ...data,
            'action':'edit',
            'user_id':data.id
        }
        updateUser(JSON.stringify(data)).then(data =>{
            if (data['status']){
                Swal.fire(
                    'Updated!',
                    'Details has been updated.',
                    'success'
                  )                
                  this.props.update(0)
            }
        })
    }

    userDelete(id,uuid){
        var data = {
            'action':'delete',
            'user_id':id,
            'uuid':uuid
        }
        updateUser(JSON.stringify(data)).then(data =>{
            if (data['status']){
                Swal.fire('User has been deleted. They cannot login now')
                this.props.update(0)
            }
        })
    }

    
    userRevive(id,uuid){
        var data = {
            'action':'revive',
            'user_id':id,
            'uuid':uuid
        }
        updateUser(JSON.stringify(data)).then(data =>{
            if (data['status']){
                Swal.fire('User has been made active. They login now')
                this.props.update(0)
            }
        })
    }

    async popUp(id, uuid=0){
        const data = {
            'action':'get',
            'user_id':id,
            'uuid':uuid
        }
        var data_main;
        await getUser(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'user_data':data_main,
            'update':data_main
        })
    }

    columns = [
        {
            id:1,
            name:"Name",
            prop: 'name'
        },
        {
            id:2,
            name:"Post",
            prop: 'status'
        },
        {
            id:3,
            name:"Username",
            prop: 'username'
        },
        {
            id:4,
            name:"Status",
            prop: 'is_active_str'
        }      
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns} popUp={this.popUp} update={this.props.update} page={this.props.page}/>
        const popUpRender = 
        
        
        <div>
             <Grid  container spacing={3} justify="center" alignContent='center' alignItems="center">
        
        <Grid item xm={4}>
        <Button  variant="contained" size='small' color="primary" onClick={()=> {this.setState({...this.state, popUp:false})}}>
            <ArrowLeftIcon></ArrowLeftIcon>
     Back
 </Button>          <h1>{this.state.user_data.name}</h1>
        &nbsp;
        &nbsp;
        &nbsp;
        &nbsp;
        &nbsp;
        &nbsp; 
        
        </Grid>
        <Grid item xm={4}>
        </Grid>
    </Grid>

            
    <Grid container  justify="center" alignContent='center' alignItems="center">
        <Grid item xm={6}>
        <table cellPadding={10} cellSpacing={10}>
            <tbody>
                <tr>
                    <td>
                        
                First Name : <TextField
                                id ='first_name'
                                name="first_name"
                                type='text'
                                onChange={this.onChange}
                                value={this.state.update.first_name}                       
                            />
                            
                    </td>
                    <td>

                            
                    Last Name : <TextField
                            
                            id ='last_name'
                            name="last_name"

                            // placeholder = {this.state.user_data.last_name}   
                            type='text'
                            onChange={this.onChange}
                            value={this.state.update.last_name}                       
                        />
                       
                    </td>
                </tr>
                <tr>
                    <td>
                    Username :<TextField
                             
                             id ='username'

                             name="username"
                            //  placeholder = {this.state.user_data.username}   
                             type='text'
                             onChange={this.onChange}
                             value={this.state.update.username}                       
                         />
                    </td>
                <td>
                Email : <TextField
                                id ='email'
                                name="email"
                                // placeholder = {this.state.user_data.email}   
                                type='email'
                                onChange={this.onChange}
                                value={this.state.update.email}                       
                            />
                </td>

                </tr>
                <tr>
                    <td>
                    User Post:
                            <select name='user_type' onChange={this.onChange} defaultValue={this.state.user_data.user_type}>
                                <option value="MANAGER">Manager</option>
                                <option value="STAFF">Staff</option>
                            </select>
                    </td>
                </tr>
<tr>
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
    <td>
    {this.state.user_data.is_active ? <Button variant="contained" color="secondary" onClick={() => {this.userDelete(this.state.user_data.id, this.state.user_data.uuid)}}>
                            Deactivate User
                        </Button> : <Button variant="contained" color="secondary" onClick={() => {this.userRevive(this.state.user_data.id, this.state.user_data.uuid)}}>
                            Activate User
                        </Button> }
                        
    </td>
</tr>

            </tbody>
        </table>
                            
                            
                       
                        <br>
                        </br>
                        </Grid>
                        </Grid>
                    </div>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default  UserList
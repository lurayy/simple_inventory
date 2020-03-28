import React, { Component } from 'react'
import List from '../list';
import { getUser, updateUser } from '../../api/user';
import {Button, TextField } from '@material-ui/core';
import {swal} from 'sweetalert';

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
                [e.target.name] : [e.target.value]
            }
        })
        console.log(this.state)
    }

    onSubmit(e){
        e.preventDefault();
        var data = this.state.user_data;
        var ele;
        for (ele in data){
            if (this.state.update[ele]){
                data[ele] = this.state.update[ele][0]
            }
        }
        data = {
            ...data,
            'action':'edit',
            'user_id':data.id
        }
        updateUser(JSON.stringify(data)).then(data =>{
            if (data['status']){
                alert('You Details has been updated.')
                this.props.update(0)
            }
        })
    }


    async popUp(id, uuid=0){
        console.log(id, uuid)
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
            'user_data':data_main
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
            name:"Status",
            prop: 'status'
        },
        {
            id:3,
            name:"Username",
            prop: 'username'
        }            
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns} popUp={this.popUp} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.user_data.name}</h1>

                        <form onSubmit={this.onSubmit}>
                            First Name : <TextField
                                id ='first_name'
                                name="first_name"
                                placeholder = {this.state.user_data.first_name}   
                                type='text'
                                onChange={this.onChange}
                                // value={this.state.update.first_name}                       
                            />
                            
                            Last Name : <TextField
                            
                                id ='last_name'
                                name="last_name"

                                placeholder = {this.state.user_data.last_name}   
                                type='text'
                                onChange={this.onChange}
                                // value={this.state.update.last_name}                       
                            />
                            
                            <br></br>
                             Username :<TextField
                             
                                id ='username'

                                name="username"
                                placeholder = {this.state.user_data.username}   
                                type='text'
                                onChange={this.onChange}
                                // value={this.state.update.username}                       
                            />
                            <br></br>
                            Email : <TextField
                                id ='email'
                                name="email"
                                placeholder = {this.state.user_data.email}   
                                type='email'
                                onChange={this.onChange}
                                // value={this.state.update.email}                       
                            />
                            <br></br>
                            User Post:
                            <select name='user_type' onChange={this.onChange} defaultValue={this.state.user_data.user_type}>
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
                        <br>
                        </br>
                        <Button variant="contained" color="secondary" onClick={() => {this.userDelete(this.state.user_data.id, this.state.user_data.uuid)}}>
                            Delete This User
                        </Button>
                        <br>
                        </br>
                    </div>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default  UserList
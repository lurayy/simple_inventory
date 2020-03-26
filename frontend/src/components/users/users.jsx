import React, { Component } from 'react'
import { getUsers } from '../../api/user'
import {  connect } from 'react-redux';
import List from '../list';


class Users extends Component {

    constructor(props){
        super(props)
        this.state = {
            'users':[],
            'loaded':false
        }
        this.update_table = this.update_table.bind(this)
    }


    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        if (this.props.user.data.user_type !== "MANAGER"){
            this.props.history.push('/')
        }
            
    }

    async getUsersData (request_json) {
        await getUsers(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                console.log(data)
                this.setState({
                    'users':data['users'],
                    'loaded':true
                })
            }  
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
    

    update_table () {
        this.setState({
            'loaded':false
        })
        console.log("updating")
        var  request_json = {
            'action':'get',
            'filter':'none',
            'start':0,
            'end':5
        }
        this.getUsersData(request_json)
    }
    render() {
        return(
            <div>
                <button onClick={this.update_table}>Update table</button>
                {this.state.loaded ? <List data={this.state.users} header={this.columns} /> : "Loading..."}
            </div>
        )
}
}


const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Users)
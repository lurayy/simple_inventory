import React, { Component } from 'react'
import { getUsers } from '../../api/user'
import {  connect } from 'react-redux';
import List from '../list';


class Users extends Component {

    constructor(props){
        super(props)
        this.state = {
            'users':[],
            'loaded':false,
            'start':0,
            'end':5
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
    

    update_table (by) {
        if (this.state.start+by>0){
            this.setState({
                'loaded':false,
                start: this.state.start+by,
                end: this.state.end+by
            })
        }
        else{
            alert("Cannot move futher from here.")
            return
        }
        
        console.log("updating ",this.state.start, this.state.end)
        var  request_json = {
            'action':'get',
            'filter':'none',
            'start':this.state.start,
            'end':this.state.end
        }
        this.getUsersData(request_json)
    }

    render() {
        
        const render_after_load = (
            <div>
                <h1>Table</h1>
                {console.log("state",this.state.users)}
                <List data={this.state.users} header={this.columns} />
                <button onClick={() => {this.update_table(-5)}}>Pervious</button><button onClick={() => {this.update_table(5)}}>Next</button>
            </div>
        )
        return(
            <div>
                <button onClick={() => {this.update_table(5)}}>Refresh table</button>
                {this.state.loaded ? render_after_load : "Loading..."}
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Users)
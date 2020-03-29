import React, { Component } from 'react'
import { getUsers } from '../../api/user'
import {  connect } from 'react-redux';
import UserList from './userList';
import { Link} from 'react-router-dom';

class Users extends Component {

    constructor(props){
        super(props)
        this.state = {
            'users':[],
            'loaded':false,
            'start':0,
            'end':10,
            'page':1
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
                this.setState({
                    'users':data['users'],
                    'loaded':true
                })
            }  
        })
    }

    async update_table (by) {
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                'loaded':false,
                start: 0,
                end: 10,
                page:1
            })
        }
        else{
            if (this.state.start+by>-1){
                await this.setState({
                    'loaded':false,
                    start: this.state.start+by,
                    end: this.state.end+by,
                    page:this.state.page+x
                })
            }
            else{
                alert("Cannot move futher from here.")
                return
            }
        }
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
                <UserList data={this.state.users} update={this.update_table} page={this.state.page} />
            </div>
        )

        return(
            <div>
                <Link to='users/create'>Create New User</Link><br></br>
                <button onClick={() => {this.update_table(0)}}>Refresh table</button>
                {this.state.loaded ? render_after_load : "Loading..."}

            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Users)
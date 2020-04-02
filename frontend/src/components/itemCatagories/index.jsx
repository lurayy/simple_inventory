import React, { Component } from 'react'
import {getItemCatagories} from '../../api//inventory/itemCatagory';
import {  connect } from 'react-redux';
import  ItemCatagoryList  from './itemCatagoryList';
import { Link} from 'react-router-dom';

class ItemCatagories extends Component {
    constructor(props){
        super(props)
        this.state = {
            'items':[],
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
        this.getItemCatagoriesData(request_json)
    }
    
    async getItemCatagoriesData (request_json) {
        await getItemCatagories(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'item_catagories':data['item_catagories'],
                    'loaded':true
                })
            }  
        })
    }

 

render() {
    const render_after_load = (
        <div>
            <ItemCatagoryList data={this.state.item_catagories} update={this.update_table} page={this.state.page} />
        </div>
    )

    return(
        <div>
            <Link to='/itemcatagories/create'>Add New Item Catagroy</Link><br></br>
            <button onClick={() => {this.update_table(0)}}>Refresh table</button><br></br>
            {this.state.loaded ? render_after_load : "Loading..."}
        </div>
    )
}
}




const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(ItemCatagories)
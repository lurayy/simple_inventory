import React, { Component } from 'react'
import {getVendors} from '../../api/inventory/vendorApi';
import {  connect } from 'react-redux';
import  VendorList  from './vendorList';

class Vendors extends Component {
    constructor(props){
        super(props)
        this.state = {
            'vendors':[],
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
        this.getVendorsData(request_json)
    }
    
    async getVendorsData (request_json) {
        await getVendors(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'vendors':data['vendors'],
                    'loaded':true
                })
            }  
        })
    }

 

render() {
    const render_after_load = (
        <div>
            <VendorList data={this.state.vendors} update={this.update_table} page={this.state.page} />
        </div>
    )

    return(
        <div>
            <button onClick={() => {this.update_table(0)}}>Refresh table</button>
            {this.state.loaded ? render_after_load : "Loading..."}

        </div>
    )
}
}




const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Vendors)
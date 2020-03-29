import React, { Component } from 'react'
import {getPurchaseOrders} from '../../api/inventory/purchaseOrder';
import {  connect } from 'react-redux';
import  PurchaseOrderList  from './purchaseOrderList';
import { Link} from 'react-router-dom';

class PurchaseOrders extends Component {
    constructor(props){
        super(props)
        this.state = {
            'purchaseOrders':[],
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
        this.getPurchaseOrdersData(request_json)
    }
    
    async getPurchaseOrdersData (request_json) {
        await getPurchaseOrders(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                console.log("data: ",data)
                this.setState({
                    'purchaseOrders':data['p_orders'],
                    'loaded':true
                })
            }  
        })
    }

 

render() {
    const render_after_load = (
        <div>
            <PurchaseOrderList data={this.state.purchaseOrders} update={this.update_table} page={this.state.page} />
        </div>
    )

    return(
        <div>
            <Link to='/purchaseorders/create'>Create New Purchase Order</Link><br></br>
            <button onClick={() => {this.update_table(0)}}>Refresh table</button><br></br>
            {this.state.loaded ? render_after_load : "Loading..."}

        </div>
    )
}
}




const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(PurchaseOrders)
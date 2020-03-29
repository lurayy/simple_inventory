import React, { Component } from 'react'
import List from '../list';
import {Button, TextField } from '@material-ui/core';
import { getPurchaseOrder, deletePurchaseOrder, updatePurchaseOrder } from '../../api/inventory/purchaseOrder';
import popUpEdit from './popUpEdit';
import PopUpEdit from './popUpEdit';

class PurchaseOrderList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'purchase_order':{},
            'purchase_items':[],
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.vendorDelete = this.vendorDelete.bind(this)
    }
    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value]
            }
        })
    }

    
    async onSubmit(e){
        e.preventDefault();
            var data = this.state.vendor
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit'}
            updatePurchaseOrder(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Vendor Data updated.")
                        this.props.update(0)
                    }
                    else{
                        alert(data['error'])
                    }
                }catch(e){
                    console.log(e)
                }
            })
    }

    vendorDelete(id){
        var data = {
            'vendors_id':[
                id
            ]
        }
        deletePurchaseOrder(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Vendor data deleted.')
                    this.props.update(0)
                }   else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
            }
        })
    }
    
    async popUp(id, uuid=0){
        const data = {
            'action':'get',
            'purchase_order_id':id,
        }
        var data_main;
        await getPurchaseOrder(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'purchase_order':data_main['p_order'][0],
            'purchase_items':data_main['p_items']
        })
    }


    columns = [
        {
            id:1,
            name:"Vendor Name",
            prop: 'vendor_name'
        },
        {
            id:2,
            name:"Items",
            prop: 'items'
        },
        {
            id:3,
            name:"Invoiced On",
            prop: 'invoiced_on'
        },
        {
            id:4,
            name:"Total Cost",
            prop: 'total_cost'
        },   
        {
            id:5,
            name:"Status",
            prop: 'status_name'
        }      
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <PopUpEdit purchase_order={this.state.purchase_order} purchase_items={this.state.purchase_items} ></PopUpEdit>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default PurchaseOrderList

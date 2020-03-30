import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from './css/popUp.module.css';
import {getVendors} from '../../api/inventory/vendorApi';


class PopUpEdit extends Component {
    constructor(props){
        super(props)
        this.state = {
            'vendor_selection':[
                {
                    'id':0,
                    'name':'Type Name To Search'
                }
            ],
            update : {
                'purchase_order':this.props.purchase_order,
                'purchase_items':this.props.purchase_items
            }
        }
        this.getVendorsData = this.getVendorsData.bind(this)
        this.converter = this.converter.bind(this)
        this.popUp = this.popUp.bind(this)
        this.searchVendor = this.searchVendor.bind(this)
        this.selectVendor = this.selectVendor.bind(this)
    }

    async getVendorsData (request_json) {
        await getVendors(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'vendor_selection':data['vendors'],
                })
            }  
        })
    }


    selectVendor(id,name){
        this.setState({
            'update': {
                ...this.state.update,
                'purchase_order':{
                    ...this.state.update.purchase_order,
                    'vendor':id,
                    'vendor_name':name
                }
            }
        })
    }


 

    handleChange = date => {
        console.log(typeof(date))
        var data = {'date':date}
        console.log(JSON.stringify(data))
    };
    converter(date){
        console.log(Date.parse(date))
        return (Date.parse(date))
    }

    popUp(id){
        console.log(id)
    }

    searchVendor(e){
        console.log(e.target.value)
        if ((e.target.value).length > 2 ){
            var request_json = {
                'action':'get',
                'start':0,
                'end':10,
                'filter':'name',
                'first_name':(e.target.value)
            }
            this.getVendorsData(request_json)
        }
    }
    
    columns = [
        {
            id:1,
            name:"Item Name",
            prop: 'item_name'
        },
        {
            id:2,
            name:"Quantity",
            prop: 'quantity'
        },
        {
            id:3,
            name:"Stock",
            prop: 'stock'
        },
        {
            id:4,
            name:"Defective",
            prop: 'defective'
        },   
        {
            id:5,
            name:"Sold",
            prop: 'sold'
        },
        {
            id:6,
            name:"Discount",
            prop: 'discount'
        },
        {
            id:7,
            name:"Purchase Price",
            prop: 'purchase_price'
        },
        {
            id:8,
            name:"Status",
            prop: 'status'
        }
    ]

    render() {
        console.log(this.state)
        const vendor_selection = this.state.vendor_selection
        const vendorPopup = <Popup trigger={<button>Change Vendor</button>} closeOnDocumentClick>
                <div>
                    <input placeholder="Vendor's first name" id='vendor_serach_box' name='vendor_serach_box' onChange={this.searchVendor}></input>
                    <div className={style.dropdown_content} id='vendor_dropdown'>
                            {vendor_selection.map(
                                vendor => (
                                    <a key={vendor.id} onClick={() => {this.selectVendor(vendor.id, vendor.name)}} >{vendor.name}</a>
                                )
                            )
                            }
                        
                    </div>
                </div>
            </Popup>
        return (
            <div>
                <h1>Purchase Order</h1>
                <h1>{this.props.purchase_order.vendor_name}</h1>
                Vendor : {this.state.update.purchase_order.vendor_name}
                {vendorPopup}<br></br>
                Invoiced On : 
                <DatePicker
                selected={this.converter(this.state.update.purchase_order.invoiced_on)}
                onChange={this.handleChange}
                />
                Completed On : 
                <DatePicker
                selected={this.converter(this.state.update.purchase_order.completed_on)}
                onChange={this.handleChange}
                /><br></br>
                Added By : {this.state.update.purchase_order.added_by_name}<br></br>
                Total Cost : <input placeholder={this.state.update.purchase_order.total_cost} /><br></br>
                Discount Type : {this.state.update.purchase_order.discount_type} <button>Change Discount Type</button><br></br>
                Discount : <input placeholder={this.state.update.purchase_order.discount}></input><br></br>
                Status : {this.state.update.purchase_order.status_name} <button>Change Status</button><br></br>

                <h3>Items</h3>
                <List data={this.props.purchase_items} header={this.columns} page={false} popUp={this.popUp} />
            </div>
        )
    }
}
export default PopUpEdit
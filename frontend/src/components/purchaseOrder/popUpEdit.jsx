import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from './css/popUp.module.css';
class PopUpEdit extends Component {
    constructor(props){
        super(props)
        this.state = {
            update : {
                'purchase_order':this.props.purchase_order,
                'purchase_items':this.props.purchase_items
            }
        }
        this.converter = this.converter.bind(this)
        this.popUp = this.popUp.bind(this)
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

    selectVendor(){


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
        const vendorPopup = <Popup trigger={<button>Change Vendor</button>}>
            <div>
                <div>
                    <input placeholder="Vendor's first name"></input>
                    <div className={style.dropdown_content} id='vendor_dropdown'>
                        <div class={style.loader} id='loader-id'>

                        </div>
                    </div>
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
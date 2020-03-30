import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from './css/popUp.module.css';
import {getVendors} from '../../api/inventory/vendorApi';

import {updatePurchaseOrder} from '../../api/inventory/purchaseOrder';
import {updatePurchaseItem, deletePurchaseItems} from '../../api/inventory/purchaseItem'
import {getPurchaseOrderStatus} from '../../api/misc';

class PopUpEdit extends Component {
    constructor(props){
        super(props)
        this.state = {
            'popUp':false,
            'current':0,
            'status':[],
            'vendor_selection':[
                {
                    'id':0,
                    'name':'Type Name To Search'
                }
            ],
            update : {
                'purchase_order':{
                    ...this.props.purchase_order,
                    'invoiced_on': this.converter(this.props.purchase_order.invoiced_on),
                    'completed_on': this.converter(this.props.purchase_order.completed_on)
                },
                'purchase_items':this.props.purchase_items
            }
        }
        this.invoiceHandler = this.invoiceHandler.bind(this)
        this.completeHandler = this.completeHandler.bind(this)
        this.getVendorsData = this.getVendorsData.bind(this)
        this.converter = this.converter.bind(this)
        this.popUp = this.popUp.bind(this)
        this.searchVendor = this.searchVendor.bind(this)
        this.selectVendor = this.selectVendor.bind(this)
        this.onChange = this.onChange.bind(this)
        this.updatePurchaseOrder = this.updatePurchaseOrder.bind(this)
        this.onChangePI = this.onChangePI.bind(this)
        this.postPurchaseItem = this.postPurchaseItem.bind(this)
        this.deletePurchaseItem = this.deletePurchaseItem.bind(this)
    }


    async componentDidMount(){
        var request_json = {
            'action':'get',
        }
        await getPurchaseOrderStatus(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    ...this.state,
                    'status':data.data
                })
            }  
        })
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

    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                'purchase_order':{
                    ...this.state.update.purchase_order,
                    [e.target.name] : [e.target.value][0]
                }
            }
        })
    }

    converter(date){
        return ( new Date(Date.parse(date)))
    }
    popUp(id){
        var key
        for (key in this.state.update.purchase_items){
            if (this.state.update.purchase_items[key].id === id){
                this.setState({
                    ...this.state,
                    'current':key,
                    'popUp':true
                })        
                return
            }
        }
        
    }

    searchVendor(e){
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
    
    invoiceHandler(date){
        this.setState({
            'update': {
                ...this.state.update,
                'purchase_order':{
                    ...this.state.update.purchase_order,
                    'invoiced_on' : date
                }
            }
        })
    }
    
    completeHandler(date){
        this.setState({
            'update': {
                ...this.state.update,
                'purchase_order':{
                    ...this.state.update.purchase_order,
                    'completed_on' : date
                }
            }
        })
    }

    updatePurchaseOrder(){
        var request_json = {
            ...this.state.update.purchase_order,
            'action':'edit',
            'purchase_order_id':this.state.update.purchase_order.id
        }
        updatePurchaseOrder(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Purchase Order Details Has Been Updated.")
            }
            else{
                alert("Error : ",data.error)
            }
        })
    }


    onChangePI(e){
        this.setState({
            'update': {
                ...this.state.update,
                'purchase_items':{
                    ...this.state.update.purchase_items,
                    [this.state.current] : {
                        ...this.state.update.purchase_items[this.state.current],
                        [e.target.name] : [e.target.value][0]
                    },
                }
            }
        })
    }

    postPurchaseItem(){
        console.log(this.state.update.purchase_items[this.state.current])
        var request_json = {
            'action':'edit',
            ...this.state.update.purchase_items[this.state.current]
        }
        console.log(request_json)
        updatePurchaseItem(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Purchase Item Details Has Been Updated.")
                this.setState({
                    'popUp':false
                })
            }
            else{
                console.log(data)
                alert(data['error'])
            }
        })
        
    }

    deletePurchaseItem(){
        var request_json = {
            purchase_items_id : [this.state.update.purchase_items[this.state.current].id]
        }
        deletePurchaseItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Purchase Item Has Beed Deleted.")
                this.setState({
                    'popUp':false
                })
            }
            else{
                console.log(data)
                alert(data['error'])
            }
        })
        
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
        const popUpItem = <div>
            <button onClick={() => {this.setState({'popUp':false})}} >Back</button><br></br><br></br>
            Item : {this.state.update.purchase_items[this.state.current].item_name} <br></br>
            Quantity : <input name="quantity" placeholder={this.state.update.purchase_items[this.state.current].quantity} type="number" onChange={this.onChangePI}></input><br></br>
            Defective : <input name="defective" placeholder={this.state.update.purchase_items[this.state.current].defective} type="number"  onChange={this.onChangePI}></input><br></br>
            
            Discount Type :<select name='discount_type' id="discount_type" defaultValue={this.state.update.purchase_items[this.state.current].discount_type}  onChange={this.onChangePI}>
                                <option value="percent">Percentage</option>
                                <option value="fixed">Fixed</option>
                            </select> <br></br>
            Discount : <input placeholder={this.state.update.purchase_items[this.state.current].discount} name="discount" onChange={this.onChangePI} ></input><br></br>
            Purchase Price : <input placeholder={this.state.update.purchase_items[this.state.current].purchase_price} name="purchase_price" onChange={this.onChangePI}></input> <br></br>
            Status : <select defaultValue= {this.state.update.purchase_items[this.state.current].status} name="status" onChange={this.onChangePI}>
                <option value="delivered">Delivered</option>
                <option value="incomplete">Incomplete</option>
                <option value="addedtocirculation">Added To Circulation</option>
            </select><br></br>
            <button onClick={() => {this.postPurchaseItem()}} >Update</button><br></br><br></br>
            <button onClick={() => {this.deletePurchaseItem()}} >Delete</button>


        </div>

        const vendor_selection = this.state.vendor_selection
        const vendorPopup = <Popup trigger={<button>Change Vendor</button>} closeOnDocumentClick>
                <div>
                    <input placeholder="Vendor's first name" id='vendor_serach_box' name='vendor_serach_box' onChange={this.searchVendor}></input>
                    <div className={style.dropdown_content} id='vendor_dropdown'>
                            {vendor_selection.map(
                                vendor => (
                                    // use css to get rid of <a>
                                    <a key={vendor.id} onClick={() => {this.selectVendor(vendor.id, vendor.name)}} >{vendor.name}</a>
                                )
                            )
                            }
                        
                    </div>
                </div>
            </Popup>
            const status = this.state.status
            console.log(this.state.update.purchase_order.status)
        return (
            <div>
                <h1>Purchase Order</h1>
                <h1>{this.props.purchase_order.vendor_name}</h1>
                Vendor : {this.state.update.purchase_order.vendor_name}
                {vendorPopup}<br></br>
                Invoiced On : 
                <DatePicker
                name='invoiced_on'
                selected={this.state.update.purchase_order.invoiced_on}
                onChange={this.invoiceHandler}
                />
                Completed On : 
                <DatePicker
                name='completed_on'
                selected={this.state.update.purchase_order.completed_on}
                onChange={this.completeHandler}
                /><br></br>
                Added By : {this.state.update.purchase_order.added_by_name}<br></br>
                Total Cost : <input placeholder={this.state.update.purchase_order.total_cost} name="total_cost" onChange={this.onChange}/><br></br>
                Discount Type :<select name='discount_type' id="discount_type" onChange={this.onChange} defaultValue={this.state.update.purchase_order.discount_type}>
                                <option value="percent">Percentage</option>
                                <option value="fixed">Fixed</option>
                            </select> <br></br>
                Discount : <input placeholder={this.state.update.purchase_order.discount} name="discount" onChange={this.onChange}></input><br></br>
                Status : <select name='status' id="status" onChange={this.onChange} value={this.state.update.purchase_order.status}  >
                                {status.map(
                                    x => (
                                    <option key={x.id} value={parseInt(x.id)}>{x.name}</option>
                                    )
                                )
                                }
                            </select> <br></br><br></br>
                <button onClick={() => {this.updatePurchaseOrder()}}>Update Purchase Order</button>
                <h3>Items</h3>
                {this.state.popUp ? popUpItem :<List data={this.props.purchase_items} header={this.columns} page={false} popUp={this.popUp} /> }  
            </div>
        )
    }
}
export default PopUpEdit
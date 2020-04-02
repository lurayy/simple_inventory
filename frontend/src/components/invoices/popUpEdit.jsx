import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from '../purchaseOrder/css/popUp.module.css';
import {getCustomers} from '../../api/sales/customer';
import {updateInvoice, getInvoice, deleteInvoices, getInvoiceStatus} from '../../api/sales/invoice';
import {updateInvoiceItem, deleteInvoiceItems, createInvoiceItem} from '../../api/sales/invoiceItem'
import {getItems} from '../../api/inventory/itemApi';
import {getPlaces} from '../../api/inventory/placeApi';

class PopUpEdit extends Component {

    constructor(props){
        super(props)
        this.state = {
            'place_selection':[],
            'stock_selection':[],
            'sold_from_selection':[],
            'popUp':false,
            'new':false,
            'current':0,
            'status':[],
            'customer_selection':[
                {
                    'id':0,
                    'name':'None'
                }
            ],
            'item_selection':[
                {
                    'id':0,
                    'name':"None"
                }
            ],
            update : {
                'invoice':{
                    ...this.props.invoice,
                    'invoiced_on': this.converter(this.props.invoice.invoiced_on),
                    'due_on': this.converter(this.props.invoice.due_on)
                },
                'invoice_items':this.props.invoice_items
            }
        }
        this.stateman = this.stateman.bind(this)
        this.refreshTable = this.refreshTable.bind(this)
        this.getItemData = this.getItemData.bind(this)
        this.selectItem = this.selectItem.bind(this)
        this.searchItem = this.searchItem.bind(this)
        this.addInvoiceItem = this.addInvoiceItem.bind(this)
        this.invoiceHandler = this.invoiceHandler.bind(this)
        this.dueOnHandler = this.dueOnHandler.bind(this)
        this.getCustomerData = this.getCustomerData.bind(this)
        this.converter = this.converter.bind(this)
        this.popUp = this.popUp.bind(this)
        this.searchCustomer = this.searchCustomer.bind(this)
        this.selectCustomer = this.selectCustomer.bind(this)
        this.onChange = this.onChange.bind(this)
        this.updateInvoice = this.updateInvoice.bind(this)
        this.onChangePI = this.onChangePI.bind(this)
        this.postInvoiceItem = this.postInvoiceItem.bind(this)
        this.deleteInvoiceItem = this.deleteInvoiceItem.bind(this)
        this.onChangePlace = this.onChangePlace.bind(this)
    }


    async componentDidMount(){
        var request_json = {
            'action':'get',
        }
        await getInvoiceStatus(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    ...this.state,
                    'status':data.data
                })
            }  
        })
    }

    async getCustomerData (request_json) {
        await getCustomers(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'customer_selection':data['customers'],
                })
            }  
        })
    }

    selectCustomer(id,name){
        this.setState({
            'update': {
                ...this.state.update,
                'invoice':{
                    ...this.state.update.invoice,
                    'customer':id,
                    'customer_name':name
                }
            }
        })
    }

    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                'invoice':{
                    ...this.state.update.invoice,
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
        for (key in this.state.update.invoice_items){
            if (this.state.update.invoice_items[key].id === id){
                this.setState({
                    ...this.state,
                    'current':key,
                    'popUp':true
                }) 
                break;       
            }
        }
        var request_json = {
            'action':'get',
            'filter':'item',
            'item_id':this.state.update.invoice_items[key].id  
        }
        this.getPlacesData(request_json)
    }

    async getPlacesData(request_json) {
        await getPlaces(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'sold_from_selection':data['placements'],
                })
                var temp = [], key, x;
                for(key in data['placements']){
                    x = {'id': data['placements'][key]['placed_on'], 'str_placed_on':data['placements'][key]['str_placed_on']}
                    temp[data['placements'][key]['placed_on']] = x
                    }
                temp = temp.filter(function (el) {
                    return el != null;
                });
                this.setState({
                    'place_selection':temp
                })

                var temp=[],p,inv;
                for (p in data['placements']){
                    if ( this.state.update.invoice_items[this.state.current]['sold_from'] === data['placements'][p]['placed_on']){
                        var string  = data['placements'][p]['purchase_item_details']['purchase_price'] + "/-  " + data['placements'][p]['purchase_item_details']['quantity'] + " " + data['placements'][p]['purchase_item_details']['vendor'] 
                        temp.push({
                            'id': data['placements'][p]['purchase_item'],
                            'str':string
                        })
                    }
                    
                }
                this.setState({
                    ...this.state,
                    'stock_selection': temp
                })
        
            }  
        })
    }

    onChangePlace(e){
        this.setState({
            'update': {
                ...this.state.update,
                'invoice_items':{
                    ...this.state.update.invoice_items,
                    [this.state.current] : {
                        ...this.state.update.invoice_items[this.state.current],
                        [e.target.name] : [e.target.value][0]
                    },
                }
            }
        })
        var temp=[],p;
                for (p in this.state.sold_from_selection){
                    if ( this.state.update.invoice_items[this.state.current]['sold_from'] === this.state.sold_from_selection[p]['placed_on']){
                        var string  = this.state.sold_from_selection[p]['purchase_item_details']['purchase_price'] + "/-  " + this.state.sold_from_selection[p]['purchase_item_details']['quantity'] + " " + this.state.sold_from_selection[p]['purchase_item_details']['vendor'] 
                        temp.push({
                            'id': this.state.sold_from_selection[p]['purchase_item'],
                            'str':string
                        })
                    }
                    
                }
                this.setState({
                    ...this.state,
                    'stock_selection': temp
                }) 
    }

    searchCustomer(e){
        if ((e.target.value).length > 2 ){
            var request_json = {
                'action':'get',
                'start':0,
                'end':10,
                'filter':'name',
                'name':(e.target.value)
            }
            this.getCustomerData(request_json)
        }
    }
    
    invoiceHandler(date){
        this.setState({
            'update': {
                ...this.state.update,
                'invoice':{
                    ...this.state.update.invoice,
                    'invoiced_on' : date
                }
            }
        })
    }
    
    dueOnHandler(date){
        this.setState({
            'update': {
                ...this.state.update,
                'invoice':{
                    ...this.state.update.invoice,
                    'due_on' : date
                }
            }
        })
    }

    updateInvoice(){
        var request_json = {
            ...this.state.update.invoice,
            'action':'edit',
            'invoice_id':this.state.update.invoice.id
        }
        updateInvoice(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Invoice Details Has Been Updated.")
                this.props.update(0)
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
                'invoice_items':{
                    ...this.state.update.invoice_items,
                    [this.state.current] : {
                        ...this.state.update.invoice_items[this.state.current],
                        [e.target.name] : [e.target.value][0]
                    },
                }
            }
        })
    }

    postInvoiceItem(is_new=false){
        var request_json
        if (is_new){
            request_json = {
                'action':'add',
                'invoice':this.state.update.invoice.id,
                ...this.state.update.invoice_items[this.state.current]
            }
            console.log("new",request_json)
            // createInvoiceItem(JSON.stringify(request_json)).then(data => {
            //     if (data['status']){
            //         alert("Invoice Item Has Been Added.")
            //         this.refreshTable()
            //     }
            //     else{
            //         alert(data['error'])
            //     }
            // })
            return
        }
        request_json = {
            'action':'edit',
            ...this.state.update.invoice_items[this.state.current]
        }
        console.log('odl',request_json)
        // updateInvoiceItem(JSON.stringify(request_json)).then(data => {
        //     if (data['status']){
        //         alert("Invoice Item Details Has Been Updated.")
        //         this.refreshTable()
        //     }
        //     else{
        //         alert(data['error'])
        //     }
        // })
    }

    deleteInvoiceItem(){
        var request_json = {
            invoice_items_id : [this.state.update.invoice_items[this.state.current].id]
        }
        deleteInvoiceItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Invoice Item Has Beed Deleted.")
                this.refreshTable()
            }
            else{
                alert(data['error'])
            }
        })
    }


    addInvoiceItem(){
        var current =0;
        var item,p_list=[];
        for (item in this.state.update.invoice_items){
            if (item.id){
                if (item.id !== "Fake Key"){
                    current = current + 1
                    p_list.push(item)
                }
            }
        }
        this.setState({
            'current':current,
            'new':true,
            'popUp':true,
            'update':{
                ...this.state.update,
                'invoice_items':[
                    ...p_list,
                    {
                        'item_name':"None",
                        'discount_type':'percentage',
                        'status':'incomplete'
                    }
                ]
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
            id:8,
            name:"Price",
            prop: 'price'
        },
        {
            id:3,
            name:"Sold From",
            prop: 'sold_from_name'
        },
        {
            id:4,
            name:"Tax Total",
            prop: 'tax_total'
        },
        ,
        {
            id:5,
            name:"Disount Amount",
            prop: 'discount_amount'
        },   
        {
            id:6,
            name:"Sub Total",
            prop: 'sub_total'
        },
        {
            id:7,
            name:"Total",
            prop: 'total'
        }
    ]

    searchItem(e){
        if ((e.target.value).length > 2 ){
            var request_json = {
                'action':'get',
                'start':0,
                'end':10,
                'filter':'name',
                'name':(e.target.value)
            }
            this.getItemData(request_json)
        }
    }

    async getItemData(request_json){
        await getItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    ...this.state,
                    'item_selection':data['items'],
                })
            }  
        })
    }
    selectItem(id, name){
        this.setState({
            'update': {
                ...this.state.update,
                'invoice_items':{
                    ...this.state.update.invoice_items,
                    [this.state.current] : {
                        ...this.state.update.invoice_items[this.state.current],
                        'item_name' : name,
                        'item':id
                    },
                }
            }
        })
        var request_json = {
            'action':'get',
            'filter':'item',
            'item_id':id
        }
        this.getPlacesData(request_json)
    }

    async refreshTable(){
        var id = this.state.update.invoice.id;
        var items= [];
        const request_json = {
            'action':'get',
            'invoice_id':id
        }
        await getInvoice(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                items = data['invoice_items']
            }
        })
        if (items.length === 0){
            items = [{
                'id':"Fake Key",
                'item_name': ''
            }]
        }
        await this.setState({
            ...this.state,
            'popUp':false,
            'update':{
                ...this.state.update,
                'invoice_items':items
            }
        })
    }


    stateman(){
        console.log(this.state)
    }

    render() {
        const item_selection = this.state.item_selection
        const itemPopUp = <Popup trigger={ <button>Select Item</button>} closeOnDocumentClick>
        <div>
            <input placeholder="Item Name" id='item_search_box' name='item_serach_box' onChange={this.searchItem}></input>
            <div className={style.dropdown_content} id='item_dropdown'>
                    {item_selection.map(
                        item => (
                            // use css to get rid of <a>
                        <a key={item.id} onClick={() => {this.selectItem(item.id, item.name)}} >{item.name} {item.sales_price}</a>
                        )
                    )}
            </div>
        </div>
        </Popup>

        var places = this.state.place_selection
        const selectPlace =<select name='sold_from' id="sold_from" onChange={this.onChangePlace} value={this.state.update.invoice_items[this.state.current].sold_from}  >
                {places.map(
                    x => (
                    <option key={x.id} value={parseInt(x.id)}>{x.str_placed_on}</option>
                    )
                )}
            </select>

            
        var stocks  = this.state.stock_selection
        var stockValue = this.state.update.invoice_items[this.state.current].purchase_item ? this.state.update.invoice_items[this.state.current].purchase_item : ''
        const selectStock =<select name='purchase_item' id="purchase_item" onChange={this.onChangePI} value={stockValue} >
                <option key='Fake Key' value='0'>Select Stock</option>
                {stocks.map(
                    x => (
                    <option key={x.id} value={parseInt(x.id)}>{x.str}</option>
                    )
                )}
            </select>


        const popUpItem = <div>
                <button onClick={() => {this.refreshTable()}} >Back</button><br></br><br></br>
                Item : {this.state.update.invoice_items[this.state.current].item_name}  {itemPopUp}<br></br>
                Sold From: 
                Place : {this.state.update.invoice_items[this.state.current].item ? selectPlace : "Select An Item First" } <br></br>
                Stock :   {this.state.update.invoice_items[this.state.current].item ? selectStock : "Select An Item First" } <br></br>
                <br></br>

                Quantity : <input name="quantity" placeholder={this.state.update.invoice_items[this.state.current].quantity} type="number" onChange={this.onChangePI} required min='1' ></input><br></br>
                Price : <input name="price" placeholder={this.state.update.invoice_items[this.state.current].price} type="number" onChange={this.onChangePI} required></input><br></br>
                
                {this.state.new ? <button onClick={() => {this.postInvoiceItem(true)}} >Add</button> : <button onClick={() => {this.postInvoiceItem()}} >Update</button>}<br></br><br></br>
                <button onClick={() => {this.deleteInvoiceItem()}} >Delete</button>
            </div>
        const customer_selection = this.state.customer_selection
        const customerPopup = <Popup trigger={<button>Change Customer</button>} closeOnDocumentClick>
        <div>
            <input placeholder="Customer's first name" id='customer_serach_box' name='customer_serach_box' onChange={this.searchCustomer}></input>
            <div className={style.dropdown_content} id='customer_dropdown'>
                    {customer_selection.map(
                        customer => (
                            <a href="#" key={customer.id} onClick={() => {this.selectCustomer(customer.id, customer.name)}} >{customer.name}</a>
                        )
                    )}
            </div>
        </div>
        </Popup>
        const status = this.state.status
        return (
            <div>
                <h1>Invoice</h1>
        <h3>{this.state.update.invoice.customer_name} </h3>
                Added By : {this.state.update.invoice.added_by_name}<br></br>
                Customer : {this.state.update.invoice.customer_name} {customerPopup}<br></br>
                Order Number : {this.state.update.invoice.order_number}<br></br>
                <br></br><br></br>
                Invoiced On : 
                <DatePicker
                name='invoiced_on'
                selected={this.state.update.invoice.invoiced_on}
                onChange={this.invoiceHandler}
                />
                Due On : 
                <DatePicker
                name='completed_on'
                selected={this.state.update.invoice.due_on}
                onChange={this.dueOnHandler}
                /><br></br><br></br>
                
                Total Amount : {this.state.update.invoice.total_amount}<br></br>
                Total Tax : {this.state.update.invoice.tax_total}<br></br>
                Total Discount: {this.state.update.invoice.discount_total}<br></br>
                Paid Amount : {this.state.update.invoice.paid_amount}<br></br>

                <br></br>
                Additional Discount : <input placeholder={this.state.update.invoice.additional_discount} name='additional_discount' onChange={this.onChange} ></input>
                <br></br><br></br>

                
                Status : <select name='status' id="status" onChange={this.onChange} value={this.state.update.invoice.status}  >
                                {status.map(
                                    x => (
                                    <option key={x.id} value={parseInt(x.id)}>{x.name}</option>
                                    )
                                )}
                            </select> <br></br><br></br>
                <button onClick={() => {this.updateInvoice()}}>Update Invoice</button><br></br><br></br>
                <button onClick={() => {this.props.delete(this.props.invoice.id)}}>Delete</button>
                <hr></hr>
                <h3>Items</h3> <button  onClick={() => {this.addInvoiceItem()}}>Add New Items</button>
                {this.state.popUp ? popUpItem :<List data={this.state.update.invoice_items} header={this.columns} page={false} popUp={this.popUp} />}
            
            <button onClick={() => {this.stateman()}}>State</button>
            </div>

        )
    }
}
export default PopUpEdit
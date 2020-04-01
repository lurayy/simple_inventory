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

class PopUpEdit extends Component {

    constructor(props){
        super(props)
        this.state = {
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
    }


    async componentDidMount(){
        var request_json = {
            'action':'get',
        }
        await getInvoiceStatus(JSON.stringify(request_json)).then(data => {
            console.log(data)
            if (data['status']){
                this.setState({
                    ...this.state,
                    'status':data.data
                })
            }  
        })
        console.log("State",this.state)
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
                return
            }
        }
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
            createInvoiceItem(JSON.stringify(request_json)).then(data => {
                if (data['status']){
                    alert("Invoice Item Has Been Added.")
                    this.refreshTable()
                }
                else{
                    alert(data['error'])
                }
            })
            return
        }
        request_json = {
            'action':'edit',
            ...this.state.update.invoice_items[this.state.current]
        }
        updateInvoiceItem(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                alert("Invoice Item Details Has Been Updated.")
                this.refreshTable()
            }
            else{
                alert(data['error'])
            }
        })
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


    render() {
        const item_selection = this.state.item_selection
        const itemPopUp = <Popup trigger={ <button>Select Item</button>} closeOnDocumentClick>
        <div>
            <input placeholder="Item Name" id='item_search_box' name='item_serach_box' onChange={this.searchItem}></input>
            <div className={style.dropdown_content} id='item_dropdown'>
                    {item_selection.map(
                        item => (
                            // use css to get rid of <a>
                            <a key={item.id} onClick={() => {this.selectItem(item.id, item.name)}} >{item.name}</a>
                        )
                    )}
            </div>
        </div>
        </Popup>
        const popUpItem = <div>
                <button onClick={() => {this.refreshTable()}} >Back</button><br></br><br></br>
                Item : {this.state.update.invoice_items[this.state.current].item_name}  {this.state.new ? itemPopUp: <span></span>}<br></br>
                Quantity : <input name="quantity" placeholder={this.state.update.invoice_items[this.state.current].quantity} type="number" onChange={this.onChangePI} required></input><br></br>
                Defective : <input name="defective" placeholder={this.state.update.invoice_items[this.state.current].defective} type="number"  onChange={this.onChangePI} required></input><br></br>
                
                Discount Type :<select name='discount_type' id="discount_type" defaultValue={this.state.update.invoice_items[this.state.current].discount_type}  onChange={this.onChangePI}>
                                    <option value="percent">Percentage</option>
                                    <option value="fixed">Fixed</option>
                                </select> <br></br>
                Discount : <input placeholder={this.state.update.invoice_items[this.state.current].discount} name="discount" onChange={this.onChangePI} ></input><br></br>
                Invoice Price : <input placeholder={this.state.update.invoice_items[this.state.current].purchase_price} name="purchase_price" onChange={this.onChangePI} required></input> <br></br>
                Status : <select defaultValue= {this.state.update.invoice_items[this.state.current].status} name="status" onChange={this.onChangePI}>
                    <option value="delivered">Delivered</option>
                    <option value="incomplete">Incomplete</option>
                    <option value="addedtocirculation">Added To Circulation</option>
                </select><br></br>
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
                            // use css to get rid of <a>
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
            </div>
        )
    }
}
export default PopUpEdit
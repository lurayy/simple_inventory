import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from '../purchaseOrder/css/popUp.module.css';
import {getCustomers} from '../../api/sales/customer';
import {createInvoice,  getInvoice, getInvoiceStatus} from '../../api/sales/invoice';
import {updateInvoiceItem, deleteInvoiceItems, createInvoiceItem} from '../../api/sales/invoiceItem'
import {getItems} from '../../api/inventory/itemApi';
import {getPlaces} from '../../api/inventory/placeApi';
import { getDiscounts, getTaxes } from '../../api/misc'
import { Grid, Button } from '@material-ui/core';
import Swal from 'sweetalert2';


class InvoiceCreation extends Component {

    constructor(props){
        super(props)
        this.state = {
            'tax_start':0,
            'tax_end':5,
            'discount_start':0,
            'discount_end':5,
            'tax_loaded':false,
            'discount_loaded':false,
            'discount_page':[],
            'tax_page':[],
            'discount_selection':[],
            'tax_selection':[],
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
                    'invoiced_on': new Date(),
                    'due_on': new Date()
                },
                'invoice_items':[[{
                    'id':'Fake Key',
                    'discount':[],
                    'applied_discount':[],
                    'tax':[],
                    'applied_tax':[]
                }]]
            }
        }
        this.update_table = this.update_table.bind(this)
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
        this.removeEntry = this.removeEntry.bind(this)
        this.addEntryDiscount = this.addEntryDiscount.bind(this)
        this.addEntryTax = this.addEntryTax.bind(this)
    }

    removeEntry(id, dis){
        var temp,temp2
        if (dis){
             temp = this.state.update.invoice_items[this.state.current].applied_discount
            temp.pop(dis)
             temp2 = this.state.update.invoice_items[this.state.current].discount
            temp2.pop(temp.id)
            this.setState({
                ...this.state,
                'update':{
                    ...this.state.update,
                    invoice_items:{
                        ...this.state.update.invoice_items,
                        [dis]:{
                            'applied_discount':temp,
                            'discount':temp2
                        }
                    }
                }
            })
        }
        else {
            
                 temp = this.state.update.invoice_items[this.state.current].applied_tax
                temp.pop(dis)
                 temp2 = this.state.update.invoice_items[this.state.current].taxes
                temp2.pop(temp.id)
                this.setState({
                    ...this.state,
                    'update':{
                        ...this.state.update,
                        invoice_items:{
                            ...this.state.update.invoice_items,
                            [dis]:{
                                'applied_tax':temp,
                                'taxes':temp2
                            }
                        }
                    }
                })
            
        }
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
            else{
                Swal.fire(data['error'])
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
            
            else{
                Swal.fire(data['error'])
            } 
        })
    }

    selectCustomer(id,name){
        console.log(id,name)
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
            'item_id':this.state.update.invoice_items[key].item  
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
                this.update_stock(data)
            }
        })

    }

    // data = sold_From_selection
    update_stock(data){
        console.log('data',data)
        var sold_from
        if (this.state.update.invoice_items[this.state.current]['sold_from']){
            sold_from = this.state.update.invoice_items[this.state.current]['sold_from']
        }else {
            sold_from = data['placements'][0]['placed_on']
            console.log('default',sold_from)
        }
        var temp=[];
        var p ;
        for (p in data['placements']){
            console.log(sold_from, "  ", data['placements'][p]['placed_on'])
            if (parseInt(sold_from) === parseInt(data['placements'][p]['placed_on'])){
                var string  = data['placements'][p]['purchase_item_details']['purchase_price'] + "/-  " + data['placements'][p]['purchase_item_details']['quantity'] + " " + data['placements'][p]['purchase_item_details']['vendor'] 
                temp.push({
                    'id': data['placements'][p]['purchase_item'],
                    'str':string
                })
                console.log(temp)
            }
            
        }
        this.setState({
            ...this.state,
            'stock_selection': temp
        })
    }  
    

    async onChangePlace(e){
        await this.setState({
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
        var temp=[],p,sold_from;
        if (this.state.update.invoice_items[this.state.current]['sold_from']){
            sold_from = this.state.update.invoice_items[this.state.current]['sold_from']
        }else {
            sold_from = this.state.sold_from[0]['placed_on']
            console.log('default',sold_from)
        }
        for (p in this.state.sold_from_selection){
            if ( parseInt(sold_from) === parseInt(this.state.sold_from_selection[p]['placed_on'])){
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
            'action':'add',
            'invoice_id':this.state.update.invoice.id,
            'status':'',
        }
        console.log(this.state)
        createInvoice(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Invoice Details Has Been Updated.")
                window.location.pathname = '/invoices'
            }
            else{
                Swal.fire(data['error'])
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
                ...this.state.update.invoice_items[this.state.current],
            }
            request_json['applied_tax'] = []
            request_json['applied_discount'] = []
            createInvoiceItem(JSON.stringify(request_json)).then(data => {
                if (data['status']){
                    Swal.fire("Invoice Item Has Been Added.")
                    this.refreshTable()
                }
                else{
                    Swal.fire(data['error'])
                }
            })
            return
        }
        request_json = {
            'action':'edit',
            'invoice':this.state.update.invoice.id,
            'invoice_item_id':this.state.update.invoice_items[this.state.current].id,
            ...this.state.update.invoice_items[this.state.current]
        }
        request_json['applied_tax'] = []
        request_json['applied_discount'] = []
        updateInvoiceItem(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Invoice Item Details Has Been Updated.")
                this.refreshTable()
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    deleteInvoiceItem(){
        var request_json = {
            invoice_items_id : [this.state.update.invoice_items[this.state.current].id]
        }
        deleteInvoiceItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Invoice Item Has Beed Deleted.")
                this.refreshTable()
            }
            else{
                Swal.fire(data['error'])
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
                        'status':'incomplete',
                        'applied_tax':[],
                        'applied_discount':[],
                        'purchase_item':'',
                        'discount':[],
                        'taxes':[]
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
            
            else{
                Swal.fire(data['error'])
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
            
            else{
                Swal.fire(data['error'])
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


    discount_columns =[
        {
            'id':1,
            'name':'Name',
            'prop':'name'
        },{
            'id':2,
            'name':'Rate',
            'prop':'rate'
        },{
            'id':3,
            'name':'Code',
            'prop':'code'
        },{
            'id':4,
            'name':'Type',
            'prop':'discount_type'
        },{
            'id':5,
            'name':'Remove',
            'prop':'removeButton'
        },
    ]

    tax_columns =[
        {
            'id':1,
            'name':'Name',
            'prop':'name'
        },{
            'id':2,
            'name':'Rate',
            'prop':'rate'
        },{
            'id':3,
            'name':'Code',
            'prop':'code'
        },{
            'id':4,
            'name':'Type',
            'prop':'tax_type'
        },{
            'id':5,
            'name':'Remove',
            'prop':'removeButton'
        },
    ]

    
    add_discount_columns =[
        {
            'id':1,
            'name':'Name',
            'prop':'name'
        },{
            'id':2,
            'name':'Rate',
            'prop':'rate'
        },{
            'id':3,
            'name':'Code',
            'prop':'code'
        },{
            'id':4,
            'name':'Type',
            'prop':'discount_type'
        }
    ]

    add_tax_columns =[
        {
            'id':1,
            'name':'Name',
            'prop':'name'
        },{
            'id':2,
            'name':'Rate',
            'prop':'rate'
        },{
            'id':3,
            'name':'Code',
            'prop':'code'
        },{
            'id':4,
            'name':'Type',
            'prop':'tax_type'
        }
    ]

    async update_table (by,dis) {
        var x = by<0?-1:1
        var request_json
        if (dis){
            if (by===0){
                await this.setState({
                    'discoount_loaded':false,
                    discount_start: 0,
                    discount_end: 10,
                    discount_page:1
                })
            }
            else{
                if (this.state.discount_start+by>-1){
                    await this.setState({
                        'discount_loaded':false,
                        discount_start: this.state.discount_start+by,
                        discount_end: this.state.discount_end+by,
                        discount_page:this.state.discount_page+x
                    })
                }
                else{
                    Swal.fire("Cannot move futher from here.")
                    return
                }
            }
            request_json = {
                'action':'get',
                'filter':'none',
                'start':this.state.discount_start,
                'end':this.state.discount_end
            }
            this.getDiscountsData(request_json)
        }
    else { 
        if (by===0){
            await this.setState({
                'tax_loaded':false,
                tax_start: 0,
                tax_end: 10,
                tax_page:1
            })
        }
        else{
            if (this.state.tax_start+by>-1){
                await this.setState({
                    'tax_loaded':false,
                    tax_start: this.state.tax_start+by,
                    tax_end: this.state.tax_end+by,
                    tax_page:this.state.tax_page+x
                })
            }
            else{
                Swal.fire("Cannot move futher from here.")
                return
            }
        }
        request_json = {
            'action':'get',
            'filter':'none',
            'start':this.state.tax_start,
            'end':this.state.tax_end
        }
        this.getTaxesData(request_json)

    }
    }
    
    async getDiscountsData (request_json) {
        await getDiscounts(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'discount_selection':data['discounts'],
                    'discount_loaded':true
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }
    async getTaxesData (request_json) {
        await getTaxes(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'tax_selection':data['taxes'],
                    'tax_loaded':true
                })
            }  
        })
    }
 
    addEntryDiscount(id){
        var dis;
        for (dis in this.state.discount_selection){
            if (this.state.discount_selection[dis].id === id){
                var temp = this.state.update.invoice_items[this.state.current]['applied_discount']
                var x = this.state.discount_selection[dis]
                temp.push(x)
                var temp2 = this.state.update.invoice_items[this.state.current]['discount']
                temp2.push(id)
                this.setState({
                    ...this.state,
                    update:{
                        ...this.state.update,
                        'invoice_items':{
                            ...this.state.update.invoice_items,
                            [this.state.current] : {
                                ...this.state.update.invoice_items[this.state.current],
                                'discount':temp2,
                                'applied_discount': temp
                            }
                        }
                    }
                })
            }
        }
    }

    addEntryTax(id){
        var dis;
        for (dis in this.state.tax_selection){
            if (this.state.tax_selection[dis].id === id){
                var temp = this.state.update.invoice_items[this.state.current]['applied_tax']
                var x = this.state.tax_selection[dis]
                temp.push(x)
                var temp2 = this.state.update.invoice_items[this.state.current]['taxes']
                temp2.push(id)
                this.setState({
                    ...this.state,
                    update:{
                        ...this.state.update,
                        'invoice_items':{
                            ...this.state.update.invoice_items,
                            [this.state.current] : {
                                ...this.state.update.invoice_items[this.state.current],
                                'tax':temp2,
                                'applied_tax': temp
                            }
                        }
                    }
                })
            }
        }
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
            <option key="Fake Key" value='Fake Value'>Select Place</option>
                {places.map(
                    x => (
                    <option key={x.id} value={x.id}>{x.str_placed_on}</option>
                    )
                )}
            </select>

            
        var stocks  = this.state.stock_selection
        var stockValue = this.state.update.invoice_items[this.state.current].purchase_item ? this.state.update.invoice_items[this.state.current].purchase_item : ''
        const selectStock = <select name='purchase_item' id="purchase_item" onChange={this.onChangePI} value={stockValue} >
                <option key='Fake Key' value="Fake Value">Select Stock</option>
                {stocks.map(
                    x => (
                    <option key={x.id} value={parseInt(x.id)}>{x.str}</option>
                    )
                )}
            </select>
        const addPopupDiscount = <div>
            <h3> Click To Apply New Discount</h3>
                            <List data={this.state.discount_selection} header={this.add_discount_columns} page={false} popUp={this.addEntryDiscount} />
                            <button onClick={()=> {this.update_table(-5,true)}}>Previous</button><span>      {this.state.discount_page}       </span><button  onClick={()=> {this.update_table(5,true)}} >Next</button>
                        </div>
        
        const addPopupTax = <div>
            <h3>Click To Apply New Tax </h3>
                            <List data={this.state.tax_selection} header={this.add_tax_columns} page={false} popUp={this.addEntryTax} />
                            <button onClick={()=> {this.update_table(-5,false)}}>Previous</button><span>      {this.state.tax_page}       </span><button  onClick={()=> {this.update_table(5,false)}} >Next</button>
                        </div>
        const discounts =this.state.update.invoice_items[this.state.current].applied_discount
        for (var dis in discounts){
            discounts[dis] = {
                ...discounts[dis],
                'removeButton':<button onClick={() => {this.removeEntry(dis,true)}}> Remove </button>
            }
        }
        
        const taxes = this.state.update.invoice_items[this.state.current].applied_tax
        for (var dis in taxes){
            taxes[dis] = {
                ...taxes[dis],
                'removeButton':<button onClick={()=>{this.removeEntry(dis,false)}}> Remove </button>
            }
        }
        const popUpItem = <div>
                <button onClick={() => {this.refreshTable()}} >Back</button><br></br><br></br>
                Item : {this.state.update.invoice_items[this.state.current].item_name}  {itemPopUp}<br></br>
                Sold From: 
                Place : {this.state.update.invoice_items[this.state.current].item ? selectPlace : "Select An Item First" } <br></br>
                Stock :   {this.state.update.invoice_items[this.state.current].item ? selectStock : "Select An Item First" } <br></br>
                <br></br>

                Quantity : <input name="quantity" placeholder={this.state.update.invoice_items[this.state.current].quantity} type="number" onChange={this.onChangePI} required min='1' ></input><br></br>
                Price : <input name="price" placeholder={this.state.update.invoice_items[this.state.current].price} type="number" onChange={this.onChangePI} required></input><br></br>
                Tax Total : {this.state.update.invoice_items[this.state.current].tax_total} <br></br>
                Sub Total : {this.state.update.invoice_items[this.state.current].sub_total} <br></br>
                Discount Amount : {this.state.update.invoice_items[this.state.current].discount_amount}<br></br>
                Total without discount : {this.state.update.invoice_items[this.state.current].total_without_discount}<br></br>
                Total : {this.state.update.invoice_items[this.state.current].total}<br></br>
                <br></br>
                Applied Discounts : :<List data={discounts} header={this.discount_columns} page={false} popUp={this.popUp} removeEntry={this.removeEntry} /><button onClick={() =>{this.update_table(0, true)}} >Apply New Discount</button> <br></br><br></br>
                {this.state.discount_loaded ? addPopupDiscount : <span></span>}<br></br>
                Applied Taxes : :<List data={taxes} header={this.tax_columns} page={false} popUp={this.popUp} removeEntry={this.removeEntry} /><br></br><button onClick={() => {this.update_table(0, false)}}>Apply New Tax</button><br></br><br></br>
                {this.state.tax_loaded ? addPopupTax : <span></span>}<br></br>
                {this.state.new ? <button onClick={() => {this.postInvoiceItem(true)}} >Add</button> : <button onClick={() => {this.postInvoiceItem()}} >Update</button>}<br></br><br></br>
                <button onClick={() => {this.deleteInvoiceItem()}} >Delete</button>
            </div>
        const customer_selection = this.state.customer_selection
        const customerPopup = <Popup trigger={<button>Select Customer</button>} closeOnDocumentClick>
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
            <Grid container justify='center' >
                
                <Grid item xm={8}>
                    <table  cellPadding='10' cellSpacing='10' >
                        <tbody>
                            <tr>
                                <th colSpan={3}>
                                    <h1>New Invoice Order</h1>
                                    <h4>Select customer and Date only</h4>
                                </th>
                            </tr>
                        <tr>
                        <td><b>Customer :</b> <input
                                defaultValue={this.state.update.invoice.customer_name}
                                label='Customer'
                                variant="outlined"
                                />
                         </td>
                        
                        <td>{customerPopup}</td>
                        </tr>
                        
                        <tr>
                            <td>
                            <b>Invoiced On : </b><br></br>
                                <DatePicker
                                name='invoiced_on'
                                selected={this.state.update.invoice.invoiced_on}
                                onChange={this.invoiceHandler}
                                />
                            </td>
                            <td>
                            <b>Due On : </b> <br></br>
                            <DatePicker
                            name='completed_on'
                            selected={this.state.update.invoice.due_on}
                            onChange={this.dueOnHandler}
                            />
                            </td>
                        </tr>
                            <tr>
                                <td>
                                <Button variant="contained" color="primary" onClick={() => {this.updateInvoice()}}>Update Invoice</Button>
                                </td>
                                <td>
                                <Button variant="contained" color="secondary"  onClick={() => {this.props.delete(this.props.invoice.id)}}>Delete</Button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </Grid>
                </Grid>
                </div>
        //     <div>
        //         <h1>Invoice</h1>
        // <h3>{this.state.update.invoice.customer_name} </h3>
        //         Added By : {this.state.update.invoice.added_by_name}<br></br>
        //         Customer : {this.state.update.invoice.customer_name} {customerPopup}<br></br>
        //         Order Number : {this.state.update.invoice.order_number}<br></br>
        //         <br></br><br></br>
        //         Invoiced On : 
        //         <DatePicker
        //         name='invoiced_on'
        //         selected={this.state.update.invoice.invoiced_on}
        //         onChange={this.invoiceHandler}
        //         />
        //         Due On : 
        //         <DatePicker
        //         name='completed_on'
        //         selected={this.state.update.invoice.due_on}
        //         onChange={this.dueOnHandler}
        //         /><br></br><br></br>
                
        //         Total Amount : {this.state.update.invoice.total_amount}<br></br>
        //         Total Tax : {this.state.update.invoice.tax_total}<br></br>
        //         Total Discount: {this.state.update.invoice.discount_total}<br></br>
        //         Paid Amount : {this.state.update.invoice.paid_amount}<br></br>

        //         <br></br>
        //         Additional Discount : <input placeholder={this.state.update.invoice.additional_discount} name='additional_discount' onChange={this.onChange} ></input>
        //         <br></br><br></br>

                
        //         Status : <select name='status' id="status" onChange={this.onChange} value={this.state.update.invoice.status}  >
        //                         {status.map(
        //                             x => (
        //                             <option key={x.id} value={parseInt(x.id)}>{x.name}</option>
        //                             )
        //                         )}
        //                     </select> <br></br><br></br>
        //         <button onClick={() => {this.updateInvoice()}}>Add Invoice</button><br></br><br></br>
        //         <hr></hr>
        //     <button onClick={() => {this.stateman()}}>State</button>
        //     </div>

        )
    }
}
export default InvoiceCreation
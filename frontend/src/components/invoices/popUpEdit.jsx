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
import { getDiscounts, getTaxes } from '../../api/misc'
import { Grid } from '@material-ui/core';
import "react-datepicker/dist/react-datepicker.css";
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';


import IconButton from '@material-ui/core/IconButton';

import {Button, TextField } from '@material-ui/core';

import Swal from 'sweetalert2'


import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';



class PopUpEdit extends Component {

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
                    ...this.props.invoice,
                    'invoiced_on': this.converter(this.props.invoice.invoiced_on),
                    'due_on': this.converter(this.props.invoice.due_on)
                },
                'invoice_items':this.props.invoice_items
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
        if (dis){
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!'
              }).then((result) => {
                if (result.value) {

            var temp = this.state.update.invoice_items[this.state.current].applied_discount
            temp.pop(dis)
            var temp2 = this.state.update.invoice_items[this.state.current].discount
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
        })
    }
        else {
            
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
                var temp = this.state.update.invoice_items[this.state.current].applied_tax
                temp.pop(dis)
                var temp2 = this.state.update.invoice_items[this.state.current].taxes
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
                Swal.fire({
                    icon:'error',
                    title:data['error']
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
            
            else{
                Swal.fire({
                    icon:'error',
                    title:data['error']
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
            else{
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })
            }
        })

    }

    // data = sold_From_selection
    update_stock(data){
        console.log("data",data)
        var sold_from;
        if (this.state.update.invoice_items[this.state.current]['sold_from']){
            sold_from = this.state.update.invoice_items[this.state.current]['sold_from']
        }else {
            sold_from = data['placements'][0]['placed_on']
        }
        var temp=[];
        var p ;
        for (p in data['placements']){
            if (sold_from === data['placements'][p]['placed_on']){
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
        var temp=[],p;
                for (p in this.state.sold_from_selection){
                    if ( parseInt( this.state.update.invoice_items[this.state.current]['sold_from']) ===parseInt( this.state.sold_from_selection[p]['placed_on'])){
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
                Swal.fire("Invoice Details Has Been Updated.")
                this.props.update(0)
            }
            else{
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })            }
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
                    Swal.fire({
                        icon:'error',
                        title:data['error']
                    })                   }
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
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })               }
        })
    }

    deleteInvoiceItem(){
        var request_json = {
            invoice_items_id : [this.state.update.invoice_items[this.state.current].id]
        }
        
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        deleteInvoiceItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Invoice Item Has Beed Deleted.")
                this.refreshTable()
            }
            else{
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })               }
        })
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
                        'discount':[],
                        'taxes':[],
                        'applied_tax':[],
                        'applied_discount':[],
                        'purchase_item':'',
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
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })            }
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
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })            }
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
                    alert("Cannot move futher from here.")
                    return
                }
            }
            var  request_json = {
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
                alert("Cannot move futher from here.")
                return
            }
        }
        var  request_json = {
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
                Swal.fire({
                    icon:'error',
                    title:data['error']
                })            }
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
        var temp,temp2;
        console.log("dis",this.state.update.invoice_items[this.state.current])
        for (dis in this.state.discount_selection){
            if (this.state.discount_selection[dis].id === id){
                temp = this.state.update.invoice_items[this.state.current]['applied_discount']
                var x = this.state.discount_selection[dis]
                temp.push(x)
                temp2 = this.state.update.invoice_items[this.state.current]['discount']
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
        const itemPopUp = <Popup trigger={ <Button variant="contained" color="primary" size='small'>Select Item</Button>} closeOnDocumentClick>
        <div>
            <input placeholder="Item Name" id='item_search_box' name='item_serach_box' onChange={this.searchItem}></input>
            <div className={style.dropdown_content} id='item_dropdown'>
                    {item_selection.map(
                        item => (
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
            <Grid container justify='center'>
                <Grid item xm={12} md={12}>
            <List data={this.state.discount_selection} header={this.add_discount_columns} page={false} popUp={this.addEntryDiscount} />
            </Grid>
            <Grid item xm={12} md={3}>
            <IconButton onClick={()=> {this.update_table(-5,true)}}><NavigateBeforeIcon /></IconButton><span>      {this.state.discount_page}       </span><IconButton  onClick={()=> {this.update_table(5,true)}} ><NavigateNextIcon /></IconButton>
            </Grid>
                            
            </Grid>
                            </div>
        
        const addPopupTax = <div>
            <h3>Click To Apply New Tax </h3>
            <Grid container justify='center'>
                <Grid item xm={12} md={12}>
            <List data={this.state.tax_selection} header={this.add_tax_columns} page={false} popUp={this.addEntryTax} />
            </Grid>
            <Grid item xm={12} md={3}>
            <IconButton onClick={()=> {this.update_table(-5,false)}}><NavigateBeforeIcon /></IconButton><span>      {this.state.discount_page}       </span><IconButton  onClick={()=> {this.update_table(5,false)}} ><NavigateNextIcon /></IconButton>
            </Grid>
                            
            </Grid>
            </div>
        

        var dis;
        const discounts =this.state.update.invoice_items[this.state.current].applied_discount
        for (dis in discounts){
            discounts[dis] = {
                ...discounts[dis],
                'removeButton':<button onClick={() => {this.removeEntry(dis,true)}}> Remove </button>
            }
        }
        
        const taxes = this.state.update.invoice_items[this.state.current].applied_tax
        for (dis in taxes){
            taxes[dis] = {
                ...taxes[dis],
                'removeButton':<button onClick={()=>{this.removeEntry(dis,false)}}> Remove </button>
            }
        }
        const popUpItem = <div>
            <table cellSpacing={10} cellPadding={10}>
                <tbody>

               
                <tr>
                    <td>
                    <Button  variant="contained" color="secondary" onClick={() => {this.refreshTable()}} >Back</Button>
                    </td>
                </tr>
                <tr>
                    <td>
                    <h3>Item :  {this.state.update.invoice_items[this.state.current].item_name}</h3>
                    </td>
                    <td>
                    {itemPopUp}
                    </td>
                </tr>
                <tr>
                    <th colSpan={2} >
                        <b>Sold From </b>
                    </th>
                </tr>

                <tr>
                    <td>
                        Place: 
                    </td>
                    <td>
                    {this.state.update.invoice_items[this.state.current].item ? selectPlace : "Select An Item First" }
                    </td>
                </tr>
                <tr>
                    <td>
                    Stock :
                    </td>
                    <td>
                    {this.state.update.invoice_items[this.state.current].item ? selectStock : "Select An Item First" }
                    </td>
                </tr>
                <tr>
                    <td>
                    Quantity : <input name="quantity" placeholder={this.state.update.invoice_items[this.state.current].quantity} type="number" onChange={this.onChangePI} required min='1' ></input><br></br>
                
                    </td>
                    <td>
                    Price : <input name="price" placeholder={this.state.update.invoice_items[this.state.current].price} type="number" onChange={this.onChangePI} required></input><br></br>
                
                    </td>
                    </tr>
                    <tr>
                    <td>
                    Tax Total : {this.state.update.invoice_items[this.state.current].tax_total} <br></br>
                    </td>
                    <td>
                    Sub Total : {this.state.update.invoice_items[this.state.current].sub_total} <br></br>
                    </td>
                </tr>
                <tr>
                    <td>
                    Discount Amount : {this.state.update.invoice_items[this.state.current].discount_amount}<br></br>
                    </td>
                    <td>
                    Total without discount : {this.state.update.invoice_items[this.state.current].total_without_discount}<br></br>
                    </td>
                </tr>
                <tr>
                    <td>
                    Total : {this.state.update.invoice_items[this.state.current].total}<br></br>
                    </td>
                </tr>
                <tr>
                    
                <td>
                    Applied Discounts 
                    </td>
                    <th>
                    <Button onClick={() =>{this.update_table(0, true)}}  variant="contained" color="secondary" size='small'>Apply New Discount</Button>
                    </th>
                </tr>
                <tr>
                    <td colSpan={3} >
                    <List data={discounts} header={this.discount_columns} page={false} popUp={this.popUp} removeEntry={this.removeEntry} />
                    </td>
                </tr>
                <tr>
                    <td colSpan={3}>
                {this.state.discount_loaded ? addPopupDiscount : <span></span>}
                </td>
                </tr>
            <tr>
                <td>
                    Applied Taxes 
                </td>
                <td>
                <Button variant="contained" color="secondary" size='small' onClick={() => {this.update_table(0, false)}}>Apply New Tax</Button>
                </td>
            </tr>
                <tr>
                    <td colSpan={3}>
                    <List data={taxes} header={this.tax_columns} page={false} popUp={this.popUp} removeEntry={this.removeEntry} />
                    </td>
                </tr>
                <tr>
                    <td colSpan={3}>
                    {this.state.tax_loaded ? addPopupTax : <span></span>}<br></br>
                    </td>
                </tr>
                <tr>
                    <td>
                    {this.state.new ? <Button variant="contained" color="primary" size='small' onClick={() => {this.postInvoiceItem(true)}} >Add</Button> : <Button  variant="contained" color="primary" size='small' onClick={() => {this.postInvoiceItem()}} >Update</Button>}
                    </td>
                    <td>
                    <Button  variant="contained" color="secondary" size='small' onClick={() => {this.deleteInvoiceItem()}} >Delete</Button>
                    </td>
                </tr>
                </tbody>
            </table>
            </div>

        const customer_selection = this.state.customer_selection
        const customerPopup = <Popup trigger={<Button variant="contained" color="primary">Change Customer</Button>} closeOnDocumentClick>
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
                
            <Grid container justify='center' alignContent='center' alignItems='center' spaceing={6}>
                <Grid item xm={12} >
                    <h2>{this.state.update.invoice.customer_name}</h2>
                </Grid>
            </Grid>

            <Grid container justify='center' >
                <Grid item xm={8}>
                    <table  cellPadding='10' cellSpacing='10' >
                        <tbody>
                        <tr>
                        <td>
                                <TextField
                                defaultValue={this.state.update.invoice.added_by_name}
                                InputProps={{
                                    readOnly: true,
                                }}
                                label='Added By'
                                variant="outlined"
                                />
                                </td>
                        <td> <TextField
                                defaultValue={this.state.update.invoice.customer_name}
                                InputProps={{
                                    readOnly: true,
                                }}
                                label='Customer'
                                variant="outlined"
                                
                                />
                         </td>
                        </tr>
                        <tr>
                            <td></td><td>{customerPopup}</td>
                        </tr>
                        <tr>
                            <td colSpan="2">
                            <TextField
                                defaultValue= {this.state.update.invoice.order_number}
                                InputProps={{
                                    readOnly: true,
                                }}
                                fullWidth
                                label='Order Number'
                                variant="outlined"
                                />
                        </td>
                        </tr>

                        <tr>
                            <td>
                            <TextField
                                defaultValue= {this.state.update.invoice.total_amount}
                                InputProps={{
                                    readOnly: true,
                                }}
                                
                                label='Total Amount'
                                variant="outlined"
                                />
                            </td>
                            <td>
                            <TextField
                                defaultValue= {this.state.update.invoice.tax_total}
                                InputProps={{
                                    readOnly: true,
                                }}
                                
                                label='Tax Total'
                                variant="outlined"
                                />
                            </td>
                        </tr>
                        <tr>
                            <td>
                            <TextField
                                defaultValue={this.state.update.invoice.discount_total}
                                InputProps={{
                                    readOnly: true,
                                }}
                                
                                label='Discount Total'
                                variant="outlined"
                                />
                            </td>
                            <td>
                            <TextField
                                defaultValue= {this.state.update.invoice.paid_amount}
                                InputProps={{
                                    readOnly: true,
                                }}
                                
                                label='Paid Amount'
                                variant="outlined"
                                />
                            </td>
                        </tr>

                        <tr>
                            <td>
                            <TextField variant="outlined" value={this.state.update.invoice.additional_discount} name='additional_discount' onChange={this.onChange} type='float' label='Additional Discount'></TextField>
                            </td>
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
                    
                            <td >
                            <b>Status : </b> 
                                    <Select label='Status' fullWidth name='status' id="status" onChange={this.onChange} value={this.state.update.invoice.status}>
                                        {status.map(
                                            x=>(
                                            <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                                            )
                                        )}
                                    </Select>
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
                <Grid container justify='center'>
                    <Grid item xs={8} >
                    <h3>Items</h3> <Button variant="contained" color="secondary"  onClick={() => {this.addInvoiceItem()}}>Add New Items</Button>
                    {this.state.popUp ? popUpItem :<List data={this.state.update.invoice_items} header={this.columns} page={false} popUp={this.popUp} />}
                
                    </Grid>
                </Grid>
            </div>
        )
    }
}
export default PopUpEdit
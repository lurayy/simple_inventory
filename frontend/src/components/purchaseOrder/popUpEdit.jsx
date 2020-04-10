import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from './css/popUp.module.css';
import {getVendors} from '../../api/inventory/vendorApi';
import {updatePurchaseOrder, getPurchaseOrder} from '../../api/inventory/purchaseOrder';
import {updatePurchaseItem, deletePurchaseItems, createPurchaseItem} from '../../api/inventory/purchaseItem'
import {getPurchaseOrderStatus} from '../../api/misc';
import {getItems} from '../../api/inventory/itemApi';
import { Grid, TextField, Button } from '@material-ui/core';

import Swal from 'sweetalert2'

import IconButton from '@material-ui/core/IconButton';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';



import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';



class PopUpEdit extends Component {

    constructor(props){
        super(props)
        this.state = {
            'popUp':false,
            'new':false,
            'current':0,
            'status':[],
            'vendor_selection':[
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
                'purchase_order':{
                    ...this.props.purchase_order,
                    'invoiced_on': this.converter(this.props.purchase_order.invoiced_on),
                    'completed_on': this.converter(this.props.purchase_order.completed_on)
                },
                'purchase_items':this.props.purchase_items
            }
        }
        this.refreshTable = this.refreshTable.bind(this)
        this.getItemData = this.getItemData.bind(this)
        this.selectItem = this.selectItem.bind(this)
        this.searchItem = this.searchItem.bind(this)
        this.addPurchaseItem = this.addPurchaseItem.bind(this)
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
                Swal.fire("Purchase Order Details Has Been Updated.")
                this.props.update(0)
            }
            else{
                Swal.fire("Error : ",data.error)
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

    postPurchaseItem(is_new=false){
        var request_json
        if (is_new){
            request_json = {
                'action':'add',
                'purchase_order':this.state.update.purchase_order.id,
                ...this.state.update.purchase_items[this.state.current]
            }
            createPurchaseItem(JSON.stringify(request_json)).then(data => {
                if (data['status']){
                    Swal.fire("Purchase Item Has Been Added.")
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
            ...this.state.update.purchase_items[this.state.current]
        }
        updatePurchaseItem(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Purchase Item Details Has Been Updated.")
                this.refreshTable()
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    deletePurchaseItem(){
        var request_json = {
            purchase_items_id : [this.state.update.purchase_items[this.state.current].id]
        }
        deletePurchaseItems(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                Swal.fire("Purchase Item Has Beed Deleted.")
                this.refreshTable()
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }


    addPurchaseItem(){
        var current =0;
        var item,p_list=[];
        for (item in this.state.update.purchase_items){
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
                'purchase_items':[
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
                'purchase_items':{
                    ...this.state.update.purchase_items,
                    [this.state.current] : {
                        ...this.state.update.purchase_items[this.state.current],
                        'item_name' : name,
                        'item':id
                    },
                }
            }
        })

    }

    async refreshTable(){
        var id = this.state.update.purchase_order.id;
        var items= [];
        const request_json = {
            'action':'get',
            'purchase_order_id':id
        }
        await getPurchaseOrder(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                items = data['p_items']
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
                'purchase_items':items
            }
        })
    }


    render() {
        const item_selection = this.state.item_selection
        const itemPopUp = <Popup trigger={ <Button variant="contained" color="secondary" >Select Item</Button>} closeOnDocumentClick>
        <div>
            <input placeholder="Item Name" id='item_search_box' name='item_serach_box' onChange={this.searchItem}></input>
            <div className={style.dropdown_content} id='vendor_dropdown'>
                    {item_selection.map(
                        item => (
                            // use css to get rid of <a>
                            <a href="#" key={item.id} onClick={() => {this.selectItem(item.id, item.name)}} >{item.name}</a>
                        )
                    )}
            </div>
        </div>
        </Popup>
        const popUpItem = <table cellPadding={10} cellSpacing={10}>
            <tbody><tr>
                    <td colSpan={2}>
                    <IconButton color='secondary' onClick={()=> {this.refreshTable()}}><NavigateBeforeIcon /></IconButton>
                    </td>
                </tr>
            <tr>
                <td>
                <TextField
                    value= {this.state.update.purchase_items[this.state.current].item_name}
                    InputProps={{
                        readOnly: true,
                    }}
                    
                    label='Item'
                    variant="outlined"
                    />
                </td>
                <td>
                {this.state.new ? itemPopUp: <span></span>}
                </td>
            </tr>
            <tr>
                <td>
                <TextField
                    value={this.state.update.purchase_items[this.state.current].quantity} 
                    type="number" 
                    required 
                    name="quantity" 
                    onChange={this.onChangePI}
                    label='Quantity'
                    variant="outlined"
                    />
                </td>
                <td>
                <TextField
                    name="defective" 
                    value={this.state.update.purchase_items[this.state.current].defective} 
                    type="number"  
                    onChange={this.onChangePI}
                    required
                    label='Defective'
                    variant="outlined"
                    />
                </td>
            </tr>
            <tr>
                    <td colSpan={2}>
                        Discount Type  :  <Select lable='Discount Type' fullWidth name='discount_type' id="discount_type"value={this.state.update.purchase_items[this.state.current].discount_type}  onChange={this.onChangePI}>
                            <MenuItem value="percent">Percentage</MenuItem>
                            <MenuItem value="fixed">Fixed</MenuItem>
                        </Select>
                    </td>
            </tr>
            <tr>
                <td>
                <TextField
                    name="discount" 
                    value={this.state.update.purchase_items[this.state.current].discount} 
                    type="number"  
                    onChange={this.onChangePI}
                    required
                    label='Discount'
                    variant="outlined"
                    />
                </td>
                <td>
                <TextField
                    name="purchase_price" 
                    value={this.state.update.purchase_items[this.state.current].purchase_price} 
                    type="number"  
                    onChange={this.onChangePI}
                    required
                    label='Purchase Price'
                    variant="outlined"
                    />
                </td>
            </tr>
            <tr>
                <td colSpan={2}>
                <Select value= {this.state.update.purchase_items[this.state.current].status} name="status" onChange={this.onChangePI}>
                    <MenuItem value="delivered">Delivered</MenuItem>
                    <MenuItem value="incomplete">Incomplete</MenuItem>
                    <MenuItem value="addedtocirculation">Added To Circulation</MenuItem>
                </Select>
                </td>
            </tr>
                <tr>
                    <td>
                    {this.state.new ? <Button variant="contained" color="primary" onClick={() => {this.postPurchaseItem(true)}} >Add</Button> : <Button variant="contained" color="primary" onClick={() => {this.postPurchaseItem()}} >Update</Button>}
                    </td>
                    <td>
                    {this.state.new ? <span></span>:<Button variant="contained" color="secondary" onClick={() => {this.deletePurchaseItem()}} >Delete</Button>}
            
                    </td>
                </tr>
                
                </tbody>
            </table>
        const vendor_selection = this.state.vendor_selection
        const vendorPopup = <Popup trigger={<Button variant="contained" color="secondary">Change Vendor</Button>} closeOnDocumentClick>
        <div>
            <input placeholder="Vendor's first name" id='vendor_serach_box' name='vendor_serach_box' onChange={this.searchVendor}></input>
            <div className={style.dropdown_content} id='vendor_dropdown'>
                    {vendor_selection.map(
                        vendor => (
                            // use css to get rid of <a>
                            <a href="#" key={vendor.id} onClick={() => {this.selectVendor(vendor.id, vendor.name)}} >{vendor.name}</a>
                        )
                    )}
            </div>
        </div>
        </Popup>
        const status = this.state.status
                
        return (
            <div>
                <Grid container justify='center'>
                    <Grid  item xm={6}>
                    <h1>{this.props.purchase_order.vendor_name}</h1>
                    </Grid>
                </Grid>
                <Grid container justify='center'>
                    <Grid item xm={6}>
                        <table cellPadding='10' cellSpacing='10'>
                            <tbody>
                                <tr>
                                    <td>
                                        <TextField
                                        value={this.state.update.purchase_order.vendor_name}
                                        InputProps={{
                                            readOnly: true,
                                        }}
                                        label='Vendor'
                                        variant="outlined"
                                        />
                                    </td>
                                    <td>
                                    {vendorPopup}
                                    </td>
                                </tr>
                                <tr>
                                    <td colSpan={2}>
                                    <TextField
                                        value={this.state.update.purchase_order.added_by_name}
                                        InputProps={{
                                            readOnly: true,
                                        }}
                                        label='Added By'
                                        variant="outlined"
                                        fullWidth
                                        />
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td>
                                    Invoiced On:<br></br>
                                    <DatePicker
                                    name='invoiced_on'
                                    selected={this.state.update.purchase_order.invoiced_on}
                                    onChange={this.invoiceHandler}
                                    />
                                    </td>
                                    <td>
                                    Completed On : <br></br>
                                    <DatePicker
                                    name='completed_on'
                                    selected={this.state.update.purchase_order.completed_on}
                                    onChange={this.completeHandler}
                                    />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <TextField
                                        value={this.state.update.purchase_order.total_cost} 
                                        name="total_cost" 
                                        onChange={this.onChange}
                                        label='Total Cost'
                                        variant="outlined"
                                        fullWidth
                                        />
                                    </td>
                                    <td>
                                    <TextField
                                        value= {this.state.update.purchase_order.discount} 
                                        name="discount"
                                        onChange={this.onChange}
                                        label='Discount'
                                        variant="outlined"
                                        fullWidth
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td colSpan={2}>
                                        Discount Type  :  <Select lable='Discount Type' fullWidth name='discount_type' id="discount_type" onChange={this.onChange} value={this.state.update.purchase_order.discount_type}>
                                            <MenuItem value="percent">Percentage</MenuItem>
                                            <MenuItem value="fixed">Fixed</MenuItem>
                                        </Select>
                                    </td>
                                </tr>
                                <tr >
                                    <td colSpan={2}>
                                    Status : <Select name='status' id="status" fullWidth onChange={this.onChange} value={this.state.update.purchase_order.status} required >
                                    {status.map(
                                        x => (
                                        <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                                        )
                                    )}
                                    </Select> 
                            </td>
                                </tr>
                                <tr>
                                    <td>
                                        <Button  variant="contained" color="primary"  onClick={() => {this.updatePurchaseOrder()}}>
                                        Update
                                        </Button>
                                       
                                    </td>
                                    <td>
                                    <Button  variant="contained" color="secondary"  onClick={() => {this.props.delete(this.props.purchase_order.id)}}>
                                        Delete
                                        </Button>
                                    </td>
                                </tr>

                            </tbody>
                        </table><br></br>
                       </Grid>
                </Grid>
                <hr></hr>
                <Grid container>
                    <Grid item md={1}>

                    </Grid>
                    <Grid item md={3}>             
                        <h1>Items</h1>   
                    </Grid>

                </Grid>
                <Grid container justify='center'>
                    <Grid item xm={8}>
                    <table cellSpacing={10} cellPadding={10}>
                    <tbody>
                        <tr>
                            <td>
                            </td>
                            <td>
                            </td>
                        </tr>
                        <tr>
                            <td colSpan={3}>
                            {this.state.popUp ? popUpItem :<div> <Button  variant="contained" color="primary" onClick={() => {this.addPurchaseItem()}}>Add New Items</Button><br></br>
                            <List data={this.state.update.purchase_items} header={this.columns} page={false} popUp={this.popUp} /></div>}
                            </td>
                        </tr>
                    </tbody>
                    </table>
                 
                
                </Grid>

                </Grid>
                </div>
        )
    }
}
export default PopUpEdit
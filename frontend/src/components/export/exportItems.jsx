import React, { Component } from 'react'
import { Grid, Button, Select} from '@material-ui/core'
import RefreshIcon from '@material-ui/icons/Refresh';
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import {getExportFields} from '../../api/misc';
import Loading from '../loading';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import {TextField} from '@material-ui/core'
import {getItemCatagories} from '../../api/inventory/itemCatagory'
import LoadingIcon from '../loading';
import List from '../list';


import MenuItem from '@material-ui/core/MenuItem';

import Swal from 'sweetalert2'

class ExportItems extends Component {

    constructor(props){
        super(props)
        this.state={
            'fields':[],
            'loading':true,
            'update':[],
            'filters':{
                exact_name:true,
                is_applied_name:false,
                is_applied_weight_from: false,
                is_applied_weight_upto: false,
                is_applied_average_cost_price_from:false,
                is_applied_average_cost_price_upto:false,
                is_applied_catagory:false,
                is_applied_stock_from:false,
                is_applied_stock_upto:false,
                is_applied_sales_price_from:false,
                is_applied_sales_price_upto:false,
                is_applied_sold_from:false,
                is_applied_sold_upto:false
            },
            'item_catagories':[],
            'items':[],
            'loadingTable':true,
            "showItems":false,
            "page":0,
            "start":0,
            "end":10
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleFilterChange = this.handleFilterChange.bind(this)
        this.update_table = this.update_table.bind(this)
        this.handlePopUp = this.handlePopUp.bind(this)
    }



    async componentDidMount(){
        var data = {
            'action':"get",
            'model':'item'
        }
        await getExportFields(JSON.stringify(data)).then(data =>  {
            if (data['status']){
                var temp = {}
                var x;
                var show_fields = [];
                var old;
                var filters = {};
                data['fields'].map(field => {
                    old=field
                    temp[field]=false
                    x = field.split('_')
                    field = ''
                    x.map(
                        y => {
                            field = field + y.charAt(0).toUpperCase() + y.slice(1)+ ' '
                        }
                    )
                    show_fields.push({'key':old, "str":field})
                    
                })
                filters['exact_name'] = false
                temp['name'] = true
                this.setState({
                    ...this.state,
                    'fields':show_fields,
                    'update':temp,
                    'loading':false
                })
            }  
        })
        data = {
            'action':'get',
            'start':0,
            'end':50
        }
        await getItemCatagories(JSON.stringify(data)).then(data=> {
            try { 
                if (data['status']){
                    this.setState({
                        ...this.state,
                        'item_catagories':data['item_catagories']
                    })
                }
                else{
                    Swal.fire({
                        icon:'error',
                        title:data['error']
                    })                   
                }
            }catch(e){
                console.log(e)
            }
        })
    }

    handleChange(e){
        if (e.target.name === 'name'){

        }
        else{
            this.setState({
                ...this.state,
                update : {
                    ...this.state.update,
                    [e.target.name]: !(this.state.update[e.target.name])
                }
            })
        }
    }
    
    handleFilterChange(e){
        var temp = "is_applied_"+e.target.name
        if (e.target.name === "exact_name"){
            this.setState({
                ...this.state,
                filters : {
                    ...this.state.filters,
                    exact_name: !(this.state.filters.exact_name)
                }
            })
        }else{
            this.setState({
                ...this.state,
                filters : {
                    ...this.state.filters,
                    [temp]:true,
                    [e.target.name]: e.target.value 
                }
            })
        }

    }

    exportData(){
        var request_json = {
            'model':'item',
            'action':'export',
            'showItems':false,
            'filter':{'fields':this.state.update, ...this.state.filters}
        }
        getExportFields(JSON.stringify(request_json)).then(data=>{
            if(data['status']){
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    back(){
        this.props.history.push('/export')
    }

      
    async update_table(by){
        await this.setState({
            ...this.state,
            loadingTable:true
        })        
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                ...this.state,
                start: 0,
                end: 10,
                page:1
            })
        }
        else{
            if (this.state.start+by>-1){
                await this.setState({
                    ...this.state,
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
        var request_json = {
            'model':'item',
            'action':'export',
            'start':this.state.start,
            'end':this.state.end,
            'showItems':true,
            'filter':{'fields':this.state.update, ...this.state.filters}
        }
        getExportFields(JSON.stringify(request_json)).then(data=>{
            if(data['status']){
                this.setState({
                    ...this.state,
                    items:data['items'],
                    showItems:true
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
        await this.setState({
            ...this.state,
            loadingTable:false
        })
    }

    handlePopUp(id){
        this.props.history.push('/items/'+this.state.items[id]['id'])
    }

    columns = [
        {
            id:1,
            name:"Name",
            prop: 'name'
        },
        {
            id:2,
            name:"Catagory",
            prop: 'catagory_str'
        },
        {
            id:3,
            name:"Price",
            prop: 'sales_price'
        },
        ,
        {
            id:4,
            name:"Stock",
            prop: 'stock'
        },
        {
            id:5,
            name:"Sold",
            prop: 'sold'
        }      
    ]

    render() {
        const list =<div><h1>Item List</h1> <List data={this.state.items} header={this.columns} update={this.update_table} popUp={this.handlePopUp} page={this.state.page} ></List></div>
        const catagories = this.state.item_catagories
        const main_render = 
        <div>
        <Grid container spacing={3} justify="center" alignItems="center">
                            <Grid item xs={3} >
                            <Button  variant="contained" size='small' color="primary" onClick={()=> {this.back()}}>
                                <ArrowLeftIcon></ArrowLeftIcon>
                                Back
                            </Button>
                            </Grid>
                            <Grid item xs={5}>

                            </Grid>
                            <Grid item xs={3}>
                            <Button variant="contained" color="secondary">
                            <RefreshIcon/>&nbsp;&nbsp;&nbsp;Refresh Filters
                            </Button>
                            </Grid>
                        </Grid>
                        <Grid container justify='center'>
                            <Grid item md={4}>
                                <table cellSpacing={5} cellPadding={5} >
                                    <tbody>
                                        <tr>
                                            <td>
                                            <h3><b>Select Data To Include On Export</b></h3>
                                            </td>
                                        </tr>
                                            {this.state.fields.map(
                                                field =>(
                                                    <tr key={field['key']}>
                                                    <td key={field['key']}> 
                                                    <FormControlLabel
                                                      control={<Switch checked={this.state.update[field['key']]} onChange={this.handleChange} name={field['key']} />}
                                                      label={field['str']}
                                                    />
                                                    </td>
                                                    </tr>
                                                )
                                            )}
                                        <tr>
                                            <td>
                                            <Button variant="contained" color="secondary" onClick={()=> {this.exportData()}}>Export Data</Button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </Grid>
                            <Grid item md={4}>
                                <table cellSpacing={5} cellPadding={5}>
                                    <tbody>
                                    <tr>
                                        <td>
                                        <h3><b>Additional Filters</b></h3>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                        <TextField id="name"  size='small' variant="outlined"name="name" defaultValue={this.state.filters.name} onChange={this.handleFilterChange} label="Name" />
                                        </td>
                                        <td>
                                        <FormControlLabel
                                                      control={<Switch checked={this.state.filters.exact_name} onChange={this.handleFilterChange} name='exact_name' />}
                                                      label={this.state.filters.exact_name ? "Match Exactly":"Partial Match"}
                                                    />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                            Weight Filter
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                        <TextField id="weight_from" size='small'  variant="outlined"  defaultValue={this.state.filters.weight_from} name="weight_from" type='number' onChange={this.handleFilterChange} label="Start Weight" />
                                        </td>
                                        <td>
                                        <TextField id="weight_upto"  size='small' variant="outlined" name="weight_upto" type='number'  defaultValue={this.state.filters.weight_upto} onChange={this.handleFilterChange} label="Start Upto" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                            Average Cost Price Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="average_cost_price_from" size='small' variant="outlined" name="average_cost_price_from"  defaultValue={this.state.filters.average_cost_price_from} type='number' onChange={this.handleFilterChange} label="ACP From" />
                                        </td>
                                        <td>
                                        <TextField id="average_cost_price_upto"size='small'  variant="outlined" name="average_cost_price_upto" type='number'   defaultValue={this.state.filters.average_cost_price_upto} onChange={this.handleFilterChange} label="ACP Upto" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            Catagory
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                        <Select fullWidth name='catagory' id="catagory" defaultValue={this.state.filters.catagory} onChange={this.handleFilterChange} required >
                                        {catagories.map(
                                            x => (
                                            <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                                            )
                                        )}
                                    </Select>
                                        </td>
                                    </tr>

                                    
                                    <tr>
                                        <td colSpan={2}>
                                            Stock
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="stock_from" variant="outlined" size='small'  name="stock_from" type='number' defaultValue={this.state.filters.stock_from} onChange={this.handleFilterChange} label="Stock From" />
                                        </td>
                                        <td>
                                        <TextField id="stock_upto" variant="outlined" size='small'  name="stock_upto" type='number' defaultValue={this.state.filters.stock_upto} onChange={this.handleFilterChange} label="Stock Upto" />
                                        </td>
                                    </tr>

                                    <tr>
                                        <td colSpan={2}>
                                            Sales Price Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="sales_price_from" variant="outlined" size='small'  name="sales_price_from" type='number' defaultValue={this.state.filters.sales_price_from} onChange={this.handleFilterChange} label="Sales Price From" />
                                        </td>
                                        <td>
                                        <TextField id="sales_price_upto" variant="outlined" size='small'  name="sales_price_upto" type='number' onChange={this.handleFilterChange}  defaultValue={this.state.filters.sales_price_upto} label="Sales Price Upto" />
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colSpan={2}>
                                            Sold Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="sold_from" size='small' variant="outlined"  size='small'  name="sold_from" type='number' defaultValue={this.state.filters.sold_from} onChange={this.handleFilterChange} label="Sold From" />
                                        </td>
                                        <td>
                                        <TextField id="sold_upto" variant="outlined" name="sold_upto" size='small'  type='number' onChange={this.handleFilterChange} defaultValue={this.state.filters.sold_upto} label="Sold Upto" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                                <Button  variant="contained" color="primary" onClick={() =>this.update_table(0)} >
                                                    Show Filtered Data
                                                </Button>
                                        </td>
                                    </tr>
                                    
                                    </tbody>
                                </table>
                            </Grid>
                        </Grid>
                        <Grid container justify='center'>
                            <Grid item md={8}>
                            {this.state.showItems ? this.state.loadingTable ? <LoadingIcon></LoadingIcon> : list :<span></span> }

                            </Grid>
                        </Grid>

                        </div>
        return (
            <div>
            {this.state.loading? <Loading></Loading> : main_render}
        </div>
        )
    }
}

export default ExportItems
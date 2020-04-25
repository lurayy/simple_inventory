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
            },
            'item_catagories':[]
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleFilterChange = this.handleFilterChange.bind(this)
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
                temp['name'] = true
                console.log(show_fields)
                this.setState({
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
                console.log(data)
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
                    })                   }
            }catch(e){
                console.log(e)
            }
        })
        console.log(this.state)
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
        console.log(temp, e.target.name)
        if (e.target.name === "exact_name"){
            console.log("here")
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
        console.log(this.state)
        var request_json = {
            'model':'item',
            'action':'export',
            'filter':{'fields':this.state.update}
        }
        getExportFields(JSON.stringify(request_json)).then(data=>{
           console.log(data)
            if(data['status']){
                console.log('Headers')
            }
        })
    }

    back(){
        this.props.history.push('/export')
    }

      

    render() {
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
                                        <TextField id="name"  size='small' variant="outlined"name="name" onChange={this.handleFilterChange} label="Name" />
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
                                        <TextField id="weight_from" size='small'  variant="outlined" name="weight_from" type='number' onChange={this.handleFilterChange} label="Start Weight" />
                                        </td>
                                        <td>
                                        <TextField id="weight_upto"  size='small' variant="outlined" name="weight_upto" type='number' onChange={this.handleFilterChange} label="Start Upto" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                            Average Cost Price Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="average_cost_price_from" size='small' variant="outlined" name="average_cost_price_from" type='number' onChange={this.handleFilterChange} label="ACP From" />
                                        </td>
                                        <td>
                                        <TextField id="average_cost_price_upto"size='small'  variant="outlined" name="average_cost_price_upto" type='number' onChange={this.handleFilterChange} label="ACP Upto" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            Catagory
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                        <Select fullWidth name='catagory' id="catagory" onChange={this.handleFilterChange} required >
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
                                        <TextField id="stock_from" variant="outlined" size='small'  name="stock_from" type='number' onChange={this.handleFilterChange} label="Stock From" />
                                        </td>
                                        <td>
                                        <TextField id="stock_upto" variant="outlined" size='small'  name="stock_upto" type='number' onChange={this.handleFilterChange} label="Stock Upto" />
                                        </td>
                                    </tr>

                                    <tr>
                                        <td colSpan={2}>
                                            Sales Price Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="sales_price_from" variant="outlined" size='small'  name="sales_price_from" type='number' onChange={this.handleFilterChange} label="Sales Price From" />
                                        </td>
                                        <td>
                                        <TextField id="sales_price_upto" variant="outlined" size='small'  name="sales_price_upto" type='number' onChange={this.handleFilterChange} label="Sales Price Upto" />
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colSpan={2}>
                                            Sold Filter
                                        </td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <TextField id="sold_from" size='small' variant="outlined"  size='small'  name="sold_from" type='number' onChange={this.handleFilterChange} label="Sold From" />
                                        </td>
                                        <td>
                                        <TextField id="sold_upto" variant="outlined" name="sold_upto" size='small'  type='number' onChange={this.handleFilterChange} label="Sold Upto" />
                                        </td>
                                    </tr>
                                    
                                    </tbody>
                                </table>
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
import React, { Component } from 'react'
import List from '../list';
import { getItemCatagory, updateItemCatagory,  deleteItemCatagory } from '../../api/inventory/itemCatagory';
import {Button, TextField, Grid } from '@material-ui/core';


import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'


class ItemCatagoryList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'itemCatagory':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.itemCatDelete = this.itemCatDelete.bind(this)
        this.popUptemp = this.popUptemp.bind(this)
        this.updatetemp = this.updatetemp.bind(this)
    }
    popUptemp(id,uuid){

    }
    updatetemp(){

    }
    onChange(e)
    {
        this.setState({
            'itemCatagory': {
                ...this.state.itemCatagory,
                [e.target.name] : [e.target.value][0]
            }
        })
    }

    
    async onSubmit(e){
        e.preventDefault();
            var data = this.state.itemCatagory
            data = {...data, 'action':'edit','item_catagory_id':data.id}
            console.log(data)
            updateItemCatagory(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'ItemCatagory Data updated.',
                            'success'
                          )
                        this.props.update(0)
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

    itemCatDelete(id){
        var data = {
            'item_catagories_id':[
                id
            ]
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
            if (result.value) {
                
        deleteItemCatagory(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    Swal.fire({
                        icon:'success',
                        title:'Item Catagory entry has been deleted.',
                        showConfirmButton: false,
                        timer:1000
                    })
                    this.props.update(0)
                }   else{
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
})
    }
    
    async popUp(id, uuid=0){
        const data = {
            'action':'get',
            'item_catagory_id':id,
        }
        var data_main;
        await getItemCatagory(JSON.stringify(data)).then(data => {
            console.log(data)
            if (data['status']){
                data_main=data
            }
        })

        await this.setState({
            'popUp':true,
            'itemCatagory':data_main['item_catagories'][0]
        })
    }


    columns = [
        {
            id:1,
            name:"Name",
            prop: 'name'
        },
        {
            id:2,
            name:'Items Under This Catagory',
            prop:'count'
        }
    ]

    items_c = [
        {
            id:1,
            name:"Item's Name",
            prop:'name'
        },{
            id:2,
            name: 'Price',
            prop: 'sales_price',
        },
        {
            id:3,
            name:'Sales Price',
            prop:'sales_price'
        },
        {
            id:4,
            name: 'Stock',
            prop:'stock',
        },
        {
            id:5,
            name:'Sold',
            prop:'sold'
        }


    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
            <Grid container justify='center'>
<Grid item xm={6}>
<Button  variant="contained" size='small' color="primary" onClick={()=> {this.setState({...this.state, popUp:false})}}>
                <ArrowLeftIcon></ArrowLeftIcon>
         Back
     </Button>
     <h1>{this.state.update.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            <table cellSpacing={10} cellPadding={10}>
                                <tbody>
                                <tr>
                                    <td>
                                    Name: 
                                    </td>
                                    <td>
                                    <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                defaultValue={this.state.itemCatagory.name}          
                            />
                                    </td>
                                </tr>
                                <tr>
<td>
<Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button>
</td>
<td>
<Button variant="contained" color="secondary" onClick={() => {this.itemCatDelete(this.state.itemCatagory.id)}}>
                            Delete Discount
                        </Button> 
</td>
                                </tr>
                                <tr>
                                   <td colSpan={3}>
                                       <h1> Related Items</h1>
                                   <List data={this.state.itemCatagory.items} header={this.items_c} popUp={this.popUptemp} update={this.updatetemp} page={false} />
                                   </td> 
                                </tr>
                                </tbody>
                            </table>
                           
                           
                        
                </form>
            
</Grid>
            </Grid>
                        
                        
                    </div>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default ItemCatagoryList

import React, { Component } from 'react'
import List from '../list';
import { getItemCatagory, updateItemCatagory,  deleteItemCatagory } from '../../api/inventory/itemCatagory';
import {Button, TextField } from '@material-ui/core';

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
                        alert("ItemCatagory Data updated.")
                        this.props.update(0)
                    }
                    else{
                        alert(data['error'])
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
        deleteItemCatagory(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('itemCatagory data deleted.')
                    this.props.update(0)
                }   else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
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
        }  
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.update.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.itemCatagory.name}          
                            />
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.itemCatDelete(this.state.itemCatagory.id)}}>
                            Delete Discount
                        </Button> 
                        
                </form>
            
                        <br>
                        </br>
                    </div>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default ItemCatagoryList

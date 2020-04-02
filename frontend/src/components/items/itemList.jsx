import React, { Component } from 'react'
import List from '../list';
import { getItem, updateItem,  deleteItems } from '../../api/inventory/itemApi';
import {Button, TextField } from '@material-ui/core';

class ItemList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'item':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.itemDelete = this.itemDelete.bind(this)
    }
    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value]
            }
        })
    }

    
    async onSubmit(e){
        e.preventDefault();
            var data = this.state.item
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit','item_id':data.id}
            console.log(data)
            updateItem(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Item Data updated.")
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

    itemDelete(id){
        var data = {
            'items_id':[
                id
            ]
        }
        deleteItems(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Item data deleted.')
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
            'item_id':id,
        }
        var data_main;
        await getItem(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'item':data_main['items'][0]
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
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.item.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.item.name}          
                            />
                            Code : <TextField
                                id ='code'
                                name="code"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.item.code} 
                            />
                             Item Type :<select name='item_type' id="item_type" defaultValue={this.state.item.item_type}  onChange={this.onChange}>
                                    <option value="percent">Percentage</option>
                                    <option value="fixed">Fixed</option>
                                </select> <br></br>
                            Rate : <input placeholder={this.state.item.rate} name="rate" onChange={this.onChange} ></input><br></br>
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.itemDelete(this.state.item.id)}}>
                            Delete Item
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

export default ItemList

import React, { Component } from 'react'
import List from '../list';
import { getPlace, updatePlace,  deletePlaces } from '../../api/inventory/placeApi';
import {Button, TextField } from '@material-ui/core';

class PlaceList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'place':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.placeDelete = this.placeDelete.bind(this)
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
            var data = this.state.place
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit','place_id':data.id}
            console.log(data)
            updatePlace(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Place Data updated.")
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

    placeDelete(id){
        var data = {
            'places_id':[
                id
            ]
        }
        deletePlaces(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Place data deleted.')
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
            'place_id':id,
        }
        var data_main;
        await getPlace(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'place':data_main['places'][0]
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
            name:"Number of Items Assigned To The Place (different Purchase orders)",
            prop: 'count_assignment'
        }     
    ]

    second_columns =[
        {
            id:1,
            name:"Item Name",
            prop:'item_name'
        },
        {
            id:2,
            name:"Stock",
            prop:'stock'
        },
        {
            id:3,
            name:'Purchase Order',
            prop:'purchase_order_uuid'
        }
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.place.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.place.name}          
                            />
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.placeDelete(this.state.place.id)}}>
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

export default PlaceList

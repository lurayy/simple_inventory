import React, { Component } from 'react'
import List from '../list';
import { getPlace, updatePlace,  deletePlaces } from '../../api/inventory/placeApi';
import {Button, TextField, Grid } from '@material-ui/core';
import {getPlacements, deletePlacement } from '../../api/misc'

import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'

import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


class PlaceList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'page':1,
            'start':0,
            'end':10,
            'popUpPlacement':false,
            'popUp':false,
            'place':{},
            'update':{
                'name':''
            },
            'placements':[]
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.placeDelete = this.placeDelete.bind(this)
        this.update = this.update.bind(this)
        this.popUpPlacement = this.popUpPlacement.bind(this)
        this.deletePlacement = this.deletePlacement.bind(this)
    }
    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value][0]
            }
        })
    }

    
    async update (by) {
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                start: 0,
                end: 10,
                page:1
            })
        }
        else{
            if (this.state.start+by>-1){
                await this.setState({
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
        var  request_json = {
            'action':'get',
            'place':this.state.update.id,
            'filter':'place',
            'start':this.state.start,
            'end':this.state.end
        }
        console.log(request_json)
        this.getPlacementsData(request_json)
    }

    async getPlacementsData(request_json){
        var data_main;
        await getPlacements(JSON.stringify(request_json)).then(data => {
            console.log(data)
            if (data['status']){
                data_main=data['placements']
            }
        })
        console.log(data_main)
        await this.setState({
            ...this.state,
            'popUpPlacement':true,
            'placements':data_main
        })
    }

    async deletePlacement(id){
        const request = {
            'action':'delete',
            'id':id
        }
        Swal.fire({
            title: 'Are you sure?',
            text: "The remaining stock will be added to the default storage place.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) =>  {
            if (result.value) {
        deletePlacement(JSON.stringify(request)).then(data=>{
            if(data['status']){
                Swal.fire('Placement is deleted and the remaining stock is added to the default storing place.')
                this.popUp(this.state.place.id)
            }
            else {
                Swal.fire(data['error'])
            }
        })
    }
})
}
    

    popUpPlacement(){

    }
    
    async onSubmit(){
            var data = this.state.update
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
        var data_main, data_main2;
        await getPlace(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'place':data_main['places'][0],
            'update':data_main['places'][0],
        })
        const req = {
            'action':'get',
            'place':id,
            'filter':'place',
            'start':0,
            'end':10
        }
        this.getPlacementsData(req)
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

    placementColumn = [
        {
            id:1,
            name:"Item",
            prop:'item_name',
        },
        {
            id:2,
            name:'Purchase Order ID',
            prop:'purchase_order_uuid'
        },
        {
            id:3,
            name:'Stock',
            prop:'stock'
        }
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        
        const popUpRender = <div>
                         &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;<Button  variant="contained" size='small' color="primary" onClick={()=> {this.setState({...this.state, popUp:false})}}>
                            <ArrowLeftIcon></ArrowLeftIcon>
                            Back
                        </Button>
                        <Grid container>
                            <Grid item xs={3}>
                            <span> </span>
                            </Grid>
                            <Grid item xs={6}>
                                <table cellSpacing={10}>
                                    <tbody>
                                        <tr>
                                            <td colSpan={2}>
                                            <h1>{this.state.place.name}</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colSpan={2}>
                                            <TextField
                                            id ='name'
                                            name="name"
                                            label='Place Name'
                                            autoFocus
                                            fullWidth
                                            required
                                            type='text'
                                            onChange={this.onChange}  
                                            value={this.state.update.name}          
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
                                            <Button variant="contained" color="secondary" onClick={() => {this.placeDelete(this.state.place.id)}}>
                                                Delete Discount
                                            </Button> 
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </Grid>
                        </Grid>
                        <Grid container justify={'center'}>
                            <Grid item xm={8}>
                            <h1>Items Located On {this.state.update.name}</h1>
                            <List data={this.state.placements} header={this.placementColumn} delete={this.deletePlacement} popUp={this.popUpPlacement} update={this.update} page={this.state.page} />
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

export default PlaceList

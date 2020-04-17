import React, { Component } from 'react'
import List from '../list';
import { getPlace, updatePlace,  deletePlaces, assignPlace } from '../../api/inventory/placeApi';
import {Button, TextField, Grid, Input } from '@material-ui/core';
import {getPlacements, deletePlacement } from '../../api/misc'
import {getItems} from '../../api/inventory/itemApi'
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'
import AddCircleIcon from '@material-ui/icons/AddCircle';
import {getPurchaseItems}  from '../../api/inventory/purchaseItem'
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


class PlaceList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'itemsPage':1,
            'itemsStart':0,
            'itemsEnd':10,
            'newPlacementPopUpSelectItem': false,
            'purchaseItemSelectPopUp':false,
            'addPlacementFinal':false,
            'page':1,
            'start':0,
            'end':10,
            'popUpPlacement':false,
            'popUp':false,
            'place':{},
            'update':{
                'name':'',
                'stock':1,
            },
            'placementUpdate':{},
            'placements':[],
            'items':[],
            'purchaseItems':[],
            'selectedPurchaseItem':[]
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.placeDelete = this.placeDelete.bind(this)
        this.update = this.update.bind(this)
        this.popUpPlacement = this.popUpPlacement.bind(this)
        this.deletePlacement = this.deletePlacement.bind(this)
        this.addNewItem = this.addNewItem.bind(this)
        this.updateItemsTable = this.updateItemsTable.bind(this)
        this.selectItem = this.selectItem.bind(this)
        this.selectPurchaseItem = this.selectPurchaseItem.bind(this)
        this.assignPlacement = this.assignPlacement.bind(this)
        this.back = this.back.bind(this)
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
    
    back(){ 
        if (this.props.data){
            this.setState({...this.state, popUp:false});
        }else{
            this.props.history.push('/places')
        }
    }
    async componentDidMount(){
        try {
            const {id} = this.props.match.params
            if (id){
                await this.popUp(id,0,true)
            }
        }catch(e){
            console.log(e)
        }
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
        this.getPlacementsData(request_json)
    }

    async getPlacementsData(request_json){
        var data_main;
        await getPlacements(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                data_main=data['placements']
            }
        })
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
            updatePlace(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Place Data updated.")
                        this.back()
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
                    this.back()
                }   else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
            }
        })
    }
    
    async popUp(id, uuid=0, fromUrl){
        if(!fromUrl){
            this.props.pushNewId(id)
        }else{
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
}

    async addNewItem(id){
        var request = {
            action:'get',
            filter:'none',
            start:0,
            end:10          
        }    
        await getItems(JSON.stringify(request)).then(data => {
            if (data['status']){
                this.setState({
                    ...this.state,
                    newPlacementPopUpSelectItem: true,
                    items:data['items']                                        
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    async assignPlacement(){
        var request = {
            'action':"add",
            'place_id':this.state.place.id,
            'purchase_item':this.state.selectedPurchaseItem.id,
            'stock':this.state.update.stock
        }
        await assignPlace(JSON.stringify(request)).then(data => {
            if (data['status']){
                Swal.fire('Selected Items have been assigned to the place.')
                this.updateItemsTable(0)
            }else{
                Swal.fire(data['error'])
            }
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

    itemsColumn = [
        {
            id:1,
            name:'Item',
            prop:'name',
        },{
            id:2,
            name:'Defined Sales Price',
            prop:'sales_price',
        },{
            id:3,
            name:'Stock',
            prop:'stock'
        },{
            id:4,
            name:'catagory',
            prop:'catagory_str'
        }
    ]

    purchaseItemsColumn = [
        {
            id:1,
            name:'Vendor',
            prop:'vendor'
        },{
            id:2,
            name:'Purchase Order ID',
            prop:'purchase_order_id',
        },{
            id:3,
            name:'Purchase Price',
            prop:'price'
        },{
            id:4,
            name:'Total Stock',
            prop:'stock'
        },{
            id:5,
            name:'Unassigned Stock (On Default Place)',
            prop:'on_default'
        }
    ]

    async updateItemsTable (by) {
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                'itemsStart': 0,
                'itemsEnd': 10,
                'itemsPage':1
            })
        }
        else{
            await this.setState({
                'itemsStart': this.state.itemsStart+by,
                'itemsEnd': this.state.itemsEnd+by,
                'itemsPage':this.state.itemsPage+x
            })
        
        }
        var  request = {
            'action':'get',
            'filter':'none',
            'start':this.state.itemsStart,
            'end':this.state.itemsEnd
        }
        await getItems(JSON.stringify(request)).then(data => {
            if (data['status']){
                this.setState({
                    ...this.state,
                    items:data['items']                                        
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }
    
    async selectItem(id){
        var request = {
            'action':'get',
            'filter':'itemForPlace',
            'item_id':id,
        }
        var item;
        for (var x in this.state.items){
            if (this.state.items[x].id===id){
                item = this.state.items[x]
            } 
        }
        await getPurchaseItems(JSON.stringify(request)).then(data => {
            console.log(data)
            if (data['status']){
                this.setState({
                    ...this.state,
                    selectedItem:item,
                    purchaseItemSelectPopUp:true,
                    purchaseItems:data['purchase_items']                                
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    async selectPurchaseItem(id){
        var purchase_item;
        for (var x in this.state.purchaseItems){
            if (this.state.purchaseItems[x].id===id){
                purchase_item = this.state.purchaseItems[x]
            } 
        }
        await this.setState({
            ...this.state,
            addPlacementFinal: true,
            placementUpdate:{
                ...this.state.placementUpdate,
                placementUpdate:{
                    'purchase_item_id':id,
                    'placed_on':this.state.place.id
                },
            },
            'selectedPurchaseItem':purchase_item,
        })
        console.log(this.state)
    }
    render() {
        var listData
        if (!this.props.data){
            listData = []
        }else{
            listData=this.props.data
        }
        const list = <List data={listData} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const fianlForm = <div>
            <table cellSpacing={10}  cellPadding={10} >
                <tbody>
                    <tr>
                        <td colSpan={2}>
                            <h2><u>Selected Item</u></h2>
                            <List data={[this.state.selectedItem]} header={this.itemsColumn}/>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan={2}>
                            <h2><u>Selected Stock (Purchase Order)</u></h2>
                            <List data={[this.state.selectedPurchaseItem]} header={this.purchaseItemsColumn}/>
                        </td>
                    </tr>
                    <tr>
                        <td> 
                            <TextField required id="stock"  name="stock" onChange={this.onChange} label="Number of Items To Assign" fullWidth defaultValue={this.state.update.stock}  type='number' autoFocus min={1} max={this.state.selectedPurchaseItem.on_default} />
                        </td>
                        <td>
                            <Button  variant="contained" color="primary" onClick={()=> {this.assignPlacement()}}>Assign</Button>
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>
        const newPlacementForm = <div>
            <hr></hr>
            <table cellSpacing={10} cellPadding={10}>
                <tbody>
                    <tr>
                        <th colSpan={2}>
                            <h1>Place new item to {this.state.place.name}</h1>
                            {this.state.purchaseItemSelectPopUp ? <h4>Select a Purchase Order</h4> : <h4>Select an Item</h4>}
                        </th>
                    </tr>
                    <tr>
                        <td colSpan={2}>
                        {this.state.purchaseItemSelectPopUp ? this.state.addPlacementFinal ? fianlForm : <List data={this.state.purchaseItems} header={this.purchaseItemsColumn} popUp={this.selectPurchaseItem}></List> : <List data={this.state.items} header={this.itemsColumn}  popUp={this.selectItem} update={this.updateItemsTable} page={this.state.itemsPage}/> }   
                           </td>
                    </tr>
                </tbody>

            </table>
        </div>
        const popUpRender = <div>
                         &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;<Button  variant="contained" size='small' color="primary" onClick={()=> {this.back()}}>
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
                                                Delete Place
                                            </Button> 
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </Grid>
                        </Grid>
                        <Grid container justify={'center'}>
                            <Grid item xm={8}>
                                <table>
                                    <tbody>
                                    <tr>
                                        <td>
                                        <h1>Items Located On {this.state.update.name}</h1>
                                        </td>
                                        <td>
                                            <Button variant="contained" color="primary" onClick={() => {this.addNewItem(this.state.place.id)}}><AddCircleIcon></AddCircleIcon></Button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                            {this.state.newPlacementPopUpSelectItem  ? newPlacementForm : <List data={this.state.placements} header={this.placementColumn} delete={this.deletePlacement} popUp={this.popUpPlacement} update={this.update} page={this.state.page} />}
                                            
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            
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

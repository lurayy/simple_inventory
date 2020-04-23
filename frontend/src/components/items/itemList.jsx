import React, { Component } from 'react'
import List from '../list';
import { getItem, updateItem,  deleteItems } from '../../api/inventory/itemApi';
import {getItemCatagories} from '../../api/inventory/itemCatagory'
import {Button, TextField,Grid, Card, CardActionArea } from '@material-ui/core';
import {getPlacements} from '../../api/misc'

import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'
import url from '../../server';

import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import FileBase64 from 'react-filebase64';

import QrScanner from '../../qrScanner'


class ItemList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'catagories':[],
            'popUp':false,
            'item':{
                'catagory':''
            },
            'update':{},
            'placements':[],
            'thumbnail_image':false,
            'product_image':false
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.itemDelete = this.itemDelete.bind(this)
        this.getPlacementsData = this.getPlacementsData.bind(this);
        this.back = this.back.bind(this)
        this.dummy =this.dummy.bind(this)
        this.onFileChange = this.onFileChange.bind(this)
        this.handleQR = this.handleQR.bind(this)
        this.getDataFromQR = this.getDataFromQR.bind(this)
    }
    
    handleQR(value){
        this.getDataFromQR(value)
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
            this.props.history.push('/items')
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
    
    onFileChange(e){
        
    const toDataURL = url => fetch(url)
        .then(response => response.blob())
        .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
        }))
    
    
    toDataURL(e.target.files[0])
        .then(dataUrl => {
        console.log('RESULT:', dataUrl)
        this.setState({
            ...this.state,
            product_image: dataUrl
        })
        })   
    }

    getFiles(files){
        this.setState({ product_image: files })
      }
      
    getThumbnail(files){
        this.setState({ thumbnail_image: files })
      }

    async onSubmit(e){
        e.preventDefault();
        console.log(this.state)
            var data = this.state.update
            data = {...data, 'action':'edit','item_id':data.id}
            data['new_product_image'] = this.state.product_image
            data['new_thumbnail_image'] = this.state.thumbnail_image
            updateItem(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'ItemData updated.',
                            'success'
                          )
                        this.props.update(0)
                    }
                    else{
                        Swal.fire({
                            icon:'error',
                            title:data['error']
                        })                    }
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
        deleteItems(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    Swal.fire({
                        icon:'success',
                        title:'Item entry has been deleted.',
                        showConfirmButton: false,
                        timer:1000
                    })                    
                    this.props.update(0)
                }   else{
                    Swal.fire({
                        icon:'error',
                        title:data['error']
                    })                }
            }catch(e){
                console.log(e)
            }
        })
    }
})
    }

    async getDataFromQR(uuid){
        var data = {
            'action':'get',
            'filter':'purchase_item',
            'uuid':uuid
        }
        console.log("asdf", uuid)

        var data_main;
        await getItem(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'update':data_main['items'][0]
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
                        'catagories':data['item_catagories']
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
        data ={
            'action':'get',
            'start':0,
            'end':10,
            'filter':'item',
            'item':data_main['items'][0]['id']
        }
        this.getPlacementsData(data)
    }

    async popUp(id, uuid=0, fromUrl){
        if(!fromUrl){
            this.props.pushNewId(id)
            console.log("popup ",id)
        }else{
        var data = {
            'action':'get',
            'item_id':id,
        }
        var data_main;
        await getItem(JSON.stringify(data)).then(data => {
            console.log(data)
            if (data['status']){
                data_main=data
            }
            else{
                Swal.fire(data['error'])
                return
            }
        })
        await this.setState({
            'popUp':true,
            'update':data_main['items'][0]
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
                        'catagories':data['item_catagories']
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
        data ={
            'action':'get',
            'start':0,
            'end':10,
            'filter':'item',
            'item':id
        }
        this.getPlacementsData(data)
    }
}


    async getPlacementsData(request){
        await getPlacements(JSON.stringify(request)).then(data=> {
            try { 
                if (data['status']){
                    for(var i in data['placements']){
                        data['placements'][i]['qr_code_image'] =  url.slice(0,-1) +data['placements'][i]['qr_code_image'];
                    }
                    console.log(data)
                    this.setState({
                       ...this.state,
                       placements : data['placements']
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
    }

    async update_placement_table (by) {
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                'loaded':false,
                placementStart: 0,
                placementEnd: 10,
                placementPage:1
            })
        }
        else{
            if (this.state.placementStart+by>-1){
                await this.setState({
                    'loaded':false,
                    placementStart: this.state.placementStart+by,
                    placementEnd: this.state.placementEnd+by,
                    placementPage:this.state.placementPage+x
                })
            }
            else{
                alert("Cannot move futher from here.")
                return
            }
        }
        var  request_json = {
            'action':'get',
            'filter':'item',
            'item':this.state.update.id,
            'start':this.state.placementStart,
            'end':this.state.placementEnd
        }
        this.getPlacementsData(request_json)
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

    placementColumns = [
        {
            id:1,
            name:"Item",
            prop:'item_name',
        },
        {
            id:2,
            name:'Place On',
            prop:'placed_on_str'
        },
        {
            id:3,
            name:'Stock',
            prop:'stock'
        },
        {
            id:4,
            name:'Purchase Order ID',
            prop:'purchase_order_uuid'
        }
    ]
    dummy(id){
        for (var x in this.state.placements){
            if (parseInt(this.state.placements[x]['id']) === parseInt( id)){
                window.location.href= ("/purchaseorders/"+this.state.placements[x]['purchase_order_id'])
            }
        }
    }

    render() {
        var product_image=url.slice(0,-1) +this.state.update.product_image;
        var thumbnail_image=url.slice(0,-1) +this.state.update.thumbnail_image;

        var listData
        if (!this.props.data){
            listData = []
        }else{
            listData=this.props.data
        }
        const catagories = this.state.catagories
        const list = <div><QrScanner onFind={this.handleQR} ></QrScanner><br></br><List data={listData} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} /></div>
        const popUpRender = <div>
                    <Grid container>
                    <Grid item xm={3}>
                    <Button  variant="contained" size='small' color="primary" onClick={()=> {this.back()}}>
                                    <ArrowLeftIcon></ArrowLeftIcon>
                            Back
                     </Button>        
                     </Grid><Grid item xm={8}>  <h1>{this.state.update.name}</h1>
                     </Grid><Grid container justify='center'><Grid item md={6}>

                        <form onSubmit={this.onSubmit}>
                            <table cellSpacing={10} cellPadding={10} >
                                <tbody>
                                <tr>
                                    <td>
                                    <TextField
                                id ='name'
                                name="name"
                                type='text'
                                label="Item's Name"
                                onChange={this.onChange}  
                                defaultValue={this.state.update.name}          
                            />
                                    </td>
                                    <td>
                                    <TextField type='number' label='Sales Price' defaultValue={this.state.update.sales_price} onChange={this.onChange}></TextField><br></br>
                            
                                    </td>
                                </tr>
                                <tr>
                                <td colSpan={2}>
                                    Item Catagory : 
                                <Select fullWidth lable='Item Catagory' name='catagory' id="catagory" onChange={this.onChange} value={this.state.update.catagory} required >
                                {catagories.map(
                                    x => (
                                    <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                                    )
                                )}
                            </Select>
                            </td>
                                </tr>
                                <tr>
                                    <td>
                                    <TextField
          id="outlined-read-only-input"
          label="Current Stock"
          defaultValue={this.state.update.stock}
          InputProps={{
            readOnly: true,
          }}
          variant="outlined"
        />
                                    </td>
                                    <td>
                                    <TextField
          id="outlined-read-only-input"
          label="Number Of Sold Items"
          defaultValue={this.state.update.sold}
          InputProps={{
            readOnly: true,
          }}
          variant="outlined"
        />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <TextField
                                id ='weight'
                                name="weight"
                                type='number'
                                label="Item's Weight (in kg)"
                                onChange={this.onChange}  
                                defaultValue={this.state.update.weight}          
                            />
                                    </td>
                                    <td>
                                    <TextField
                                id ='average_cost_price'
                                name="average_cost_price"
                                type='number'
                                label="Item's Cost Price"
                                onChange={this.onChange}  
                                defaultValue={this.state.update.average_cost_price}          
                            />
                                    </td>
                                    </tr>
                                    <tr>
                                        <td colSpan={2}>
                                        <TextField
                                            fullWidth
                                            id ='description'
                                            name="description"
                                            type='text'
                                            label="Description"
                                            onChange={this.onChange}  
                                            defaultValue={this.state.update.description}          
                                        />
                                        </td>
                                    </tr>
                                <tr>
                                    <td colSpan={2}>
                                        <h3>Product Image</h3>
                                            <img width="100%" src={product_image} alt='Product Image' ></img>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    Upload Product Image : <FileBase64
                                    multiple={ true } 
                                    onDone={ this.getFiles.bind(this) } />
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td colSpan={2}>
                                        <h3>Thumbnail Image</h3>
                                            <img width="100%" src={thumbnail_image} alt='Thumbnail Image' ></img>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    Upload Thumbnail : <FileBase64
                                    multiple={ true } 
                                    onDone={ this.getThumbnail.bind(this) } />
                                    </td>
                                </tr>
                                <tr>
                                    <td>

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
                                    <Button variant="contained" color="secondary" onClick={() => {this.itemDelete(this.state.update.id)}}>
                            Delete Item
                        </Button> 
                                    </td>
                                </tr>
                                </tbody>
                            </table>                             
                </form>
            
                        <br>
                        </br>
                        </Grid>
                        </Grid>
                        </Grid>
                        <Grid container justify='center'>
                            <Grid item xm={6} >
                                <u><h3>Placement Of Current Item</h3></u>
                                <List data={this.state.placements} header={this.placementColumns}  popUp={this.dummy} update={this.update_placement_table} page={this.state.placementPage}>
                                </List>
                                <hr></hr>
                                <Grid item xm={4}>
                                {this.state.placements.map(
                                                header => (
                                                    <div key={header.id} >
                                                    <h4> {header['uuid']} </h4>
                                                    <img src={header['qr_code_image']} ></img></div>
                                                )
                                            )}
                                            </Grid>
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

export default ItemList

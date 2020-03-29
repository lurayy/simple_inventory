import React, { Component } from 'react'
import List from '../list';
import { getVendor, updateVendor,  deleteVendors } from '../../api/inventory/vendorApi';
import {Button, TextField } from '@material-ui/core';

class VendorList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'vendor':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.vendorDelete = this.vendorDelete.bind(this)
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
            var data = this.state.vendor
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit'}
            updateVendor(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Vendor Data updated.")
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

    vendorDelete(id){
        var data = {
            'vendors_id':[
                id
            ]
        }
        deleteVendors(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Vendor data deleted.')
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
            'vendor_id':id,
        }
        var data_main;
        await getVendor(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'vendor':data_main['vendors'][0]
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
            name:"Phone Number",
            prop: 'phone1'
        },
        {
            id:3,
            name:"Email",
            prop: 'email'
        },
        {
            id:4,
            name:"Address",
            prop: 'address'
        }      
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.vendor.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            First Name: <TextField
                                id ='first_name'
                                name="first_name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.vendor.first_name}          
                            />
                            Middle Name : <TextField
                                id ='middle_name'
                                name="middle_name"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.vendor.middle_name} 
                            />
                            Last Name  : <TextField
                                id ='last_name'
                                name="last_name"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.vendor.last_name}
                                  
                            />
                            <br></br>
                            Email : <TextField
                                id ='email'
                                name="email"
                                type='email'
                                onChange={this.onChange}                                
                                placeholder={this.state.vendor.email}
                                  
                            />
                            <br></br>
                            Website : <TextField
                                id ='website'
                                name="website"
                                type='text'
                                onChange={this.onChange}                                
                                placeholder={this.state.vendor.website}
                            />
                            <br></br>
                            Tax Number : <TextField
                                id ='tax_number'
                                name="tax_number"
                                type='number'
                                onChange={this.onChange}                                
                                placeholder={this.state.vendor.tax_number}
                                  
                            />
                            <br></br>
                            Contact Number: <TextField
                                id ='phone1'
                                name="phone1"
                                type='number'
                                onChange={this.onChange}                                  
                                placeholder={this.state.vendor.phone1}
                            />
                            <br></br>
                            Contact Number 2 : <TextField
                                id ='phone2'
                                name="phone2"
                                type='number'
                                onChange={this.onChange}                                
                                placeholder={this.state.vendor.phone2}
                            />
                            <br></br>
                            
                            Addresss : <TextField
                                id ='address'
                                name="address"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.vendor.address}
                            />
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.vendorDelete(this.state.vendor.id)}}>
                            Delete Vendor
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

export default VendorList

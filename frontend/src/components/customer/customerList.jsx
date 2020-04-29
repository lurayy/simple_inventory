import React, { Component } from 'react'
import List from '../list';
import { getCustomer, updateCustomer,  deleteCustomers, getCustomerCategory } from '../../api/sales/customer';
import {Button, TextField, Grid, withStyles } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

import {FormControl, InputLabel, Input} from '@material-ui/core'
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'
import LoadingIcon from '../loading';

import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';


const styles = makeStyles((theme) => ({
    root: {
    flexGrow: 12,
    },
    paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    },
}));


class CustomerList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'loading':false,
            'popUp':false,
            'customer':{},
            'update':{},
            'customerCategories':[]
        }
        this.getCustomerCategories = this.getCustomerCategories.bind(this)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.customerDelete = this.customerDelete.bind(this)
        this.back = this.back.bind(this)
        this.popUp= this.popUp.bind(this)
    }
    
    back(){ 
        if (this.props.data){
            this.setState({...this.state, popUp:false});
        }else{
            this.props.history.push('/customers')
        }
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

    async componentDidMount(){
        await this.getCustomerCategories()
        try {
            const {id} = this.props.match.params
            if (id){
                await this.popUp(id,0,true)
            }
            else{
            }
        }catch(e){
            console.log(e)
        }

    }

    async getCustomerCategories() {
        var requestJson = {
            'action':'get',
        }
        await getCustomerCategory(JSON.stringify(requestJson)).then((data) => {
            if(data['status']){
                this.setState({
                    ...this.state,
                    customerCategories:data['customerCategories']
                })
            }
            else{
                Swal.fire(data['error'])
            }
        })
    }

    complete(){
        this.setState({
            ...this.state,
            loading:false
        })
    }
    loading(){
        this.setState({
            ...this.state,
            loading:true
        })
    }

    async onSubmit(){
            this.loading()
            var data = this.state.update
            data = {...data, 'action':'edit'}
            updateCustomer(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'Customer Details has been updated.',
                            'success'
                          )
                            this.back()
                        }
                    else{
                        Swal.fire({
                            icon:'error',
                            title:data['error']
                        })
                        this.complete()
                    }
                }catch(e){
                    console.log(e)
                }
            })
        this.complete()
    }

    customerDelete(id){
        this.loading()
        var data = {
            'customers_id':[
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
                deleteCustomers(JSON.stringify(data)).then(data=>{
                    try {
                        if (data['status']){
                            Swal.fire({
                                icon:'success',
                                title:'Customer entry has been deleted.',
                                showConfirmButton: false,
                                timer:1000
                            })
                            this.back()
                        }   else{
                            Swal.fire({
                                icon:'error',
                                title:data['error']
                            })
                            this.complete()
                            this.back()
                        }
                    }catch(e){
                        console.log(e)
                    }
                })
              
            }
          })
          this.complete()   
    }
    
    async popUp(id, uuid=0, fromUrl=false){
        this.loading()
        if(!fromUrl){
            this.props.pushNewId(id)
        }else{
            const data = {
                'action':'get',
                'customer_id':id,
            }
            var data_main;
            await getCustomer(JSON.stringify(data)).then(data => {
                if (data['status']){
                    data_main=data
                }
                else {
                    Swal.fire(data['error'])
                    return
                }
            })
            await this.setState({
                'popUp':true,
                'update':data_main['customers'][0],
                'customer':data_main['customers'][0]
            })
        }
        this.complete()
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
        },
        {
            id:5,
            name:"Category",
            prop:'category_str'
        }   
    ]



    render() {
        const catagories = this.state.customerCategories
        var listData
        if (!this.props.data){
            listData = []
        }else{
            listData=this.props.data
        }
        const list = <List data={listData} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
         const popUpRender =
         <div>
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp; <Button  variant="contained" size='small' color="primary" onClick={()=> {this.back()}}>
                <ArrowLeftIcon></ArrowLeftIcon>
         Back
     </Button>
        <Grid  container spacing={3} justify="center" alignContent='center' alignItems="center">
            <Grid item xm={4}>
            
            </Grid>
            <Grid item xs={4}>
            <h1>{this.state.update.name}</h1>
            </Grid>
            <Grid item xm={4}>
            </Grid>
        </Grid>

        <Grid container  justify="center" alignContent='center' alignItems="center">
        <Grid item xm={6}>
            <Grid container spacing={3} justify="center" alignItems="center">
                <Grid item xm={2} > 
                <TextField required id="first_name" label="First Name" name='first_name' defaultValue={this.state.update.first_name} onChange={this.onChange} autoFocus/>
                </Grid>
                <Grid item xm={2}>
                <TextField required id="middle_name" label="Middle Name" name='middle_name' defaultValue={this.state.update.middle_name} onChange={this.onChange} />
                </Grid>
                <Grid item xm={2}>
                <TextField required id="last_name" label="Last Name" name='last_name' defaultValue={this.state.update.last_name} onChange={this.onChange} />
                </Grid>
            </Grid>
            
            <Grid container spacing={3}>
                <Grid item xm={6} md={6}> 
                <FormControl fullWidth>
                <InputLabel htmlFor="email">Email address</InputLabel>
                <Input id="email" required name='email' fullWidth onChange={this.onChange} defaultValue={this.state.update.email}  />
                </FormControl>
                </Grid>
                <Grid item xm={6} md={6}> 
                 <TextField
                                id ='website'
                                name="website"
                                label='Website'
                                type='text'
                                fullWidth
                                onChange={this.onChange}                                
                                defaultValue={this.state.update.website}
                            />

               </Grid>
            </Grid>


            <Grid container spacing={3} >
                
                <Grid item xm={6} md={6}> 
                <TextField
                label="Primary Phone Number"
                                id ='phone1'
                                name="phone1"
                                fullWidth
                                onChange={this.onChange}                                  
                                value={this.state.update.phone1}
                            />
                </Grid>
                <Grid item xm={6} md={6}> 
                 
                <TextField
                    label='Second Phone Number'
                                id ='phone2'
                                name="phone2"
                                fullWidth
                                onChange={this.onChange}                                
                                value={this.state.update.phone2}
                            />

               </Grid>
            </Grid>


            <Grid container spacing={3}>

                <Grid item xm={6} md={6}> 
                <TextField
                                id ='address'
                                name="address"
                                type='text'
                                label='Address'
                                fullWidth
                                onChange={this.onChange}
                                value={this.state.update.address}
                            />
                </Grid>
                <Grid item xm={6} md={6} > 
                <TextField
                                id ='tax_number'
                                name="tax_number"
                                type='number'
                                fullWidth
                                label='Tax Number'
                                onChange={this.onChange}                                
                                value={this.state.update.tax_number}   
                            />
               </Grid>
            </Grid>
            <Grid container spacing={3}>
            <Grid item xm={6} md={6}>
            <Select onChange={this.onChange} fullWidth  value={this.state.update.category}  name='category' id="category">
                {catagories.map(
                    x => (
                    <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                    )
                )}
            </Select>
            </Grid>
            </Grid>
            <Grid container spacing={3}  alignItems='flex-end'>

                <Grid item xm={3} md={6}> 
                <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                onClick={()=>{this.onSubmit()}}
                                >
                                Update
                                </Button>
                </Grid>
                <Grid item xm={3} md={6}> 
                <Button variant="contained" color="secondary" onClick={() => {this.customerDelete(this.state.customer.id)}}>
                    Delete Customer
                </Button> 
               </Grid>
            </Grid>
        </Grid>
        </Grid><br></br>
        </div>
        return (
            <div>
                {this.state.loading ?  <LoadingIcon></LoadingIcon> :this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

CustomerList.propTypes = {
    classes: PropTypes.object.isRequired,
  };


export default withStyles(styles)(CustomerList)
import React, { Component } from 'react'
import List from '../list';
import { getDiscount, updateDiscount,  deleteDiscounts } from '../../api/misc';
import {Button, TextField, Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'

import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


class DiscountList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'discount':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.back = this.back.bind(this)
        this.discountDelete = this.discountDelete.bind(this)
    }
    
    async componentDidMount(){
        try {
            const {id} = this.props.match.params
            if (id){
                await this.popUp(id,0,true)
            }
        }catch(e){
        }
    }

       
    back(){ 
        if (this.props.data){
            this.setState({...this.state, popUp:false});
        }else{
            this.props.history.push('/discounts')
        }
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

    
    onChange(e)
    {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name] : [e.target.value][0]
            }
        })
    }

    
    async onSubmit(){
            var data = this.state.update
            data = {...data, 'action':'edit','discount_id':data.id}
            console.log(data)
            updateDiscount(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'Discounts details has been updated.',
                            'success'
                          )
                        this.back()
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

    discountDelete(id){
        var data = {
            'discounts_id':[
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
                deleteDiscounts(JSON.stringify(data)).then(data=>{
                    try {
                        if (data['status']){
                            Swal.fire({
                                icon:'success',
                                title:'Discount entry has been deleted.',
                                showConfirmButton: false,
                                timer:1000
                            })
                            this.back()
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
    
    async popUp(id, uuid=0, fromUrl=false){
        if(!fromUrl){
            this.props.pushNewId(id)
        }
        else{
            const data = {
                'action':'get',
                'discount_id':id,
            }
            var data_main;
            await getDiscount(JSON.stringify(data)).then(data => {
                if (data['status']){
                    data_main=data
                }
            })
            await this.setState({
                'popUp':true,
                'discount':data_main['discounts'][0],
                'update':data_main['discounts'][0]
            })
        }
    }


    columns = [
        {
            id:1,
            name:"Name",
            prop: 'name'
        },
        {
            id:2,
            name:"Code",
            prop: 'code'
        },
        {
            id:3,
            name:"Discount Type",
            prop: 'discount_type'
        },
        {
            id:4,
            name:"Rate",
            prop: 'rate'
        }      
    ]
    

    render() {
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
        <Grid  container justify="center" alignContent='center' alignItems="center" spacing={3}>
            <Grid item xm={4}>
            
            </Grid>
            <Grid item xs={4}>
            <h1>{this.state.discount.name}</h1>
            </Grid>
            <Grid item xm={4}>
            </Grid>
        </Grid>

        <Grid container  justify="center" alignContent='center' alignItems="center"   direction={'column'} spacing={10}>
        <Grid item xm={6}>
            <Grid container spacing={3} justify="center" alignItems="center">
                <Grid item xm={2} > 
                <TextField required id="name" label="Name" name='name' defaultValue={this.state.discount.name} onChange={this.onChange} autoFocus/>
                </Grid>
                <Grid item xm={2}>
                <TextField required id="code" label="code" name='code' defaultValue={this.state.discount.code} onChange={this.onChange} />
                </Grid>
            </Grid>
            
            <Grid container spacing={3}>
                <Grid item xm={6} md={6}>
                    Discount Type :  
                 <FormControl>
                                <Select onChange={this.onChange}   value={this.state.update.discount_type}  name='discount_type' id="discount_type">
                                <MenuItem value="percent">Percentage</MenuItem>
                                <MenuItem value="fixed">Fixed</MenuItem>
                                </Select>
                            </FormControl>
                </Grid>
                <Grid item xm={6} md={6} > 
                <TextField required id="rate"  name="rate"  label="rate" defaultValue={this.state.discount.rate} onChange={this.onChange} />

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
                <Button variant="contained" color="secondary" onClick={() => {this.discountDelete(this.state.discount.id)}}>
                    Delete Discount
                </Button> 
               </Grid>
            </Grid>
        </Grid>
        </Grid><br></br>
        </div>

        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}


export default (DiscountList)


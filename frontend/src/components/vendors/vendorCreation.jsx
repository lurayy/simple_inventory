import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField , withStyles} from '@material-ui/core';
import { createVendor } from '../../api/inventory/vendorApi';


import {Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';


import {FormControl, InputLabel, Input} from '@material-ui/core'
import Swal from 'sweetalert2'


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


class VendorCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'update':{
                'middle_name':[''],
                'website':[''],
                'phone2':[''],
                'address':['']
            }
        }
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
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
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'add'}
            console.log(data)
            createVendor(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'Vendor details has been added.',
                            'success'
                          )                    }
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

    render() {
        const { classes } = this.props;

        return (
            <div>
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp; 
        <Grid  container spacing={3} justify="center" alignContent='center' alignItems="center">
            <Grid item xm={4}>
            
            </Grid>
            <Grid item xs={4}>
            <h1>Add New Customer</h1>
            </Grid>
            <Grid item xm={4}>
            </Grid>
        </Grid>

        <Grid container  justify="center" alignContent='center' alignItems="center">
        <Grid item xm={6}>
            <Grid container spacing={3} justify="center" alignItems="center">
                <Grid item xm={2} > 
                <TextField required id="first_name" label="First Name" name='first_name' autoFocus onChange={this.onChange} />
                </Grid>
                <Grid item xm={2}>
                <TextField id="middle_name" label="Middle Name" name='middle_name'  onChange={this.onChange} />
                </Grid>
                <Grid item xm={2}>
                <TextField required id="last_name" label="Last Name" name='last_name'  onChange={this.onChange} />
                </Grid>
            </Grid>
            
            <Grid container spacing={3}>
                <Grid item xm={6} md={6}> 
                <FormControl fullWidth required>
                <InputLabel htmlFor="email">Email address</InputLabel>
                <Input id="email" required name='email' fullWidth onChange={this.onChange}   />
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
                                required
                                onChange={this.onChange}                                  
                            />
                </Grid>
                <Grid item xm={6} md={6}> 
                 
                <TextField
                    label='Second Phone Number'
                                id ='phone2'
                                name="phone2"
                                fullWidth
                                onChange={this.onChange}                                
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
                                required
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
                                required                              
                            />
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
                                Add
                                </Button>
                </Grid>
                <Grid item xm={3} md={6}> 
                
               </Grid>
            </Grid>
        </Grid>
        </Grid><br></br>
        </div>
        )
    }
}

VendorCreation.propTypes = {
    classes: PropTypes.object.isRequired,
  };

const mapStateToProps = state => ({
    user: state.user
})

export default withStyles(styles)(connect(mapStateToProps)(VendorCreation))

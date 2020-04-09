import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField,Grid } from '@material-ui/core';
import { createTax } from '../../api/misc';


import { makeStyles } from '@material-ui/core/styles';

import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'

import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';

import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
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


class TaxCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'update':{
                'name':'',
                'code':'',
                'tax_type':'normal',
                'rate':''
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
                [e.target.name] : [e.target.value][0]
            }
        })
    }


    async onSubmit(e){
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele]
            }
            data = {...data, 'action':'add'}
            console.log(data)
            createTax(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'Tax details has been added.',
                            'success'
                          )
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

    render() {
        const { classes } = this.props;

            const popUpRender = 
                <div>
           &nbsp;
           &nbsp;
           &nbsp;
           &nbsp;
           &nbsp;
           &nbsp; 
       <Grid  container justify="center" alignContent='center' alignItems="center" spacing={3}>
           <Grid item xm={4}>
           
           </Grid>
           <Grid item xs={4}>
           <h1>Add New Tax</h1>
           </Grid>
           <Grid item xm={4}>
           </Grid>
       </Grid>

       <Grid container  justify="center" alignContent='center' alignItems="center"   direction={'column'} spacing={10}>
       <Grid item xm={6}>
           <Grid container spacing={3} justify="center" alignItems="center">
               <Grid item xm={2} > 
               <TextField required id="name" label="Name" name='name' defaultValue={this.state.update.name} onChange={this.onChange} autoFocus/>
               </Grid>
               <Grid item xm={2}>
               <TextField required id="code" label="code" name='code' defaultValue={this.state.update.code} onChange={this.onChange} />
               </Grid>
           </Grid>
           
           <Grid container spacing={3}>
               <Grid item xm={6} md={6}>
                   Tax Type :  
                <FormControl className={classes.formControl}>
                               <Select onChange={this.onChange}   value={this.state.update.discount_type}  name='discount_type' id="discount_type">
                               <MenuItem value="percent">Percentage</MenuItem>
                               <MenuItem value="fixed">Fixed</MenuItem>
                               </Select>
                           </FormControl>
               </Grid>
               <Grid item xm={6} md={6} > 
               <TextField required id="rate"  name="rate" onChange={this.onChange} label="rate" name='rate' defaultValue={this.state.update.rate} onChange={this.onChange} />

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
        return (
            popUpRender
        )
    }
}



TaxCreation.propTypes = {
    classes: PropTypes.object.isRequired,
  };


const mapStateToProps = state => ({
    user: state.user
})
export default withStyles(styles)(connect(mapStateToProps)(TaxCreation))

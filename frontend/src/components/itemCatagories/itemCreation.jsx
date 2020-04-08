import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField, Grid } from '@material-ui/core';
import { createItemCatagory } from '../../api/inventory/itemCatagory';

import Swal from 'sweetalert2'

class DiscountCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
           'itemCatagory':{}
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
            'itemCatagory': {
                ...this.state.itemCatagory,
                [e.target.name] : [e.target.value][0]
            }
        })
    }


    async onSubmit(e){
        e.preventDefault();
            var data = {...this.state.itemCatagory}
            data = {...data, 'action':'add'}
            createItemCatagory(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire(
                            'Updated!',
                            'ItemCatagory Data has been added.',
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
        const popUpRender =
        <div>
        <Grid container justify='center'>
        <Grid item xm={6}>
                                <form onSubmit={this.onSubmit}>
                                    <table>
                                        <tbody>
                                        <tr>
                                            <td>
                                            Name: 
                                            </td>
                                            <td>
                                            <TextField
                                        id ='name'
                                        name="name"
                                        type='text'
                                        onChange={this.onChange}  
                                        defaultValue={this.state.itemCatagory.name}          
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
                                        Add
                                        </Button>
        </td>
        <td>

        </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                   
                                   
                                
                        </form>
                    
        </Grid>
                    </Grid>
                    
                    </div>
        return (
            popUpRender
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(DiscountCreation)
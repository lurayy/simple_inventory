import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField, Grid } from '@material-ui/core';
import { createPlace } from '../../api/inventory/placeApi';
import Swal from 'sweetalert2';


class PlaceCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'update':{
            }
        }
    }

    async componentDidMount() {
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
        e.preventDefault();
            var data = {...this.state.update}
            data = {...data, 'action':'add'}
            console.log(data)
            createPlace(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        Swal.fire("New Place Added")
                    }
                    else{
                        Swal.fire(data['error'])
                    }
                }catch(e){
                    console.log(e)
                }
            })
    }

    render() {
        const popUpRender = <div>
            <Grid container justify='center'>
                <Grid item>
                    
<form onSubmit={this.onSubmit}>
                    <table cellPadding={10} cellSpacing={10}>
                        <tbody >
                            <tr>
<td>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}      
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
                                Create</Button>
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

export default connect(mapStateToProps)(PlaceCreation)
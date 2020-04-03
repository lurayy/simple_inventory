import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField } from '@material-ui/core';
import { createPlace } from '../../api/inventory/placeApi';


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
                        alert("New Place Added")
                    }
                    else{
                        alert(data['error'])
                    }
                }catch(e){
                    console.log(e)
                }
            })
    }

    render() {
        const popUpRender = <div>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}      
                            />
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Create</Button>
                </form>
            
                        <br>
                        </br>
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
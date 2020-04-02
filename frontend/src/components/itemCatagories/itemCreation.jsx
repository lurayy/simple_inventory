import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField } from '@material-ui/core';
import { createItemCatagory } from '../../api/inventory/itemCatagory';


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
                        alert("New Item Catagory Added")
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
                                placeholder={this.state.itemCatagory.name}          
                            />
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Add
                                </Button>
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

export default connect(mapStateToProps)(DiscountCreation)
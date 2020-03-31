import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField } from '@material-ui/core';
import { createCustomer } from '../../api/sales/customer';


class CustomerCreation extends Component {

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
        e.preventDefault();
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'add'}
            createCustomer(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("New Customer Added")
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
        return (
            <div>
                <h1>Add New Vendor</h1>
                <form onSubmit={this.onSubmit}>
                            First Name: <TextField
                                id ='first_name'
                                name="first_name"
                                type='text'
                                onChange={this.onChange}  
                                required                  
                            />
                            Middle Name : <TextField
                                id ='middle_name'
                                name="middle_name"
                                type='text'
                                onChange={this.onChange} 
                            />
                            Last Name  : <TextField
                                id ='last_name'
                                name="last_name"
                                type='text'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            Email : <TextField
                                id ='email'
                                name="email"
                                type='email'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            Website : <TextField
                                id ='website'
                                name="website"
                                type='text'
                                onChange={this.onChange}
                            />
                            <br></br>
                            Tax Number : <TextField
                                id ='tax_number'
                                name="tax_number"
                                type='number'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            Contact Number: <TextField
                                id ='phone1'
                                name="phone1"
                                type='number'
                                onChange={this.onChange}
                                required 
                            />
                            <br></br>
                            Contact Number 2 : <TextField
                                id ='phone2'
                                name="phone2"
                                type='number'
                                onChange={this.onChange}
                            />
                            <br></br>
                            
                            Addresss : <TextField
                                id ='address'
                                name="address"
                                type='text'
                                onChange={this.onChange}
                            />
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button>
                        
                </form>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    user: state.user
})

export default connect(mapStateToProps)(CustomerCreation)
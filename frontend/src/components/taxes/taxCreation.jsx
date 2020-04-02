import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField } from '@material-ui/core';
import { createTax } from '../../api/misc';


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
        e.preventDefault();
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
                        alert("New Tax type Added")
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
                            Code : <TextField
                                id ='code'
                                name="code"
                                type='text'
                                onChange={this.onChange}
                            />
                             Tax Type :<select name='tax_type' id="tax_type" value={this.state.update.discont_type}  onChange={this.onChange}>
                                    <option value="normal">Normal</option>
                                    <option value="fixed">Fixed</option>
                                </select> <br></br>
                            Rate : <input  name="rate" id="rate" type='number' onChange={this.onChange} value={this.state.update.rate} ></input><br></br>
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Create
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

export default connect(mapStateToProps)(TaxCreation)
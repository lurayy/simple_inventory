import React, { Component } from 'react'
import {  connect } from 'react-redux';
import {Button, TextField } from '@material-ui/core';
import { createItem } from '../../api/inventory/itemApi';
import {getItemCatagories} from '../../api/inventory/itemCatagory'


class ItemCreation extends Component {

    constructor (props){
        super(props)
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {
            'catagories':[],
            'update':{
            }
        }
    }

    async componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        var data = {
            'action':'get',
            'start':0,
            'end':50
        }
        await getItemCatagories(JSON.stringify(data)).then(data=> {
            try { 
                if (data['status']){
                    this.setState({
                        ...this.state,
                        'catagories':data['item_catagories']
                    })
                }
                else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
            }
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


    async onSubmit(e){
        e.preventDefault();
            var data = {...this.state.update}
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele]
            }
            data = {...data, 'action':'add'}
            console.log(data)
            createItem(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("New Item Added")
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
        const catagories = this.state.catagories
        const popUpRender = <div>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}      
                            />
                            Catagory : <select name='catagory' id="catagory" onChange={this.onChange} required >
                                {catagories.map(
                                    x => (
                                    <option key={x.id} value={parseInt(x.id)}>{x.name}</option>
                                    )
                                )}
                            </select> <br></br><br></br>
                            
                            Sales Price : <input name='sales_price' type='float' onChange={this.onChange}></input><br></br>

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

export default connect(mapStateToProps)(ItemCreation)
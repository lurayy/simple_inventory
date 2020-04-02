import React, { Component } from 'react'
import List from '../list';
import { getDiscount, updateDiscount,  deleteDiscounts } from '../../api/misc';
import {Button, TextField } from '@material-ui/core';

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
        this.discountDelete = this.discountDelete.bind(this)
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
            var data = this.state.discount
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit','discount_id':data.id}
            console.log(data)
            updateDiscount(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Discount Data updated.")
                        this.props.update(0)
                    }
                    else{
                        alert(data['error'])
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
        deleteDiscounts(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Discount data deleted.')
                    this.props.update(0)
                }   else{
                    alert(data['error'])
                }
            }catch(e){
                console.log(e)
            }
        })
    }
    
    async popUp(id, uuid=0){
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
            'discount':data_main['discounts'][0]
        })
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
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>
                        <button onClick={()=> {this.setState({'popUp':false})}}>Back</button><br></br>
                        <h1>{this.state.discount.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.discount.name}          
                            />
                            Code : <TextField
                                id ='code'
                                name="code"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.discount.code} 
                            />
                             Discount Type :<select name='discount_type' id="discount_type" defaultValue={this.state.discount.discount_type}  onChange={this.onChange}>
                                    <option value="percent">Percentage</option>
                                    <option value="fixed">Fixed</option>
                                </select> <br></br>
                            Rate : <input placeholder={this.state.discount.rate} name="rate" onChange={this.onChange} ></input><br></br>
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.discountDelete(this.state.discount.id)}}>
                            Delete Discount
                        </Button> 
                        
                </form>
            
                        <br>
                        </br>
                    </div>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default DiscountList

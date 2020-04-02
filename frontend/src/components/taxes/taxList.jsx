import React, { Component } from 'react'
import List from '../list';
import { getTax, updateTax,  deleteTaxes } from '../../api/misc';
import {Button, TextField } from '@material-ui/core';

class TaxList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'tax':{},
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.taxDelete = this.taxDelete.bind(this)
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
            var data = this.state.tax
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit','tax_id':data.id}
            console.log(data)
            updateTax(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Tax Data updated.")
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

    taxDelete(id){
        var data = {
            'taxes_id':[
                id
            ]
        }
        deleteTaxes(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Tax data deleted.')
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
            'tax_id':id,
        }
        var data_main;
        await getTax(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'tax':data_main['taxes'][0]
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
            name:"Tax Type",
            prop: 'tax_type'
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
                        <h1>{this.state.tax.name}</h1>
                        <form onSubmit={this.onSubmit}>
                            Name: <TextField
                                id ='name'
                                name="name"
                                type='text'
                                onChange={this.onChange}  
                                placeholder={this.state.tax.name}          
                            />
                            Code : <TextField
                                id ='code'
                                name="code"
                                type='text'
                                onChange={this.onChange}
                                placeholder={this.state.tax.code} 
                            />
                             Tax Type :<select name='tax_type' id="tax_type" defaultValue={this.state.tax.tax_type}  onChange={this.onChange}>
                                    <option value="percent">Percentage</option>
                                    <option value="fixed">Fixed</option>
                                </select> <br></br>
                            Rate : <input placeholder={this.state.tax.rate} name="rate" onChange={this.onChangePI} ></input><br></br>
                            <br></br>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                >
                                Update
                                </Button> <Button variant="contained" color="secondary" onClick={() => {this.taxDelete(this.state.tax.id)}}>
                            Delete Tax
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

export default TaxList

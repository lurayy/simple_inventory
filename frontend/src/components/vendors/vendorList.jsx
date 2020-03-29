import React, { Component } from 'react'
import List from '../list';
import { getVendor } from '../../api/inventory/vendorApi';

class VendorList extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'vendor':{},
            'update':{}
        }
        // this.onChange = this.onChange.bind(this);
        // this.onSubmit = this.onSubmit.bind(this);
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

    
    async popUp(id, uuid=0){
        const data = {
            'action':'get',
            'vendor_id':id,
        }
        var data_main;
        await getVendor(JSON.stringify(data)).then(data => {
            if (data['status']){
                data_main=data
            }
        })
        await this.setState({
            'popUp':true,
            'vendor_data':data_main
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
            name:"Phone Number",
            prop: 'phone1'
        },
        {
            id:3,
            name:"Email",
            prop: 'email'
        },
        {
            id:4,
            name:"Address",
            prop: 'address'
        }      
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        return (
            <div>
                {list}
            </div>
        )
    }
}

export default VendorList

import React, { Component } from 'react'
import List from '../list';
import { getInvoice, deleteInvoices, updateInvoice } from '../../api/sales/invoice';
import PopUpEdit from './popUpEdit';

class InvoiceListing extends Component {
    
    constructor(props){
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp':false,
            'invoices':{},
            'invoice_items':[],
            'update':{}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.invoiceDelete = this.invoiceDelete.bind(this)
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
            var data = this.state.vendor
            var ele;
            for (ele in this.state.update){
                data[ele] = this.state.update[ele][0]
            }
            data = {...data, 'action':'edit'}
            updateInvoice(JSON.stringify(data)).then(data=> {
                try { 
                    if (data['status']){
                        alert("Vendor Data updated.")
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

    invoiceDelete(id){
        var data = {
            'invoices_id':[
                id
            ]
        }
        deleteInvoices(JSON.stringify(data)).then(data=>{
            try {
                if (data['status']){
                    alert('Invoice has been Deleted.')
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
            'invoice_id':id,
        }
        var data_main;
        await getInvoice(JSON.stringify(data)).then(data => {
            if (data['status']){
                console.log(data)
                data_main=data
            }
            else{
                alert(data['error'])
            }
        })
        if (data_main['invoice_items'].length === 0) {
            console.log("blank")
            data_main['invoice_items'] = [{
                id:0
            }]
        }
        await this.setState({
            'popUp':true,
            'invoice':data_main['invoice'][0],
            'invoice_items':data_main['invoice_items']
        })
    }


    columns = [
        {
            id:1,
            name:"Customer's Name",
            prop: 'customer_name'
        },
        {
            id:2,
            name:"Sold By",
            prop: 'added_by_name'
        },
        {
            id:3,
            name:"Paid Amount",
            prop: 'paid_amount'
        },
        {
            id:4,
            name:"Order Number",
            prop: 'order_number'
        },
        {
            id:5,
            name:'Invoiced On',
            prop:'invoiced_on_str'
        },
        {
            id:6,
            name:'Status',
            prop:'status_name'
        }
    ]
    

    render() {
        const list = <List data={this.props.data} header={this.columns}   popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <PopUpEdit invoice={this.state.invoice} invoice_items={this.state.invoice_items} update={this.props.update} delete={this.invoiceDelete} ></PopUpEdit>
        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}

export default InvoiceListing

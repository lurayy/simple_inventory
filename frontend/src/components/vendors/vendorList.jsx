import React, { Component } from 'react'
import List from '../list';
import { getVendor, updateVendor, deleteVendors } from '../../api/inventory/vendorApi';
import { Button, TextField, Grid } from '@material-ui/core';

import { FormControl, InputLabel, Input } from '@material-ui/core'
import Swal from 'sweetalert2'
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';

class VendorList extends Component {

    constructor(props) {
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp': false,
            'vendor': {},
            'update': {}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.back = this.back.bind(this)
        this.vendorDelete = this.vendorDelete.bind(this)
    }

    onChange(e) {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name]: [e.target.value][0]
            }
        })
    }

    back() {
        if (this.props.data) {
            this.setState({ ...this.state, popUp: false });
        } else {
            this.props.history.push('/vendors')
        }
    }
    async componentDidMount() {
        try {
            const { id } = this.props.match.params
            if (id) {
                await this.popUp(id, 0, true)
            }
        } catch (e) {
            console.log(e)
        }
    }
    async onSubmit() {
        var data = this.state.update
        data = { ...data, 'action': 'edit' }
        console.log(data)
        updateVendor(JSON.stringify(data)).then(data => {
            try {
                if (data['status']) {
                    Swal.fire(
                        'Updated!',
                        'Vendor Details has been updated.',
                        'success'
                    )
                    this.back()
                }
                else {
                    Swal.fire({
                        icon: 'error',
                        title: data['error']
                    })
                }
            } catch (e) {
                console.log(e)
            }
        })
    }

    vendorDelete(id) {
        var data = {
            'vendors_id': [
                id
            ]
        }
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            deleteVendors(JSON.stringify(data)).then(data => {
                try {
                    if (data['status']) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Vendor entry has been deleted.',
                            showConfirmButton: false,
                            timer: 1000
                        })
                        this.back()
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: data['error']
                        })
                    }
                } catch (e) {
                    console.log(e)
                }
            })
        })
    }

    async popUp(id, uuid = 0, fromUrl) {
        if (!fromUrl) {
            this.props.pushNewId(id)
        } else {
            const data = {
                'action': 'get',
                'vendor_id': id,
            }
            var data_main;
            await getVendor(JSON.stringify(data)).then(data => {
                if (data['status']) {
                    data_main = data
                }
            })
            await this.setState({
                'popUp': true,
                'vendor': data_main['vendors'][0],
                'update': data_main['vendors'][0]
            })
        }
    }


    columns = [
        {
            id: 1,
            name: "Name",
            prop: 'name'
        },
        {
            id: 2,
            name: "Phone Number",
            prop: 'phone1'
        },
        {
            id: 3,
            name: "Email",
            prop: 'email'
        },
        {
            id: 4,
            name: "Address",
            prop: 'address'
        }
    ]


    render() {
        var listData
        if (!this.props.data) {
            listData = []
        } else {
            listData = this.props.data
        }
        const list = <List data={listData} header={this.columns} popUp={this.popUp} update={this.props.update} page={this.props.page} />
        const popUpRender = <div>


            <Grid container spacing={3} justify="center" alignContent='center' alignItems="center">

                <Grid item xm={4}>
                    <Button variant="contained" size='small' color="primary" onClick={() => { this.back() }}>
                        <ArrowLeftIcon></ArrowLeftIcon>
         Back
     </Button>          <h1>{this.state.update.name}</h1>
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;

            </Grid>
                <Grid item xm={4}>
                </Grid>
            </Grid>

            <Grid container justify="center" alignContent='center' alignItems="center">
                <Grid item xm={6}>
                    <Grid container spacing={3} justify="center" alignItems="center">
                        <Grid item xm={2} >
                            <TextField required value={this.state.update.first_name} id="first_name" label="First Name" name='first_name' autoFocus onChange={this.onChange} />
                        </Grid>
                        <Grid item xm={2}>
                            <TextField id="middle_name" value={this.state.update.middle_name} label="Middle Name" name='middle_name' onChange={this.onChange} />
                        </Grid>
                        <Grid item xm={2}>
                            <TextField required id="last_name" value={this.state.update.last_name} label="Last Name" name='last_name' onChange={this.onChange} />
                        </Grid>
                    </Grid>

                    <Grid container spacing={3}>
                        <Grid item xm={6} md={6}>
                            <FormControl fullWidth required>
                                <InputLabel htmlFor="email">Email address</InputLabel>
                                <Input id="email" required name='email' value={this.state.update.email} fullWidth onChange={this.onChange} />
                            </FormControl>
                        </Grid>
                        <Grid item xm={6} md={6}>
                            <TextField
                                id='website'
                                name="website"
                                label='Website'
                                value={this.state.update.website}
                                type='text'
                                fullWidth
                                onChange={this.onChange}
                            />

                        </Grid>
                    </Grid>


                    <Grid container spacing={3} >

                        <Grid item xm={6} md={6}>
                            <TextField
                                label="Primary Phone Number"
                                id='phone1'
                                value={this.state.update.phone1}
                                name="phone1"
                                fullWidth
                                required
                                onChange={this.onChange}
                            />
                        </Grid>
                        <Grid item xm={6} md={6}>

                            <TextField
                                label='Second Phone Number'
                                id='phone2'
                                name="phone2"
                                value={this.state.update.phone2}
                                fullWidth
                                onChange={this.onChange}
                            />

                        </Grid>
                    </Grid>


                    <Grid container spacing={3}>

                        <Grid item xm={6} md={6}>
                            <TextField
                                id='address'
                                name="address"
                                type='text'
                                label='Address'
                                value={this.state.update.address}
                                fullWidth
                                onChange={this.onChange}
                                required
                            />
                        </Grid>
                        <Grid item xm={6} md={6} >
                            <TextField
                                id='tax_number'
                                name="tax_number"
                                type='number'
                                fullWidth
                                label='Tax Number'
                                value={this.state.update.tax_number}
                                onChange={this.onChange}
                                required
                            />
                        </Grid>
                    </Grid>
                    <Grid container spacing={3} alignItems='flex-end'>

                        <Grid item xm={3} md={6}>
                            <Button
                                type='submit'
                                variant="contained"
                                color="primary"
                                onClick={() => { this.onSubmit() }}
                            >
                                Update
                                </Button>
                        </Grid><Grid item xm={3} md={6}>
                            <Button variant="contained" color="secondary" onClick={() => { this.vendorDelete(this.state.update.id) }}>
                                Delete Vendor
                </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>

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

export default VendorList

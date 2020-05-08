import React, { Component } from 'react'
import List from '../list';
import { getGiftCard, deleteGiftCards, updateGiftCard } from '../../api/payment/giftCards';
import { Button, TextField, Grid } from '@material-ui/core';

import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import Swal from 'sweetalert2'

import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


class GiftCardList extends Component {

    constructor(props) {
        super(props)
        this.popUp = this.popUp.bind(this)
        this.state = {
            'popUp': false,
            'update': {}
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.back = this.back.bind(this)
        this.giftCardDelete = this.giftCard.bind(this)
    }

    async componentDidMount() {
        try {
            const { id } = this.props.match.params
            if (id) {
                await this.popUp(id, 0, true)
            }
        } catch (e) {
        }
    }


    back() {
        if (this.props.data) {
            this.setState({ ...this.state, popUp: false });
        } else {
            this.props.history.push('/cards')
        }
    }
    complete() {
        this.setState({
            ...this.state,
            loading: false
        })
    }
    loading() {
        this.setState({
            ...this.state,
            loading: true
        })
    }


    onChange(e) {
        this.setState({
            'update': {
                ...this.state.update,
                [e.target.name]: [e.target.value][0]
            }
        })
    }


    async onSubmit() {
        var data = this.state.update
        data = { ...data, 'action': 'edit', 'giftCardUUID': data.uuid }
        console.log(data)
        updateGiftCard(JSON.stringify(data)).then(data => {
            try {
                if (data['status']) {
                    Swal.fire(
                        'Updated!',
                        'Gift Card details has been updated.',
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

    giftCard(uuid) {
        var data = {
            'giftCardsUUID': [
                uuid
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
            if (result.value) {
                deleteGiftCards(JSON.stringify(data)).then(data => {
                    try {
                        if (data['status']) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Gift Card Has Been Deleted.',
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

            }
        })
    }

    async popUp(uuid, temp = 0, fromUrl = false) {
        if (!fromUrl) {
            this.props.pushNewId(uuid)
        }
        else {
            const data = {
                'action': 'get',
                'gitfCardUUID': uuid,
            }
            var data_main;
            await getGiftCard(JSON.stringify(data)).then(data => {
                if (data['status']) {
                    data_main = data
                }
            })
            await this.setState({
                'popUp': true,
                'giftCards': data_main['giftCards'][0],
                'update': data_main['giftCards'][0]
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
            name: "Code",
            prop: 'code'
        },
        {
            id: 3,
            name: "Discount Type",
            prop: 'discount_type'
        },
        {
            id: 4,
            name: "Rate",
            prop: 'rate'
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

        const popUpRender =
            <div>
                &nbsp;
                &nbsp;
                &nbsp;
                &nbsp;
                &nbsp;
            &nbsp; <Button variant="contained" size='small' color="primary" onClick={() => { this.back() }}>
                    <ArrowLeftIcon></ArrowLeftIcon>
         Back
     </Button>
                <Grid container justify="center" alignContent='center' alignItems="center" spacing={3}>
                    <Grid item xm={4}>

                    </Grid>
                    <Grid item xs={4}>
                        <h1>{this.state.discount.name}</h1>
                    </Grid>
                    <Grid item xm={4}>
                    </Grid>
                </Grid>

                <Grid container justify="center" alignContent='center' alignItems="center" direction={'column'} spacing={10}>
                    <Grid item xm={6}>
                        <Grid container spacing={3} justify="center" alignItems="center">
                            <Grid item xm={2} >
                                <TextField required id="name" label="Name" name='name' defaultValue={this.state.discount.name} onChange={this.onChange} autoFocus />
                            </Grid>
                            <Grid item xm={2}>
                                <TextField required id="code" label="code" name='code' defaultValue={this.state.discount.code} onChange={this.onChange} />
                            </Grid>
                        </Grid>

                        <Grid container spacing={3}>
                            <Grid item xm={6} md={6}>
                                Discount Type :
                 <FormControl>
                                    <Select onChange={this.onChange} value={this.state.update.discount_type} name='discount_type' id="discount_type">
                                        <MenuItem value="percent">Percentage</MenuItem>
                                        <MenuItem value="fixed">Fixed</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid item xm={6} md={6} >
                                <TextField required id="rate" name="rate" label="rate" defaultValue={this.state.discount.rate} onChange={this.onChange} />

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
                            </Grid>
                            <Grid item xm={3} md={6}>
                                <Button variant="contained" color="secondary" onClick={() => { this.giftCard(this.state.discount.id) }}>
                                    Delete Discount
                </Button>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid><br></br>
            </div>

        return (
            <div>
                {this.state.popUp ? popUpRender : list}
            </div>
        )
    }
}


export default (GiftCardList)


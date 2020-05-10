import React, { Component } from 'react'
import { getItems } from '../../api//inventory/itemApi';
import { connect } from 'react-redux';
import ItemList from './itemList';
import { Link } from 'react-router-dom';


import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import LoadingIcon from '../loading';
import MenuItem from '@material-ui/core/MenuItem';
import { Select } from '@material-ui/core'
import RefreshIcon from '@material-ui/icons/Refresh';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import { TextField } from '@material-ui/core'
import { getItemCatagories } from '../../api/inventory/itemCatagory'

import Swal from 'sweetalert2'


const styles = makeStyles((theme) => ({
    root: {
        flexGrow: 12,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
}));


class Items extends Component {
    constructor(props) {
        super(props)
        this.state = {
            'item_catagories': [],
            'items': [],
            'loaded': false,
            'start': 0,
            'end': 10,
            'page': 1,
            'result': 'No result',
            'dialog_open': false,
            'filters': {
                exact_name: true,
                is_applied_name: false,
                is_applied_weight_from: false,
                is_applied_weight_upto: false,
                is_applied_average_cost_price_from: false,
                is_applied_average_cost_price_upto: false,
                is_applied_catagory: false,
                is_applied_stock_from: false,
                is_applied_stock_upto: false,
                is_applied_sales_price_from: false,
                is_applied_sales_price_upto: false,
                is_applied_sold_from: false,
                is_applied_sold_upto: false,
            },

        }
        this.update_table = this.update_table.bind(this)
        this.handleFilterChange = this.handleFilterChange.bind(this)
        this.pushNewId = this.pushNewId.bind(this)
    }


    pushNewId(id) {
        this.props.history.push('/items/' + id)
    }

    handleScan = data => {
        if (data) {
            this.setState({
                ...this.state,
                result: data
            })
        }
    }
    handleError = err => {
        console.error(err)
    }


    async componentDidMount() {
        console.log(this.props.user.isLoggedIn)
        if (this.props.user.isLoggedIn === false) {
            this.props.history.push('/')
        }
        var data = {
            'action': 'get',
            'start': 0,
            'end': 50
        }
        await getItemCatagories(JSON.stringify(data)).then(data => {
            try {
                if (data['status']) {
                    this.setState({
                        ...this.state,
                        'item_catagories': data['item_catagories']
                    })
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
        this.update_table(0)
    }

    handleFilterChange(e) {
        var temp = "is_applied_" + e.target.name
        if (e.target.name === "exact_name") {
            this.setState({
                ...this.state,
                filters: {
                    ...this.state.filters,
                    exact_name: !(this.state.filters.exact_name)
                }
            })
        } else {
            this.setState({
                ...this.state,
                filters: {
                    ...this.state.filters,
                    [temp]: true,
                    [e.target.name]: e.target.value
                }
            })
        }
    }

    async update_table(by) {
        var x = by < 0 ? -1 : 1
        if (by === 0) {
            await this.setState({
                ...this.state,
                'loaded': false,
                start: 0,
                end: 10,
                page: 1
            })
        }
        else {
            if (this.state.start + by > -1) {
                await this.setState({
                    ...this.state,
                    'loaded': false,
                    start: this.state.start + by,
                    end: this.state.end + by,
                    page: this.state.page + x
                })
            }
            else {
                alert("Cannot move futher from here.")
                return
            }
        }
        var request_json = {
            'action': 'get',
            'filter': 'multiple',
            'start': this.state.start,
            'end': this.state.end,
            'filters': this.state.filters
        }
        this.getItemsData(request_json)
    }

    async getItemsData(request_json) {
        await getItems(JSON.stringify(request_json)).then(data => {
            if (data['status']) {
                this.setState({
                    ...this.state,
                    'items': data['items'],
                    'loaded': true
                })
            }
        })
    }



    render() {
        const catagories = this.state.item_catagories
        const render_after_load = (
            <div>
                <ItemList pushNewId={this.pushNewId} data={this.state.items} update={this.update_table} page={this.state.page} />
            </div>
        )


        return (
            <div>

                <Grid container
                    spacing={2}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <h2 style={{ marginTop: 0 }}>
                        Items
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>
                        <Link to='/items/create' style={{ textDecoration: 'none' }}>
                            <Button style={{ margin: '5px 10px' }} variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Add New Item
                            </Button>
                        </Link>
                    </div>
                    <Grid item md={10}>
                        <table cellSpacing={5} cellPadding={5}>
                            <tbody>
                                <tr>
                                    <th colSpan={2}>
                                        Name
                                            </th>

                                    <th colSpan={2}>
                                        Weight
                                            </th>
                                </tr>
                                <tr>
                                    <td>
                                        <TextField id="name" size='small' variant="outlined" name="name" defaultValue={this.state.filters.name} onChange={this.handleFilterChange} label="Name" />
                                    </td>
                                    <td>
                                        <FormControlLabel
                                            control={<Switch checked={this.state.filters.exact_name} onChange={this.handleFilterChange} name='exact_name' />}
                                            label={this.state.filters.exact_name ? "Match Exactly" : "Partial Match"}
                                        />
                                    </td>
                                    <td>
                                        <TextField id="weight_from" size='small' variant="outlined" defaultValue={this.state.filters.weight_from} name="weight_from" type='number' onChange={this.handleFilterChange} label="Start Weight" />
                                    </td>
                                    <td>
                                        <TextField id="weight_upto" size='small' variant="outlined" name="weight_upto" type='number' defaultValue={this.state.filters.weight_upto} onChange={this.handleFilterChange} label="Start Upto" />
                                    </td>
                                </tr>
                                <tr>
                                    <th colSpan={2}>
                                        Average Cost Price
                                            </th>

                                    <th colSpan={2}>
                                        Catagory
                                            </th>
                                </tr>
                                <tr>
                                    <td>
                                        <TextField id="average_cost_price_from" size='small' variant="outlined" name="average_cost_price_from" defaultValue={this.state.filters.average_cost_price_from} type='number' onChange={this.handleFilterChange} label="ACP From" />
                                    </td>
                                    <td>
                                        <TextField id="average_cost_price_upto" size='small' variant="outlined" name="average_cost_price_upto" type='number' defaultValue={this.state.filters.average_cost_price_upto} onChange={this.handleFilterChange} label="ACP Upto" />
                                    </td>

                                    <td colSpan={2}>
                                        <Select fullWidth name='catagory' id="catagory" defaultValue={this.state.filters.catagory} onChange={this.handleFilterChange} required >
                                            {catagories.map(
                                                x => (
                                                    <MenuItem key={x.id} value={parseInt(x.id)}>{x.name}</MenuItem>
                                                )
                                            )}
                                        </Select>
                                    </td>
                                </tr>

                                <tr>
                                    <th colSpan={2}>
                                        Stock
                                            </th>

                                    <th colSpan={2}>
                                        Sales Price
                                            </th>
                                </tr>
                                <tr>
                                    <td>
                                        <TextField id="stock_from" variant="outlined" size='small' name="stock_from" type='number' defaultValue={this.state.filters.stock_from} onChange={this.handleFilterChange} label="Stock From" />
                                    </td>
                                    <td>
                                        <TextField id="stock_upto" variant="outlined" size='small' name="stock_upto" type='number' defaultValue={this.state.filters.stock_upto} onChange={this.handleFilterChange} label="Stock Upto" />
                                    </td>

                                    <td>
                                        <TextField id="sales_price_from" variant="outlined" size='small' name="sales_price_from" type='number' defaultValue={this.state.filters.sales_price_from} onChange={this.handleFilterChange} label="Sales Price From" />
                                    </td>
                                    <td>
                                        <TextField id="sales_price_upto" variant="outlined" size='small' name="sales_price_upto" type='number' onChange={this.handleFilterChange} defaultValue={this.state.filters.sales_price_upto} label="Sales Price Upto" />
                                    </td>
                                </tr>
                                <tr>
                                    <th colSpan={2}>
                                        Sold
                                            </th>
                                </tr>
                                <tr>
                                    <td>
                                        <TextField id="sold_from" size='small' variant="outlined" size='small' name="sold_from" type='number' defaultValue={this.state.filters.sold_from} onChange={this.handleFilterChange} label="Sold From" />
                                    </td>
                                    <td>
                                        <TextField id="sold_upto" variant="outlined" name="sold_upto" size='small' type='number' onChange={this.handleFilterChange} defaultValue={this.state.filters.sold_upto} label="Sold Upto" />
                                    </td>
                                    <td colSpan={2}>
                                        <Button variant="contained" color="primary" onClick={() => this.update_table(0)} >
                                            Show Filtered Data
                                                </Button>
                                    </td>
                                </tr>

                            </tbody>
                        </table>
                        <Paper >
                            {this.state.loaded ? render_after_load : <LoadingIcon></LoadingIcon>}
                        </Paper>
                    </Grid>

                </Grid>
            </div>
        )
    }
}





const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Items);

import React, { Component } from 'react'
import { getInvoices } from '../../api/sales/invoice';
import { connect } from 'react-redux';
import InvoiceListing from './invoiceListing';
import { Link } from 'react-router-dom';


import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import RefreshIcon from '@material-ui/icons/Refresh';
import LoadingIcon from '../loading';

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


class Invoices extends Component {
    constructor(props) {
        super(props)
        this.state = {
            'invoices': [],
            'loaded': false,
            'start': 0,
            'end': 10,
            'page': 1
        }
        this.update_table = this.update_table.bind(this)
        this.pushNewId = this.pushNewId.bind(this)
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false) {
            this.props.history.push('/')
        }
        this.update_table(0)
    }

    async update_table(by) {
        var x = by < 0 ? -1 : 1
        if (by === 0) {
            await this.setState({
                'loaded': false,
                start: 0,
                end: 10,
                page: 1
            })
        }
        else {
            if (this.state.start + by > -1) {
                await this.setState({
                    'loaded': false,
                    start: this.state.start + by,
                    end: this.state.end + by,
                    page: this.state.page + x
                })
            }
            else {
                Swal.fire({
                    icon: 'error',
                    title: 'cannot go any further'
                })
                return
            }
        }
        var request_json = {
            'action': 'get',
            'filter': 'none',
            'start': this.state.start,
            'end': this.state.end
        }
        this.getInvoiceData(request_json)
    }

    async getInvoiceData(request_json) {
        var invoice
        await getInvoices(JSON.stringify(request_json)).then(data => {
            if (data['status']) {
                for (invoice in data['invoices']) {
                    data['invoices'][invoice]['invoiced_on_str'] = (data['invoices'][invoice]['invoiced_on']).split('T')[0]
                    data['invoices'][invoice]['due_on_str'] = (data['invoices'][invoice]['due_on']).split('T')[0]
                }
                this.setState({
                    'invoices': data['invoices'],
                    'loaded': true
                })
            }
            else {
                Swal.fire(data['error'])
            }
        })
    }

    pushNewId(id) {
        this.props.history.push('/invoices/' + id)
    }




    render() {

        const render_after_load = (
            <div>
                <InvoiceListing pushNewId={this.pushNewId} data={this.state.invoices} update={this.update_table} page={this.state.page} />
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
                        Invoices
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>

                        <Link to='/invoices/create' style={{ textDecoration: 'none' }}>
                            <Button style={{ margin: '5px 10px' }} variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Add New Invoice
                            </Button>
                        </Link>
                    </div>

                    <Grid item xs={12}>
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
export default connect(mapStateToProps)(Invoices)

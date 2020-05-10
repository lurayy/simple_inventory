import React, { Component } from 'react'
import { getDiscounts } from '../../api/misc';
import { connect } from 'react-redux';
import DiscountList from './discountList';
import { Link } from 'react-router-dom';

import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import RefreshIcon from '@material-ui/icons/Refresh';
import LoadingIcon from '../loading';




class Discounts extends Component {
    constructor(props) {
        super(props)
        this.state = {
            'taxes': [],
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
                alert("Cannot move futher from here.")
                return
            }
        }
        var request_json = {
            'action': 'get',
            'filter': 'none',
            'start': this.state.start,
            'end': this.state.end
        }
        this.getDiscountsData(request_json)
    }

    async getDiscountsData(request_json) {
        await getDiscounts(JSON.stringify(request_json)).then(data => {
            if (data['status']) {
                this.setState({
                    'discounts': data['discounts'],
                    'loaded': true
                })
            }
        })
    }

    pushNewId(id) {
        this.props.history.push('/discounts/' + id)
    }




    render() {

        const render_after_load = (
            <div>
                <DiscountList pushNewId={this.pushNewId} data={this.state.discounts} update={this.update_table} page={this.state.page} />
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
                        Discounts
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>
                        <Link to='/discounts/create' style={{ textDecoration: 'none' }}>
                            <Button variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Add New Discount
                            </Button>
                        </Link>
                    </div>

                    <Grid item xs={12}>
                        <Paper>
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

export default connect(mapStateToProps)(Discounts)
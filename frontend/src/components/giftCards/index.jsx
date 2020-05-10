import React, { Component } from 'react'
import { getGiftCards } from '../../api/payment/giftCards';
import { connect } from 'react-redux';
import GiftCardList from './cardList';
import { Link } from 'react-router-dom';

import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import RefreshIcon from '@material-ui/icons/Refresh';
import LoadingIcon from '../loading';


class GiftCards extends Component {
    constructor(props) {
        super(props)
        this.state = {
            'giftCards': [],
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
        this.getGiftCardsData(request_json)
    }

    async getGiftCardsData(request_json) {
        await getGiftCards(JSON.stringify(request_json)).then(data => {
            console.log(data)
            if (data['status']) {
                this.setState({
                    ...this.state,
                    'giftCards': data['gift_cards'],
                    'loaded': true
                })
            }
        })
    }

    pushNewId(uuid) {
        this.props.history.push('/cards/' + uuid)
    }




    render() {
        const render_after_load = (
            <div>
                <GiftCardList pushNewId={this.pushNewId} data={this.state.giftCards} update={this.update_table} page={this.state.page} />
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
                        Gift Cards
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>

                        <Link to='/cards/create' style={{ textDecoration: 'none' }}>
                            <Button style={{ margin: '5px 10px' }} variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Create New Gift Card
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

export default connect(mapStateToProps)(GiftCards)
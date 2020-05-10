import React, { Component } from 'react'
import { getPlaces } from '../../api/inventory/placeApi';
import { connect } from 'react-redux';
import PlaceList from './placeList';
import { Link } from 'react-router-dom';


import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import RefreshIcon from '@material-ui/icons/Refresh';
import LoadingIcon from '../loading';

class Placements extends Component {
    constructor(props) {
        super(props)
        this.state = {
            'places': [],
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

    pushNewId(id) {
        this.props.history.push('/places/' + id)
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
        this.getPlacesData(request_json)
    }

    async getPlacesData(request_json) {
        await getPlaces(JSON.stringify(request_json)).then(data => {
            console.log(data)
            if (data['status']) {
                this.setState({
                    'places': data['places'],
                    'loaded': true
                })
            }
        })
    }



    render() {
        const render_after_load = (
            <div>
                <PlaceList pushNewId={this.pushNewId} data={this.state.places} update={this.update_table} page={this.state.page} />
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
                        Item Managements
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>
                        <Link to='/places/create' style={{ textDecoration: 'none' }}>
                            <Button style={{ margin: '5px 10px' }} variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Add New Place
                            </Button>
                        </Link>
                    </div>
                    <Grid item xs={12}>
                        <Paper>
                            {this.state.loaded ? render_after_load : <LoadingIcon></LoadingIcon>}
                        </Paper>
                    </Grid>

                </Grid>
            </div>)
    }
}




const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Placements)
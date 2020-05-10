import React, { Component } from 'react'
import { getUsers } from '../../api/user'
import { connect } from 'react-redux';
import UserList from './userList';
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
import Swal from 'sweetalert2';


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

class Users extends Component {

    constructor(props) {
        super(props)
        this.state = {
            'users': [],
            'loaded': false,
            'start': 0,
            'end': 10,
            'page': 1
        }
        this.update_table = this.update_table.bind(this)
        this.pushNewId = this.pushNewId.bind(this)
    }


    pushNewId(id) {
        this.props.history.push('/users/' + id)
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false) {
            this.props.history.push('/')
        }
        if (this.props.user.data.user_type !== "MANAGER") {
            console.log("not manager")
            Swal.fire({
                icon: 'error',
                title: 'Permission Denied!',
                text: 'You donont have authorization. Contact Manager or Admin'
            })
            this.props.history.push('/')
            return
        }
        this.update_table(0)

    }

    async getUsersData(request_json) {
        await getUsers(JSON.stringify(request_json)).then(data => {
            if (data['status']) {
                this.setState({
                    'users': data['users'],
                    'loaded': true
                })
            }
        })
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
        this.getUsersData(request_json)
    }


    render() {
        const render_after_load = (
            <div>
                <UserList pushNewId={this.pushNewId} data={this.state.users} update={this.update_table} page={this.state.page} />
            </div>
        )
        const { classes } = this.props;


        return (
            <div className={classes.root}>
                <Grid container
                    spacing={2}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <h2 style={{ marginTop: 0 }}>
                        Vendors
                    </h2>
                    <div>
                        <Button style={{ margin: '5px 10px' }} variant="contained" color="primary" onClick={() => { this.update_table(0) }}>
                            <RefreshIcon />&nbsp;&nbsp;&nbsp;Refresh Table
                        </Button>
                        <Link to='/users/create' style={{ textDecoration: 'none' }}>
                            <Button style={{ margin: '5px 10px' }} variant="contained" color="secondary">
                                <AddCircleIcon />&nbsp;&nbsp;&nbsp;Add New Staff
                            </Button>
                        </Link>
                    </div>

                    <Grid item xs={12}>
                        <Paper className={classes.paper}>
                            {this.state.loaded ? render_after_load : <LoadingIcon></LoadingIcon>}
                        </Paper>
                    </Grid>

                </Grid>
            </div>
        )
    }
}


Users.propTypes = {
    classes: PropTypes.object.isRequired,
};


const mapStateToProps = state => ({
    user: state.user,
})

export default withStyles(styles)(connect(mapStateToProps)(Users))

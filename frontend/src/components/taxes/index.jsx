import React, { Component } from 'react'
import {getTaxes} from '../../api/misc';
import {  connect } from 'react-redux';
import  TaxList  from './taxList';
import { Link} from 'react-router-dom';


import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import RefreshIcon from '@material-ui/icons/Refresh';
import LoadingIcon from '../loading';


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


class Taxes extends Component {
    constructor(props){
        super(props)
        this.state = {
            'taxes':[],
            'loaded':false,
            'start':0,
            'end':10,
            'page':1
        }
        this.update_table = this.update_table.bind(this)
        this.pushNewId = this.pushNewId.bind(this)
    }

    
    pushNewId(id){
        this.props.history.push('/taxes/'+id)
    }


    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
        this.update_table(0)
    }

    async update_table (by) {
        var x = by<0?-1:1
        if (by===0){
            await this.setState({
                'loaded':false,
                start: 0,
                end: 10,
                page:1
            })
        }
        else{
            if (this.state.start+by>-1){
                await this.setState({
                    'loaded':false,
                    start: this.state.start+by,
                    end: this.state.end+by,
                    page:this.state.page+x
                })
            }
            else{
                alert("Cannot move futher from here.")
                return
            }
        }
        var  request_json = {
            'action':'get',
            'filter':'none',
            'start':this.state.start,
            'end':this.state.end
        }
        this.getTaxesData(request_json)
    }
    
    async getTaxesData (request_json) {
        await getTaxes(JSON.stringify(request_json)).then(data => {
            console.log(data)
            if (data['status']){
                this.setState({
                    'taxes':data['taxes'],
                    'loaded':true
                })
            }  
        })
    }

 

render() {
    const { classes } = this.props;

    const render_after_load = (
        <div>
            <TaxList data={this.state.taxes} update={this.update_table} page={this.state.page} pushNewId={this.pushNewId}/>
        </div>
    )

    return(
        <div className={classes.root}>
        <Grid container spacing={3} justify="center" alignItems="center">
            <Grid item xs={3} >
            <Button variant="contained" color="primary" onClick={() => {this.update_table(0)}}>
              <RefreshIcon/>&nbsp;&nbsp;&nbsp;Refresh Table
              </Button>
            </Grid>
            <Grid item xs={5}>
  
            </Grid>
              <Grid item xs={3}>
              <Link to='/taxes/create' style={{ textDecoration: 'none' }}>
              <Button variant="contained" color="secondary">
              <AddCircleIcon/>&nbsp;&nbsp;&nbsp;Add New Tax
              </Button>
              </Link>
              </Grid>
  
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



Taxes.propTypes = {
    classes: PropTypes.object.isRequired,
  };


const mapStateToProps = state => ({
    user: state.user,
})

export default withStyles(styles)(connect(mapStateToProps)(Taxes))
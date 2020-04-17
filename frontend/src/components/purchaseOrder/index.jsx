import React, { Component } from 'react'
import {getPurchaseOrders} from '../../api/inventory/purchaseOrder';
import {  connect } from 'react-redux';
import  PurchaseOrderList  from './purchaseOrderList';
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

import Swal from 'sweetalert2'



class PurchaseOrders extends Component {
    constructor(props){
        super(props)
        this.state = {
            'purchaseOrders':[],
            'loaded':false,
            'start':0,
            'end':10,
            'page':1
        }
        this.update_table = this.update_table.bind(this)
        this.pushNewId = this.pushNewId.bind(this)
    }

    
    pushNewId(id){
        this.props.history.push('/purchaseorders/'+id)
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
        this.getPurchaseOrdersData(request_json)
    }
    
    async getPurchaseOrdersData (request_json) {
        await getPurchaseOrders(JSON.stringify(request_json)).then(data => {
            if (data['status']){
                this.setState({
                    'purchaseOrders':data['p_orders'],
                    'loaded':true
                })
            } 
            else{
                Swal.fire(data['error'])
            } 
        })
    }

 

render() {
    const render_after_load = (
        <div>
            <PurchaseOrderList pushNewId={this.pushNewId} data={this.state.purchaseOrders} update={this.update_table} page={this.state.page} />
        </div>
    )

    return(
        <div>
        <Grid container spacing={3} justify="center" alignItems="center">
            <Grid item xs={3} >
            <Button variant="contained" color="primary" onClick={() => {this.update_table(0)}}>
              <RefreshIcon/>&nbsp;&nbsp;&nbsp;Refresh Table
              </Button>
            </Grid>
            <Grid item xs={5}>
  
            </Grid>
              <Grid item xs={3}>
              <Link to='/purchaseorders/create' style={{ textDecoration: 'none' }}>
              <Button variant="contained" color="secondary">
              <AddCircleIcon/>&nbsp;&nbsp;&nbsp;Add New Purchase Order
              </Button>
              </Link>
              </Grid>
  
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

export default connect(mapStateToProps)(PurchaseOrders)

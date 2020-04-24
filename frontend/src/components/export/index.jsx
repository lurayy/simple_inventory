import React, { Component } from 'react'
import {getExport, } from '../../api/misc';
import {  connect } from 'react-redux';


import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import LoadingIcon from '../loading';
import url from '../../server'



class Export extends Component {
    constructor(props){
        super(props)
        this.state = {
            loaded:true,
            fields:{},
            docs:false
        }
    }
    
    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
    }


    export(){
        var data = {
            'action':"export",
            'filter':'none',
        }
        getExport(JSON.stringify(data)).then(data => {
            if(data['status']){
                this.setState({
                    ...this.state,
                    items: data['items'],
                    docs:true
                })
            }           
        })
    }

    redirect(em){
        this.props.history.push("/export/"+em)

    }



render() {
    const index_redner = (
        <Grid container justify='center'>
            <Grid item xs={10}>
        <table cellPadding={15} cellSpacing={25} >
            <tbody>
                <tr>
                    <td>
                    <Button variant="contained" color="secondary" onClick={()=>{this.redirect('purchaseorders')}}>Export Purchase Orders</Button>

                    </td>
                    <td>
                    <Button  variant="contained" color="secondary"  onClick={()=>{this.redirect('invoices')}}>Export Invoices</Button>
                    </td>
                    <td>
                    <Button variant="contained" color="secondary" onClick={()=>{this.redirect('items')}}>Export Items</Button>
                    </td>
                 </tr>
            </tbody>
        </table>
            </Grid>
        </Grid>
        )
   
    
    const render_after_load = (
        <div>
            {index_redner}
            <Grid container>
                <Grid md={10} item>
                
                </Grid>
            </Grid>
        </div>
    )
    const { classes } = this.props;

    return(
        <div >
        <Grid container spacing={3} justify="center" alignItems="center">  
          <Grid item md={10}>
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

export default (connect(mapStateToProps)(Export))

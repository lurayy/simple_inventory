import React, { Component } from 'react'
import {getExport, selectExportFields} from '../../api/misc';
import {  connect } from 'react-redux';


import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import { withStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import LoadingIcon from '../loading';
import List from '../list'
import ReactDOM from 'react-dom';
import { PDFViewer,Document, PDFDownloadLink, Page, Text, View, StyleSheet } from '@react-pdf/renderer';
import url from '../../server'

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

    getExportFields(){
        var data = {
            'action':"get",
            'model':'item'
        }
        selectExportFields(JSON.stringify(data)).then(data => {
            if (data['status']){
                this.setState({
                    'fields':data['fields'],
                    'loaded':true
                })
            }  
        })
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




render() {
    const link = url+"apiv1/inventory/export"
    const render_after_load = (
        <div>
           <h1>Export Data</h1>
            <a href={link} >Export</a>
        </div>
    )
   

    const { classes } = this.props;

    return(
        <div className={classes.root}>
        <Grid container spacing={3} justify="center" alignItems="center">  
          <Grid item md={12}>
            <Paper className={classes.paper}>
            {this.state.loaded ? render_after_load : <LoadingIcon></LoadingIcon>}
            </Paper>
          </Grid>
        </Grid>
      </div>
    )
}
}


Export.propTypes = {
    classes: PropTypes.object.isRequired,
  };


const mapStateToProps = state => ({
    user: state.user,
})

export default withStyles(styles)(connect(mapStateToProps)(Export))

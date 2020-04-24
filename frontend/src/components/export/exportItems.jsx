import React, { Component } from 'react'
import { Grid, Button} from '@material-ui/core'
import RefreshIcon from '@material-ui/icons/Refresh';
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import {getExportFields} from '../../api/misc';
import Loading from '../loading';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

class ExportItems extends Component {

    constructor(props){
        super(props)
        this.state={
            'fields':[],
            'loading':true,
            'update':[],
        }
        this.handleChange = this.handleChange.bind(this)
    }

    async componentDidMount(){
        var data = {
            'action':"get",
            'model':'item'
        }
        await getExportFields(JSON.stringify(data)).then(data =>  {
            if (data['status']){
                var temp = {}
                var x;
                var show_fields = [];
                var old;
                data['fields'].map(field => {
                    old=field
                    temp[field]=false
                    x = field.split('_')
                    field = ''
                    x.map(
                        y => {
                            field = field + y.charAt(0).toUpperCase() + y.slice(1)+ ' '
                        }
                    )
                    show_fields.push({'key':old, "str":field})
                })
                temp['name'] = true
                console.log(show_fields)
                this.setState({
                    'fields':show_fields,
                    'update':temp,
                    'loading':false
                })
            }  
        })
        console.log(this.state)
    }

    handleChange(e){
        if (e.target.name === 'name'){

        }
        else{
            this.setState({
                ...this.state,
                update : {
                    ...this.state.update,
                    [e.target.name]: !(this.state.update[e.target.name])
                }
            })
        }
    }

    exportData(){
        console.log(this.state)
        var request_json = {
            'model':'item',
            'action':'export',
            'filter':{'fields':this.state.update}
        }
        getExportFields(JSON.stringify(request_json)).then(data=>{
           console.log(data)
            if(data['status']){
                console.log('Headers')
            }
        })
    }

    back(){
        this.props.history.push('/export')
    }

      

    render() {
        const main_render = 
        <div>
        <Grid container spacing={3} justify="center" alignItems="center">
                            <Grid item xs={3} >
                            <Button  variant="contained" size='small' color="primary" onClick={()=> {this.back()}}>
                                <ArrowLeftIcon></ArrowLeftIcon>
                                Back
                            </Button>
                            </Grid>
                            <Grid item xs={5}>

                            </Grid>
                            <Grid item xs={3}>
                            <Button variant="contained" color="secondary">
                            <RefreshIcon/>&nbsp;&nbsp;&nbsp;Refresh Filters
                            </Button>
                            </Grid>
                        </Grid>
                        <Grid container justify='center'>
                            <Grid item md={4}>
                                <table cellSpacing={5} cellPadding={5} >
                                    <tbody>
                                        <tr>
                                            <td>
                                            <h3><b>Select Data To Include On Export</b></h3>
                                            </td>
                                        </tr>
                                            {this.state.fields.map(
                                                field =>(
                                                    <tr key={field['key']}>
                                                    <td key={field['key']}> 
                                                    <FormControlLabel
                                                      control={<Switch checked={this.state.update[field['key']]} onChange={this.handleChange} name={field['key']} />}
                                                      label={field['str']}
                                                    />
                                                    </td>
                                                    </tr>
                                                )
                                            )}
                                        <tr>
                                            <td>
                                            <Button variant="contained" color="secondary" onClick={()=> {this.exportData()}}>Export Data</Button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </Grid>
                            <Grid item md={4}>
                                <table cellSpacing={5} cellPadding={5}>
                                    <tbody>
                                    <tr>
                                        <td>
                                        <h3><b>Additional Filters</b></h3>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </Grid>
                        </Grid>
                        
                        </div>
        return (
            <div>
            {this.state.loading? <Loading></Loading> : main_render}
        </div>
        )
    }
}

export default ExportItems
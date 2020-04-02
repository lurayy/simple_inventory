import React, { Component } from 'react'
import {getTaxes} from '../../api/misc';
import {  connect } from 'react-redux';
import  TaxList  from './taxList';
import { Link} from 'react-router-dom';

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
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn === false ){
            this.props.history.push('/')
        }
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
    const render_after_load = (
        <div>
            <TaxList data={this.state.taxes} update={this.update_table} page={this.state.page} />
        </div>
    )

    return(
        <div>
            <Link to='/taxes/create'>Add New Tax</Link><br></br>
            <button onClick={() => {this.update_table(0)}}>Refresh table</button><br></br>
            {this.state.loaded ? render_after_load : "Loading..."}

        </div>
    )
}
}




const mapStateToProps = state => ({
    user: state.user,
})

export default connect(mapStateToProps)(Taxes)
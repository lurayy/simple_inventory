import React, { Component } from 'react'
import { isLoggedIn, permission} from '../common'


class CreateUser extends Component {

    componentDidMount() {
        console.log(isLoggedIn)
        console.log(permission)
    }

    render() {
        return (
            <div>
                <h1>Create New User</h1>
            </div>
        )
    }
}

export default CreateUser
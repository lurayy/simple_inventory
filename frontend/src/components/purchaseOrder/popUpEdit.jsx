import React from 'react'
import Popup from "reactjs-popup";


const popUpEdit =  (props) => {
    console.log(props)
    return (
        <div>
            <Popup trigger={props.popUp} >
            <h1>Popup</h1>
            </Popup>
        </div>
    )
}

export default popUpEdit;
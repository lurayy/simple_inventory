import React, { Component } from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import List from '../list';
import Popup from "reactjs-popup";
import style from '../purchaseOrder/css/popUp.module.css';
import classes from './css/invoice.module.css';

import { Grid } from '@material-ui/core';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import "react-datepicker/dist/react-datepicker.css";
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';
import IconButton from '@material-ui/core/IconButton';
import { makeStyles } from '@material-ui/core/styles';
import { Button, TextField } from '@material-ui/core';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';

import { getCustomers } from '../../api/sales/customer';
import { getPurchaseItem } from '../../api/inventory/purchaseItem'
import { updateInvoice, getInvoice, deleteInvoices, getInvoiceStatus } from '../../api/sales/invoice';
import { updateInvoiceItem, deleteInvoiceItems, createInvoiceItem } from '../../api/sales/invoiceItem'
import { getItems } from '../../api/inventory/itemApi';
import { getPlaces } from '../../api/inventory/placeApi';
import { getDiscounts, getTaxes } from '../../api/misc'
import { getPaymentMethods, validateGiftCard, doPayment } from '../../api/payment/payment';

import Table from 'react-bootstrap/Table'
import Swal from 'sweetalert2'
import QrScanner from '../../qrScanner'


const useStyles = makeStyles({
    paymentFormField: {
        margin: '10px',
    }

})

const PaymentPopup = (props) => {
    const classes = useStyles();
    const { invoice } = props.invoiceData;


    const [payment_data, set_payment_data] = React.useState({
        invoice_id: '',
        amount: '',
        transaction_from: '',
        transaction_id: '',
        payment_method_id: '',
    });
    const [applyCard, setApplyCard] = React.useState(false)
    const [giftCode, setGiftCode] = React.useState('')
    const [isGiftCodeVerified, setIsGiftCodeVerified] = React.useState(false)

    const _verify = async (e) => {
        console.log(giftCode)
        var request_json = {
            'action': 'get',
            'code': giftCode
        }

        await validateGiftCard(JSON.stringify(request_json)).then(data => {
            setIsGiftCodeVerified(true)

            console.log(data)
            if (data['status']) {
                Swal.fire('Great!', data.msg, 'success')
                setIsGiftCodeVerified(data.status)
            } else {
                Swal.fire('Ooops!', data.msg, 'error')
            }
        })
    }

    const _giftCodeChange = (e) => {
        setGiftCode(e.target.value)
    }


    const _txFromChange = (e) => {
        set_payment_data({ ...payment_data, transaction_from: e.target.value })
    }
    const _txIDChange = (e) => {
        set_payment_data({ ...payment_data, transaction_id: e.target.value })
    }
    const _txAmountChange = (e) => {
        set_payment_data({ ...payment_data, amount: e.target.value })
    }

    const _savePayment = async (e) => {



        var request_json = {
            'action': 'add',
            'payment_method': payment_data.payment_method_id,
            'invoice_id': invoice.id,
            'amount': payment_data.amount,
            'transaction_from': payment_data.amount,
            'transaction_id': payment_data.transaction_id
        }

        console.log(request_json)

        // doPayment(JSON.stringify(request_json)).then(data => {
        //     console.log('Data is', data)
        //     if (data.status) {

        //         Swal.fire('Gift card is valid', 'Great!', 'success')
        //     }
        // })

    }

    console.log(invoice)

    return (
        <Popup
            open={props.show}
            closeOnDocumentClick
            onClose={props.onClose}

        >
            <div style={{ padding: 20, display: 'flex', flexDirection: 'column' }}>
                <h3>Proceed</h3>
                <br />
                <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-around' }}>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <div>Discount Total</div>
                        <div><b>Rs. {invoice.discount_total}</b></div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <div>Tax Total</div>
                        <div><b>Rs. {invoice.tax_total}</b></div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <div>Total</div>
                        <div><b>Rs. {invoice.total_amount}</b></div>
                    </div>
                </div>
                <br />

                <form noValidate autoComplete="off" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '5px 30px', display: 'flex', flexDirection: 'row' }}>
                        <div style={{ width: '80%' }}>Select Payment Method :</div>
                        <Select
                            fullWidth
                            value={payment_data.payment_method_id}
                            onChange={(e) => {
                                e.preventDefault()
                                console.log('clicked')
                                console.log(e.target.value)
                                set_payment_data({
                                    ...payment_data,
                                    payment_method_id: e.target.value,
                                })

                                // setApplyCard(props.payment_methods.find(item => item.id === e.target.value).is_gift_card)
                                setApplyCard(true)

                            }}
                        >
                            {
                                props.payment_methods.map((item, index) => {
                                    return <MenuItem key={index} value={item.id}>{item.name}</MenuItem>
                                })
                            }
                        </Select>
                    </div>






                    <div style={{ display: 'flex', flexDirection: 'row' }}>
                        <TextField
                            className={classes.paymentFormField}
                            required
                            label="Transaction From"
                            size='small'
                            variant="outlined"
                            onChange={_txFromChange}
                        />

                        <TextField
                            className={classes.paymentFormField}
                            required
                            label='Transaction ID'
                            size='small'
                            variant="outlined"
                            onChange={_txIDChange}
                        />
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'row' }}>
                        <TextField
                            fullWidth
                            className={classes.paymentFormField}
                            label="Amount"
                            variant="outlined"
                            onChange={_txAmountChange}
                            size='small'
                        />
                    </div>

                    {applyCard ? (
                        <>
                            <div style={{ display: 'flex', padding: '10px' }}>
                                <div style={{ width: '35%', verticalAlign: 'center', lineHeight: '59px' }}>Apply Gift Card :</div>
                                <TextField
                                    className={classes.paymentFormField}
                                    label="Input Code"
                                    size='small'
                                    variant="outlined"
                                    onChange={_giftCodeChange}
                                />
                                <Button
                                    variant="contained"
                                    color="primary"
                                    style={{ margin: '10px 0' }}
                                    onClick={_verify}
                                >{isGiftCodeVerified ? 'Verified' : 'Verify'}</Button>
                            </div>
                        </>) : null
                    }


                </form>
                <div>
                    <Button
                        style={{ float: 'right', margin: '10px 20px 0 0', display: 'inline-block' }}
                        variant="contained"
                        color="secondary"
                        onClick={_savePayment}
                    >Save Payment</Button>
                </div>

            </div>
        </Popup>
    )
}
export default PaymentPopup;
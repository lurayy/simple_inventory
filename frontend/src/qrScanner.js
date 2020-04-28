import React from 'react';
import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import QrReader from 'react-qr-reader'


function SimpleDialog(props) {
  const { onClose, open, onOpen } = props;

  const handleClose = () => {
    console.log('close')
    onClose();
  };

  const handleError = value =>{
    console.log(value)
  };
  const sleep = (milliseconds) =>{
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }

  const handleOpen = () => { 
    onOpen();
  }
  
  const handleScan = value => {
    if (value){
      if (props.onFind(value)){
        handleClose()
      }
    }
    else{
      handleClose()
      sleep(3000)
      handleOpen()
    }
  }

  return (
    <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open} fullWidth maxWidth={'sm'}>
      <DialogTitle id="simple-dialog-title">Place the QR inside the Box</DialogTitle>
          <QrReader
          delay={300}
          onError={handleError}
          onScan={handleScan}
          style={{ width: '100%' }}
          />
    </Dialog>
  );
}


function QrScanner(props) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button variant="contained" ref={props.refoption} color="secondary" id="btnScanner" onClick={handleClickOpen}>
        Scan QR Code 
      </Button>
      <SimpleDialog open={open} onClose={handleClose} onOpen={handleClickOpen} onFind={props.onFind} />
    </div>
  );
}
export default QrScanner
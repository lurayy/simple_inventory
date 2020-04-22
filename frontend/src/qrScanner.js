import React from 'react';
import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import QrReader from 'react-qr-reader'


function SimpleDialog(props) {
  const { onClose, open } = props;

  const handleClose = () => {
    onClose();
  };

  const handleError = value =>{
    console.log(value)
  };

  const handleScan = value => {
    if (value){
      props.onFind(value)
      handleClose()
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
      <br />
      <Button variant="contained" color="secondary" onClick={handleClickOpen}>
        Scan Item's QR Code 
      </Button>
      <SimpleDialog open={open} onClose={handleClose} onFind={props.onFind} />
      <br></br>
    </div>
  );
}
export default QrScanner
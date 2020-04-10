import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid'
import IconButton from '@material-ui/core/IconButton';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const List = (props) => {
  var page = true;
  if (!props.page){
    page=props.page
  }
  const classes = useStyles();
  const headers = props.header
  const rows = props.data
  var temp;
  var no_data=false
  var back=true
  if (rows.length === 0){
    no_data=true
  } 
  if (props.page === 1){
    back = false
  }


  const pagination = <div>
    {back? <IconButton color="secondary" onClick={() => {props.update(-10)}} aria-label="pervious-button">
      <NavigateBeforeIcon />
    </IconButton> : <IconButton color="secondary" onClick={() => {props.update(-10)}} aria-label="pervious-button" disabled>
      <NavigateBeforeIcon />
    </IconButton>}
    <b>
    Page: {props.page}</b>
    {no_data? <IconButton color="secondary" onClick={() => {props.update(10)}} aria-label="pervious-button" disabled>
      <NavigateNextIcon />
    </IconButton> : <IconButton color="secondary" onClick={() => {props.update(10)}} aria-label="pervious-button">
      <NavigateNextIcon />
    </IconButton>}
  </div>

  return (
      <div>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
                {headers.map(
                    header =>(
                    <TableCell key={header.id}><b>{header.name}</b></TableCell>
                    )
                )}
            </TableRow>
          </TableHead>
          <TableBody>
          {rows.map(
              row =>(
                  <TableRow key={row.id} onClick={() => {props.popUp(row.id, row.uuid)}}>
                      {headers.map(
                          header =>
                              (
                                  temp = header.prop,
                              <TableCell key={header.id}>{row[temp]}</TableCell>
                              )
                      )}
                  </TableRow>
              )
          )}
          </TableBody>
        </Table>
      </TableContainer>

      <Grid container justify="center" alignItems="center">
    <Grid item xs={"auto"}>
    {no_data ? <h2>No Data Available</h2> : <span></span>}
    </Grid>
    </Grid>
    <br></br>
    <Grid container justify="center" alignItems="center">
    <Grid item xs={"auto"}>
    {page ? pagination : <span></span>}
    </Grid>    
    </Grid>
    <br></br>
    </div>
  );
}

export default List
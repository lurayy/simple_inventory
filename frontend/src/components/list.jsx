import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Pagination from '@material-ui/lab/Pagination';
import Grid from '@material-ui/core/Grid'

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

  // const pagination = <div>
  //   <h4>Page: {props.page}</h4>
  //   <button onClick={() => {props.update(-10)}}>Pervious</button><button onClick={() => {props.update(10)}}>Next</button>
  // </div>
const pagination =       <Pagination count={10} variant="outlined" color="secondary" />

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
    <br></br>
    <Grid container justify="center" alignItems="center">
    <Grid item xs={6}>
    {page ? pagination : <span></span>}
    </Grid>
    </Grid>
    <br></br>
    </div>
  );
}

export default List
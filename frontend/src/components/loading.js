import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    backgroundColor: "black",
        
    // position: 'fixed',
    left: theme.spacing(2),
    bottom: theme.spacing(2),
    right: theme.spacing(2),
    },
}));

export default function LoadingIcon() {
  const [progress, setProgress] = React.useState(0);

  React.useEffect(() => {
    function tick() {
      // reset when reaching 100%
      setProgress(oldProgress => (oldProgress >= 100 ? 0 : oldProgress + 1));
    }

    const timer = setInterval(tick, 20);
    return () => {
      clearInterval(timer);
    };
  }, []);

  return (
    <Grid
    container
    spacing={0}
    direction="column"
    alignItems="center"
    justify="center"
    style={{ minHeight: '100vh' }}
  >
  
    <Grid item xs={3}>
    <CircularProgress variant="determinate" value={progress} />

    </Grid>   
  
  </Grid> 
        
  );
}
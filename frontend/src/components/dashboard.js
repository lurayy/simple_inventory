import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import Login from './users/login';
import Logout from './users/logout';
import VendorCreation from './vendors/vendorCreation';
import UserCreation from './users/userCreation';
import { BrowserRouter as Router, Switch , Route} from 'react-router-dom';
import Users from './users';
import Vendors from './vendors/index';
import Customers from './customer/index';
import CustomerCreation from './customer/customerCreation'
import PurchaseOrders from './purchaseOrder/index'
import PurchaseOrderCreation from './purchaseOrder/purchaseOrderCreation'
import Invoices from './invoices/index';
import InvoiceCreation from './invoices/invoiceCreation';
import Discounts from './discounts/index';
import DiscountCreation from './discounts/discountCreation'
import Taxes from './taxes/index';
import TaxCreation from './taxes/taxCreation'
import Items from './items/index'
import ItemCreation from './items/itemCreation'
import ItemCatagories from './itemCatagories/index';
import ItemCatagoryCreation from './itemCatagories/itemCreation';
import Places from './placement/index'
import PlaceCreation from './placement/placeCreation'

import { useSelector } from "react-redux";

import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';

import DashboardIcon from '@material-ui/icons/Dashboard';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import PeopleIcon from '@material-ui/icons/People';
import DescriptionIcon from '@material-ui/icons/Description';
import MonetizationOnIcon from '@material-ui/icons/MonetizationOn';
import FeaturedPlayListIcon from '@material-ui/icons/FeaturedPlayList';
import SettingsIcon from '@material-ui/icons/Settings';

import CustomerList from './customer/customerList'
import DiscountList from './discounts/discountList'
import InvoiceListing from './invoices/invoiceListing'
import ItemCatagoryList from './itemCatagories/itemCatagoryList'
import ItemList from './items/itemList'
import PlaceList from './placement/placeList'
import PurchaseOrderList  from './purchaseOrder/purchaseOrderList'
import TaxList from './taxes/taxList'
import UserList from './users/userList'
import VendorList from './vendors/vendorList'
import Export from './export/index'
import GetAppIcon from '@material-ui/icons/GetApp';
const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24,
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    textAlign: 'center',
    flexDirection: 'column',
  },
  fixedHeight: {
    height: 240,
  },
}));

function Dashboard() {
  
  const classes = useStyles();
  const [open, setOpen] = React.useState(true);
  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);

  };

  const user = useSelector(state => state.user);
  var isDashboard = false
  if( (window.location.pathname) ==='/'){
    isDashboard = true
  }

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="absolute" className={clsx(classes.appBar, open && classes.appBarShift)}>
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            className={clsx(classes.menuButton, open && classes.menuButtonHidden)}
          >
            <MenuIcon />
          </IconButton>
          <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            Mandala IMS
          </Typography>
          <IconButton color="inherit"  onClick={()=> {window.location.href="/logout"}}>
          <ExitToAppIcon/>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}
      >
        <div className={classes.toolbarIcon}>
          <Typography>
            {user.data.first_name} <span>  </span> {user.data.last_name}<br></br>
            {user.data.user_type}
          </Typography>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Router>
        <Divider />
        <List>
    <ListItem button onClick={()=> {window.location.href="/"}}>
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
    <ListItem button  onClick={()=> {window.location.href="/purchaseorders"}}>
      <ListItemIcon>
        <ShoppingCartIcon />
      </ListItemIcon>
      <ListItemText primary="Purchase Orders" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/vendors"}}>
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary="Vendors" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/invoices"}}>
      <ListItemIcon>
        <DescriptionIcon />
      </ListItemIcon>
      <ListItemText primary="Invoices" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/customers"}}>
      <ListItemIcon>
        <MonetizationOnIcon />
      </ListItemIcon>
      <ListItemText primary="Customers" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/items"}}>
      <ListItemIcon>
      <FeaturedPlayListIcon />
      </ListItemIcon>
      <ListItemText primary="Items" />
    </ListItem>
        </List>
        <Divider />
        <List>
    <ListItem button onClick={()=> {window.location.href="/places"}}>
      <ListItemIcon>
      <SettingsIcon />
      </ListItemIcon>
      <ListItemText primary="Item Managements" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/discounts"}}>
      <ListItemIcon>
      <SettingsIcon />
      </ListItemIcon>
      <ListItemText primary="Discounts" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/taxes"}}>
      <ListItemIcon>
      <SettingsIcon />
      </ListItemIcon>
      <ListItemText primary="Taxes" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/itemcatagories"}}>
      <ListItemIcon>
      <SettingsIcon />
      </ListItemIcon>
      <ListItemText primary="Item Catagories" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/users"}}>
      <ListItemIcon>
      <SettingsIcon />
      </ListItemIcon>
      <ListItemText primary="Staff Management" />
    </ListItem>
    <ListItem button onClick={()=> {window.location.href="/export"}}>
      <ListItemIcon>
      <GetAppIcon />
      </ListItemIcon>
      <ListItemText primary="Export Data" />
    </ListItem>
        </List>
        </Router>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container className={classes.container}>
          <Grid container justify="center">
            <Grid item xs={12} >
              {/* {isDashboard ? <Hello></Hello>: <span></span>} */}
            <Router>
            <Switch>
                    <Route path='/login' component={Login}></Route>
                    <Route path='/logout' component={Logout}></Route>
                    <Route path='/users/create' component = {UserCreation}></Route>
                    <Route path='/users/:id' component = {UserList}></Route>
                    <Route path='/users' component = {Users}></Route>

                    <Route path='/vendors/create' component = {VendorCreation}></Route>
                    <Route path='/vendors/:id' component = {VendorList}></Route>
                    <Route path='/vendors' component = {Vendors}></Route>
                    
                    <Route path='/customers/create' component = {CustomerCreation}></Route>
                    <Route path='/customers/:id' component = {CustomerList}></Route>
                    <Route path='/customers' component = {Customers}></Route>

                    <Route path='/purchaseorders/create' component = {PurchaseOrderCreation}></Route>
                    <Route path='/purchaseorders/:id' component = {PurchaseOrderList}></Route>
                    <Route path='/purchaseorders' component = {PurchaseOrders}></Route>
                    
                    <Route path='/invoices/create' component = {InvoiceCreation}></Route>
                    <Route path='/invoices/:id' component = {InvoiceListing}></Route>
                    <Route path='/invoices' component = {Invoices}></Route>

                    <Route path='/discounts/create' component= {DiscountCreation}></Route>
                    <Route path='/discounts/:id' component= {DiscountList}></Route>
                    <Route path='/discounts' component= {Discounts}></Route>
                    
                    <Route path='/taxes/create' component= {TaxCreation}></Route>
                    <Route path='/taxes/:id' component= {TaxList}></Route>
                    <Route path='/taxes' component= {Taxes}></Route>
                    
                    <Route path='/items/create' component= {ItemCreation}></Route>
                    <Route path='/items/:id' component= {ItemList}></Route>
                    <Route path='/items' component= {Items}></Route>

                    <Route path='/itemcatagories/create' component= {ItemCatagoryCreation}></Route>
                    <Route path='/itemcatagories/:id' component= {ItemCatagoryList}></Route>
                    <Route path='/itemcatagories' component= {ItemCatagories}></Route>

                    <Route path='/places/create' component= {PlaceCreation}></Route>
                    <Route path='/places/:id' component= {PlaceList}></Route>
                    <Route path='/places' component= {Places}></Route>

                    <Route path='/export' component= {Export}></Route>
                    </Switch>
            </Router>
            </Grid>            
          </Grid>
        </Container>
      </main>
    </div>
  );
}

export default Dashboard
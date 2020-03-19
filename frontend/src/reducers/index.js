import { combineReducers } from 'redux';
import userReducer from './userReducer';
import usersReducer from './usersReducer';

const rootReducers = combineReducers ({
    user: userReducer,
    users : usersReducer
})

export default rootReducers
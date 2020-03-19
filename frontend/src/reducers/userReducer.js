var initState = {
    'isLoggedIn':false,
    'data':{}
}
const userReducer = (state=initState, action) => {
    switch(action.type){
        case 'logout':
            state.data = {}
            state.isLoggedIn = false;
            return{
                isLoggedIn: state.isLoggedIn
            }
        case 'loggedIn':
            state.data = action.payload
            state.isLoggedIn = true;
            return {
                data: state.data,
                isLoggedIn: state.isLoggedIn
            }
        default:
            return state;
    }
};

export default userReducer
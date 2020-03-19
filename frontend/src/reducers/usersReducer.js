var initState = {
    'data':{}
}
const usersReducer = (state=initState, action) => {
    switch(action.type){
        case 'setUsers':
            state.users = action.payload
            return{
                users: state.users
            }
        default:
            return state;
    }

};

export default usersReducer
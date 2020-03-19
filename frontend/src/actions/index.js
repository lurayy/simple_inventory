export const logout = () => {
    return {
        type: 'logout'
    };
}

export const loggedIn = (data) => {
    return {
        type: 'loggedIn',
        payload: data
    };
}

import {useSelector} from 'react-redux'

const isLoggedIn = () => {
    const temp = useSelector(state=> state.user.isLoggedIn)
    console.log(temp)
    return temp
}

const permission = () => {
    const userType = useSelector(state => state.user.data.user_type)
    if (userType === "MANAGER"){
        return true
    }
    else {
        return false
    }
}
export {isLoggedIn, permission}
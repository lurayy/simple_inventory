import { baseRequest } from './base';

const loginUser = async data => {
    try {
      return await baseRequest("apiv1/users/login", "POST", data);
    } catch (e) {
      alert(e);
    }
  };

const csrfToken = async () => {
    try {
        return await baseRequest("apiv1/users/verify", "GET");
      } catch (e) {
        alert(e);
      }
    };

const logoutUser = async data => {
  try {
    return await baseRequest('apiv1/users/logout', "GET");
  } catch(e){
    alert(e);
  }
};

const createUser = async data => {
  try {
    return await baseRequest('apiv1/users/create','POST', data);
  } catch(e){
    alert(e)
  }
};

const getUsers = async data => {
  try {
    return await baseRequest('apiv1/users/get','POST', data);
  } catch(e){
    alert(e)
  }
};


const getUser = async data => {
  try {
    return await baseRequest('apiv1/users/get/0','POST', data);
  } catch(e){
    alert(e)
  }
};

const updateUser = async data => {
  try{
    return await baseRequest('apiv1/users/get/0', 'POST', data);
  } catch (e){
    alert(e)
  }
};


const getCurrentUser = async data => {
  try{
    return await baseRequest('apiv1/users/current', 'POST', data);
  } catch (e){
    alert(e)
  }
};

export { loginUser, csrfToken, logoutUser, getUsers, createUser, getUser, updateUser, getCurrentUser }
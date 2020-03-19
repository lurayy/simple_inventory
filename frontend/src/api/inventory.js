import { baseRequest } from './base';

const getVendors = async data => {
  try {
    return await baseRequest('apiv1/inventory/vendors/get','POST', data);
  } catch(e){
    alert(e)
  }
};

const deleteVendors = async data => {
  try {
    return await baseRequest('apiv1/inventory/vendors/delete','POST', data);
  } catch(e){
    alert(e)
  }
};

const updateVendor = async data => {
  try {
    return await baseRequest('apiv1/inventory/vendors/0','POST', data);
  } catch(e){
    alert(e)
  }
};

const createVendor = async data => {
    try {
      return await baseRequest('apiv1/inventory/vendor/create','POST', data);
    } catch(e){
      alert(e)
    }
};

export { getVendors, createVendor, deleteVendors, updateVendor}
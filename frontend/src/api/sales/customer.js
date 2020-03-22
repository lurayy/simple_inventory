import { baseRequest } from '../base';
// api for Invoices 

const getCustomers = async data => {
    try {
      return await baseRequest('apiv1/inventory/customers','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteCustomers = async data => {
    try {
      return await baseRequest('apiv1/inventory/customers/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createCustomer = async data => {
      try {
        return await baseRequest('apiv1/inventory/customers','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getCustomer = async data => {
    try {
      return await baseRequest('apiv1/inventory/customer','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateCustomer= async data => {
    try {
      return await baseRequest('apiv1/inventorycustomer','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getCustomers, createCustomer, deleteCustomers, updateCustomer, getCustomer}
  
import { baseRequest } from '../base';
// api for Invoices 

const getCustomers = async data => {
    try {
      return await baseRequest('apiv1/sales/customers','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteCustomers = async data => {
    try {
      return await baseRequest('apiv1/sales/customers/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createCustomer = async data => {
      try {
        return await baseRequest('apiv1/sales/customers','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getCustomer = async data => {
    try {
      return await baseRequest('apiv1/sales/customer','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateCustomer= async data => {
    try {
      return await baseRequest('apiv1/sales/customer','POST', data);
    } catch(e){
      alert(e)
    }
  };
   
  const getCustomerCategory= async data => {
    try {
      return await baseRequest('apiv1/sales/customers/category','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getCustomerCategory, getCustomers, createCustomer, deleteCustomers, updateCustomer, getCustomer}
  
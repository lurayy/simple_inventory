import { baseRequest } from '../base';
// api for Invoices 

const getInvoices = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoices','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteInvoices = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoices/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createInvoice = async data => {
      try {
        return await baseRequest('apiv1/inventory/invoices','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getInvoice = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoice','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateInvoice= async data => {
    try {
      return await baseRequest('apiv1/inventory/invoice','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getInvoices, createInvoice, deleteInvoices, updateInvoice, getInvoice}
  
import { baseRequest } from '../base';
// api for Invoices 

const getInvoices = async data => {
    try {
      return await baseRequest('apiv1/sales/invoices','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteInvoices = async data => {
    try {
      return await baseRequest('apiv1/sales/invoices/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createInvoice = async data => {
      try {
        return await baseRequest('apiv1/sales/invoices','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getInvoice = async data => {
    try {
      return await baseRequest('apiv1/sales/invoice','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateInvoice= async data => {
    try {
      return await baseRequest('apiv1/sales/invoice','POST', data);
    } catch(e){
      alert(e)
    }
  };
  const getInvoiceStatus= async data => {
    try {
      return await baseRequest('apiv1/sales/invoices/status','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getInvoiceStatus, getInvoices, createInvoice, deleteInvoices, updateInvoice, getInvoice}
  
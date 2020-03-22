import { baseRequest } from '../base';
// api for Invoices 

const getInvoiceItems = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoiceitems','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteInvoiceItems = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoiceitems/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createInvoiceItem = async data => {
      try {
        return await baseRequest('apiv1/inventory/invoiceitems','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getInvoiceItem = async data => {
    try {
      return await baseRequest('apiv1/inventory/invoiceitem','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateInvoiceItem= async data => {
    try {
      return await baseRequest('apiv1/inventory/invoiceitem','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getInvoiceItems, createInvoiceItem, deleteInvoiceItems, updateInvoiceItem, getInvoiceItem}
  
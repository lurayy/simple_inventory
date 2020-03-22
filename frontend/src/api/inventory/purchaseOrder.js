import { baseRequest } from '../base';
// api for items 

const getPurchaseOrders = async data => {
    try {
      return await baseRequest('apiv1/inventory/porders','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deletePurchaseOrder = async data => {
    try {
      return await baseRequest('apiv1/inventory/porders/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createPurchaseOrder = async data => {
      try {
        return await baseRequest('apiv1/inventory/porders','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getPurchaseOrder = async data => {
    try {
      return await baseRequest('apiv1/inventory/porder','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updatePurchaseOrder= async data => {
    try {
      return await baseRequest('apiv1/inventory/porder','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getPurchaseOrders, deletePurchaseOrder, createPurchaseOrder, getPurchaseOrder, updatePurchaseOrder}
  
import { baseRequest } from '../base';
// api for items 

const getPurchaseItems = async data => {
    try {
      return await baseRequest('apiv1/inventory/pitems','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deletePurchaseItem = async data => {
    try {
      return await baseRequest('apiv1/inventory/pitems/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createPurchaseItem = async data => {
      try {
        return await baseRequest('apiv1/inventory/pitems','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getPurchaseItem = async data => {
    try {
      return await baseRequest('apiv1/inventory/pitem','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updatePurchaseItem= async data => {
    try {
      return await baseRequest('apiv1/inventory/pitem','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getPurchaseItems, deletePurchaseItem, createPurchaseItem, getPurchaseItem, updatePurchaseItem}
  
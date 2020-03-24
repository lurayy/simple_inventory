import { baseRequest } from '../base';
// api for items 

  
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
  
  const updatePurchaseItem= async data => {
    try {
      return await baseRequest('apiv1/inventory/pitem','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export { deletePurchaseItem, createPurchaseItem, updatePurchaseItem}
  
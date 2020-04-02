import { baseRequest } from '../base';
// api for items 

const getItemCatagories = async data => {
    try {
      return await baseRequest('apiv1/inventory/items/catagories','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteItemCatagory = async data => {
    try {
      return await baseRequest('apiv1/inventory/items/catagories/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createItemCatagory = async data => {
      try {
        return await baseRequest('apiv1/inventory/items/catagories','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getItemCatagory = async data => {
    try {
      return await baseRequest('apiv1/inventory/items/catagory','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateItemCatagory= async data => {
    try {
      return await baseRequest('apiv1/inventory/items/catagory','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export { getItemCatagories, deleteItemCatagory, createItemCatagory, getItemCatagory, updateItemCatagory}
  
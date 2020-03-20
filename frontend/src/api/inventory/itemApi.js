import { baseRequest } from '../base';
// api for items 

const getItems = async data => {
    try {
      return await baseRequest('apiv1/inventory/items','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteItems = async data => {
    try {
      return await baseRequest('apiv1/inventory/items/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createItem = async data => {
      try {
        return await baseRequest('apiv1/inventory/items','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getItem = async data => {
    try {
      return await baseRequest('apiv1/inventory/item','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateItem= async data => {
    try {
      return await baseRequest('apiv1/inventory/item','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getItems, createItem, deleteItems, updateItem, getItem}
  
import { baseRequest } from '../base';
// api for items 

const getplaces = async data => {
    try {
      return await baseRequest('apiv1/inventory/places','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteplaces = async data => {
    try {
      return await baseRequest('apiv1/inventory/places/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createplace = async data => {
      try {
        return await baseRequest('apiv1/inventory/places','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getplace = async data => {
    try {
      return await baseRequest('apiv1/inventory/place','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateplace= async data => {
    try {
      return await baseRequest('apiv1/inventory/place','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
export {getplaces, createplace, deleteplaces, updateplace, getplace}
  
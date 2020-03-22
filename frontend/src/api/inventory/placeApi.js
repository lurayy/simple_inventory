import { baseRequest } from '../base';
// api for items 

const getPlaces = async data => {
    try {
      return await baseRequest('apiv1/inventory/places','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deletePlaces = async data => {
    try {
      return await baseRequest('apiv1/inventory/places/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createPlace = async data => {
      try {
        return await baseRequest('apiv1/inventory/places','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getPlace = async data => {
    try {
      return await baseRequest('apiv1/inventory/place','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updatePlace = async data => {
    try {
      return await baseRequest('apiv1/inventory/place','POST', data);
    } catch(e){
      alert(e)
    }
  };

  const assignPlace = async data => {
    try { 
      return await  baseRequest('apiv1/inventory/places/assign','POST', data);
    } catch (e){
      alert(e)
    }
  }
  
export {getPlaces, createPlace, deletePlaces, updatePlace, getPlace, assignPlace}
  
import { baseRequest } from './base';
 

const getGiftCards = async data => {
    try {
      return await baseRequest('apiv1/payment/giftcards','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const getGiftCard = async data => {
    try {
      return await baseRequest('apiv1/payment/giftcard','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createGiftCard = async data => {
      try {
        return await baseRequest('apiv1/payment/giftcards','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const editGiftCard = async data => {
    try {
      return await baseRequest('apiv1/payment/giftcard','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const deleteGiftCards = async data => {
    try {
      return await baseRequest('apiv1/payment/giftcards/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };



  
export { getGiftCard, getGiftCards, createGiftCard, editGiftCard, deleteGiftCards }
  
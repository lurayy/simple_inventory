import { baseRequest } from '../base';
 

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
  
  
  const updateGiftCard = async data => {
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

  
  const validateGiftCard = async data => {
    try {
      return await baseRequest('apiv1/payment/giftcards/validate','POST', data);
    } catch(e){
      alert(e)
    }
  };



  
export { validateGiftCard, getGiftCard, getGiftCards, createGiftCard, updateGiftCard, deleteGiftCards }
  
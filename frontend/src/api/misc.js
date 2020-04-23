import { baseRequest } from './base';
 

const getDiscounts = async data => {
    try {
      return await baseRequest('apiv1/sales/discounts','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteDiscounts = async data => {
    try {
      return await baseRequest('apiv1/sales/discounts/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createDiscount = async data => {
      try {
        return await baseRequest('apiv1/sales/discounts','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getDiscount = async data => {
    try {
      return await baseRequest('apiv1/sales/discount','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateDiscount= async data => {
    try {
      return await baseRequest('apiv1/sales/discount','POST', data);
    } catch(e){
      alert(e)
    }
  };


  
const getTaxes = async data => {
    try {
      return await baseRequest('apiv1/sales/taxes','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  
  const deleteTaxes = async data => {
    try {
      return await baseRequest('apiv1/sales/taxes/delete','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const createTax = async data => {
      try {
        return await baseRequest('apiv1/sales/taxes','POST', data);
      } catch(e){
        alert(e)
      }
  };
  
  
  const getTax = async data => {
    try {
      return await baseRequest('apiv1/sales/tax','POST', data);
    } catch(e){
      alert(e)
    }
  };
  
  const updateTax= async data => {
    try {
      return await baseRequest('apiv1/sales/tax','POST', data);
    } catch(e){
      alert(e)
    }
  };

  const getPurchaseOrderStatus= async data => {
    try {
      return await baseRequest('apiv1/inventory/status/porders','POST', data);
    } catch(e){
      alert(e)
    }
  };

  
  const getPlacements= async data => {
    try {
      return await baseRequest('apiv1/inventory/placements','POST', data);
    } catch(e){
      alert(e)
    }
  };

  const deletePlacement = async data => {
    try {
      return await baseRequest('apiv1/inventory/places/assign','POST', data);
    } catch(e){
      alert(e)
    }
  }

  
  const selectExportFields = async data => {
    try {
      return await baseRequest('apiv1/inventory/export','POST', data);
    } catch(e){
      alert(e)
    }
  }

  const getExport = async data => {
    try {
      return await baseRequest('apiv1/inventory/export','POST', data);
    } catch(e){
      alert(e)
    }
  }

  
export {getExport, selectExportFields, deletePlacement,  getPlacements, getPurchaseOrderStatus, getDiscounts, createDiscount, deleteDiscounts, updateDiscount, getDiscount, getTaxes, createTax, deleteTaxes, updateTax, getTax}
  
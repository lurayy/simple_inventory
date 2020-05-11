import { baseRequest } from '../base';


const getGiftCards = async data => {
    try {
        return await baseRequest('apiv1/payment/giftcards', 'POST', data);
    } catch (e) {
        alert(e)
    }
};


const getGiftCard = async data => {
    try {
        return await baseRequest('apiv1/payment/giftcard', 'POST', data);
    } catch (e) {
        alert(e)
    }
};

const getPaymentMethods = async data => {
    try {
        return await baseRequest('apiv1/payment/methods', 'POST', data)
    } catch (e) {
        alert(e)
    }
}

const doPayment = async (data) => {
    try {
        return await baseRequest('apiv1/payment/do', 'POST', data)
    } catch (e) {
        alert(e)
    }
}


const validateGiftCard = async data => {
    try {
        return await baseRequest('apiv1/payment/giftcard/validate', 'POST', data)
    } catch (e) {
        alert(e)
    }
}


export { getPaymentMethods, doPayment, validateGiftCard }

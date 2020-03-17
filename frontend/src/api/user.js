import { baseRequest } from './base';

const loginUser = async data => {
    try {
      return await baseRequest("/login", "POST", data);
    } catch (e) {
      alert(e);
    }
  };

const csrfToken = async () => {
    try {
        return await baseRequest("/verify", "GET");
      } catch (e) {
        alert(e);
      }
    };
    
export { loginUser, csrfToken }
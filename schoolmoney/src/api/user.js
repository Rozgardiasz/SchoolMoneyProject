import axios from 'axios';


export const setUserId = (id) => {
    localStorage.setItem('user_id', id);
  };
  
  export const getUserId = () => {
    return localStorage.getItem('user_id');
  };
  
  export const setUserName = (firstName, lastName) => {
    localStorage.setItem('user_first_name', firstName);
    localStorage.setItem('user_last_name', lastName);
  };
  
  export const getUserFirstName = () => {
    return localStorage.getItem('user_first_name');
  };
  
  export const getUserLastName = () => {
    return localStorage.getItem('user_last_name');
  };
  
  export const setUserEmail = (email) => {
    localStorage.setItem('user_email', email);
  };
  
  export const getUserEmail = () => {
    return localStorage.getItem('user_email');
  };
  
  export const clearUserData = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('user_email');
  };
  
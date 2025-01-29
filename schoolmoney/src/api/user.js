import axios from 'axios';
import { getToken } from "./auth";


export const setUserId = (id) => {
    localStorage.setItem('user_id', id);
  };
  
  export const getUserId = () => {
    return Number(localStorage.getItem('user_id'));
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

  export const setAccountNumber = (account_number) => {
    localStorage.setItem('user_account_number', account_number);
  };

  export const getAccountNumber = () => {
    return localStorage.getItem('user_account_number');
  };

  export const setAccountBalance = (balance) => {
    localStorage.setItem('user_balance', balance);
  };

  export const getAccountBalance = () => {
    return localStorage.getItem('user_balance');
  };


  export const setAccountID = (account_id) => {
    localStorage.setItem('user_account_id', account_id);
  };


  export const getAccountID = () => {
    return localStorage.getItem('user_account_id');
  };





export async function getUserById(id) {
  const token = getToken(); 
  try {
    const response = await axios.get(`http://localhost:8000/get_user/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Błąd podczas pobierania użytkownika:", error);
    throw error;
  }
}

  
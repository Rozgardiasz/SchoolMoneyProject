import axios from 'axios';

import { getUserId, getAccountID, getAccountBalance, getAccountNumber } from "@/api/user";
import {getToken} from "@/api/auth"


const API_URL = 'http://localhost:8000';


export async function createCollection(fundData) {
  try {
    const token = getToken(); // Pobieramy token

    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    const payload = {
      id: 0, // Backend generuje ID
      goal: fundData.goal,
      title: fundData.title,
      description: fundData.description,
      start_date: new Date(fundData.startDate).toISOString(),
      end_date: new Date(fundData.endDate).toISOString(),
      class_id: fundData.classId,
      creator_id: getUserId(),
      account: {
        id: getAccountID(),
        account_number: getAccountNumber(),
        balance: getAccountBalance(),
      },
    };

    console.log("Wysyłane dane do API:", payload); // Debugging

    const response = await fetch(`${API_URL}/create_collection/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Błąd API: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Błąd przy tworzeniu zbiórki:", error);
    throw error;
  }
}


export async function createPayment(account_number, amount, description, child_id = 0) {
  try {
    const token = getToken(); // Pobieramy token

    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    // Tworzymy payload z danymi do wysłania w żądaniu
    const payload = {
      account_number, // Numer konta przekazany jako argument
      amount, // Kwota płatności
      description, // Opis płatności
      child_id, // ID dziecka (domyślnie 0)
    };

    console.log("Wysyłane dane do API:", payload); // Debugging

    // Wykonujemy zapytanie POST do odpowiedniego endpointa
    const response = await fetch(`${API_URL}/create_payment/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Błąd API: ${response.status} - ${errorText}`);
    }

    return await response.json(); // Zwracamy odpowiedź z serwera
  } catch (error) {
    console.error("Błąd przy tworzeniu płatności:", error);
    throw error;
  }
};
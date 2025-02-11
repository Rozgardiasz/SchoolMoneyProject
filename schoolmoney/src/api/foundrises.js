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


export async function createPayment(description, account_number, amount, child_id) {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    // Walidacja danych wejściowych
    if (!account_number || typeof account_number !== "string") {
      throw new Error("Nieprawidłowy numer konta.");
    }
    if (!amount || isNaN(amount) || amount <= 0) {
      throw new Error("Kwota musi być większa niż 0.");
    }

    const payload = {
      account_number,
      amount,
      description,
      child_id,
    };

    console.log("Wysyłane dane do API:", payload);

    const response = await fetch(`${API_URL}/transfer/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    // Sprawdzenie odpowiedzi API
    if (!response.ok) {
      const errorData = await response.json().catch(() => null); // Obsługa braku JSON-a w odpowiedzi
      const errorMessage = errorData?.detail || response.statusText;
      
      if (response.status === 401) {
        throw new Error("Sesja wygasła. Zaloguj się ponownie.");
      }

      throw new Error(`Błąd API: ${errorMessage}`);
    }

    return await response.json(); // Zwróć odpowiedź API

  } catch (error) {
    console.error("Błąd przy tworzeniu płatności:", error);
    throw error;
  }
}


export async function closeCollectionEarly(collectionId) {
  try {
    const token = getToken(); // Pobieramy token
    
    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    const response = await fetch(`${API_URL}/close_collection_early/${collectionId}`, {
      method: "POST", // Zakładając, że endpoint używa POST
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    // Obsługuje błędy API
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Błąd API: ${response.status} - ${errorText}`);
    }

    return await response.json(); // Zwracamy odpowiedź API

  } catch (error) {
    console.error("Błąd podczas zamykania zbiórki wcześniej:", error);
    throw error;
  }
}



export async function modifyCollection(collectionId,fundEditData)
{
  try {
    const token = getToken();
    const response = await axios.put(
      `${API_URL}/modify_collection/${collectionId}`,
      fundEditData,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Błąd podczas pobierania zbiórek:", error);
    return [];
  }
}

export async function fetchCollectionById(classId, collectionId) {
  try {
    const token = getToken();
    const response = await axios.get(
      `${API_URL}/get_collections_in_class/${classId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    const collection = response.data.find((col) => col.id === collectionId);

    if (!collection) {
      console.warn(`Kolekcja o ID ${collectionId} nie została znaleziona.`);
      return null;
    }

    return {
      ...collection,
      image: collection.image || "https://finlio.pl/wp-content/uploads/2023/07/polska-waluta-zlotowka-951x530-c-default.jpg",
    };
  } catch (error) {
    console.error("Błąd podczas pobierania kolekcji:", error);
    return null;
  }
}


export async function fetchCollectionsInClass(classId) {
  try {
    const token = getToken();
    const response = await axios.get(
      `${API_URL}/get_collections_in_class/${classId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    return response.data.map(collection => ({
      ...collection,
      image: collection.image || "https://finlio.pl/wp-content/uploads/2023/07/polska-waluta-zlotowka-951x530-c-default.jpg",
    }));
  } catch (error) {
    console.error("Błąd podczas pobierania zbiórek:", error);
    return [];
  }
}



export async function fetchTransactionsForCollection(collectionId) {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    const response = await axios.get(
      `${API_URL}/transactions_for_collection/${collectionId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    return response.data.map(transaction => ({
      amount: transaction.amount,
      first_name: transaction.source?.first_name || "Nieznane",
      last_name: transaction.source?.last_name || "Nieznane",
      timestamp: transaction.timestamp
    }));
  } catch (error) {
    console.error("Błąd podczas pobierania transakcji dla zbiórki:", error);
    return [];
  }
}

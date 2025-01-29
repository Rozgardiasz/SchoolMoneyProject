import { getUserId, getAccountID, getAccountBalance, getAccountNumber } from "@/api/user";
import {getToken} from "@/api/auth"

export async function createCollection(fundData) {
  try {
    const token = getToken(); // Pobieramy token

    if (!token) {
      throw new Error("Brak tokena, użytkownik niezalogowany.");
    }

    const payload = {
      id: 0, // Backend generuje ID
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

    const response = await fetch("http://localhost:8000/create_collection/", {
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

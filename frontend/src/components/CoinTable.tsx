import React, { useEffect, useState } from "react";
import "./CoinTable.css"

interface Coin {
  id: string;
  symbol: string;
  name: string;
  current_price: number;
  market_cap: number;
  total_volume: number;
  high_24h: number;
  low_24h: number;
}

const API_URL = "http://localhost:8000/coins";

const CoinTable: React.FC = () => {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Failed to fetch data");
  
        const jsonResponse = await response.json();
        const data = jsonResponse.coins;
  
        if (data.length === 0) {
          setError("No coins available.");
        } else {
          setCoins(data);
        }
      } catch (err: any) {
        console.error("Fetch error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
  
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="bg-gray-900 relative overflow-x-auto shadow-md sm:rounded-lg bg-color">
      <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase dark:text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3 bg-gray-50 dark:bg-gray-800">Symbol</th>
              <th scope="col" className="px-6 py-3">Name</th>
              <th scope="col" className="px-6 py-3 bg-gray-50 dark:bg-gray-800">Price</th>
              <th scope="col" className="px-6 py-3">Market Cap</th>
              <th scope="col" className="px-6 py-3 bg-gray-50 dark:bg-gray-800">24h High</th>
              <th scope="col" className="px-6 py-3">24h Low</th>
            </tr>
          </thead>
          <tbody>
            {coins?.map((coin) => (
              <tr key={coin.id} className="border-b border-gray-200 dark:border-gray-700">
                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">{coin.symbol.toUpperCase()}</th>
                <td className="px-6 py-4">{coin.name}</td>
                <td className="px-6 py-4 bg-gray-50 dark:bg-gray-800">{coin.current_price.toFixed(2)}€</td>
                <td className="px-6 py-4">{coin.market_cap.toLocaleString()}€</td>
                <td className="px-6 py-4 bg-gray-50 dark:bg-gray-800">{coin.high_24h.toFixed(2)}€</td>
                <td className="px-6 py-4">{coin.low_24h.toFixed(2)}€</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
  );
};

export default CoinTable;

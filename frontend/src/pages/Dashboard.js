import { useEffect, useState } from "react";
import API from "../api";
import ProductCard from "../components/ProductCard";
import { Bar } from "react-chartjs-2";
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Dashboard() {
  const [products, setProducts] = useState([]);
  const [stats, setStats] = useState([]);

  useEffect(() => {
    API.get("/products").then(res => setProducts(res.data));
    API.get("/sentiment/stats").then(res => setStats(res.data));
  }, []);

  const chartData = {
    labels: stats.map(s => s.product),
    datasets: [
      {
        label: 'Average Positive',
        data: stats.map(s => s.avg_positive),
        backgroundColor: 'green',
      },
      {
        label: 'Average Negative',
        data: stats.map(s => s.avg_negative),
        backgroundColor: 'red',
      },
    ],
  };

  return (
    <div className="container">
      <h2>Dashboard</h2>
      {stats.length > 0 && (
        <div className="chart-container">
          <h3>Sentiment Overview</h3>
          <Bar data={chartData} />
        </div>
      )}
      <h3>Products</h3>
      {products.map(p => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
}
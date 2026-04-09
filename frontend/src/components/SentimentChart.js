import { Pie } from "react-chartjs-2";
import { Chart, ArcElement } from "chart.js";

Chart.register(ArcElement);

export default function SentimentChart({ positive, negative }) {
  const data = {
    labels: ["Positive", "Negative"],
    datasets: [
      {
        data: [positive, negative],
        backgroundColor: ["green", "red"]
      }
    ]
  };

  return <Pie data={data} />;
}
import { useState } from "react";
import API from "../api";
import SentimentChart from "./SentimentChart";

export default function FeedbackForm({ product }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const submit = async () => {
    const res = await API.post("/feedback", { product, text });
    setResult(res.data.analysis);
  };

  return (
    <div>
      <textarea placeholder="Write feedback..." onChange={(e) => setText(e.target.value)} />
      <button onClick={submit}>Submit</button>

      {result && (
        <>
          <p>Positive: {result.positive.toFixed(2)}</p>
          <p>Negative: {result.negative.toFixed(2)}</p>
          <SentimentChart positive={result.positive} negative={result.negative} />
        </>
      )}
    </div>
  );
}
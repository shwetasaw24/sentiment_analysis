import FeedbackForm from "./FeedbackForm";

export default function ProductCard({ product }) {
  return (
    <div className="card">
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <FeedbackForm product={product.name} />
    </div>
  );
}
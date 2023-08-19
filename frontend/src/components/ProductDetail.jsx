// components/ProductDetail.jsx
import React from "react";

function ProductDetail({ product }) {
    return (
        <div>
            <h1>Single Product Axios Call</h1>
            {Object.keys(product).length > 0 ? (
                <div>
                    <p>ID: {product.id}</p>
<p>Name: {product.name}</p>
<p>Category: {product.category}</p>
<p>Description: {product.description}</p>
<p>Posted By: {product.creator.first_name} {product.creator.last_name}</p>
<p>Quantity: {product.quantity}</p>
<p>Price: {product.price}</p>
<p>Reviews:</p>
<ul>
    {product.reviews.map((review, index) => (
        <li key={index}>
            <p>Content: {review.content}</p>
            <p>Rating: {review.rating}</p>
            <p>Posted By: {review.creator.first_name}</p>
        </li>
    ))}
</ul>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default ProductDetail;

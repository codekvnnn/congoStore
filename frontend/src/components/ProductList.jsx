// components/ProductList.jsx
import React from "react";

function ProductList({ title, products }) {
    return (
        <div>
            <h1>{title}</h1>
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
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
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ProductList;

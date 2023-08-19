import React, { useState, useEffect } from "react";
import LoginForm from './components/LoginForm';
import UserInfo from "./components/UserInfo";
import ProductDetail from "./components/ProductDetail";
import ProductList from "./components/ProductList";
import { 
    fetchAllProducts, 
    fetchProductsByCategory, 
    fetchProductsByDescription, 
    fetchProductById,
    fetchUserById,
    loginUser
} from './services/apiService';

function App() {
    const [allProducts, setAllProducts] = useState([]);
    const [allProductsByCategory, setAllProductsByCategory] = useState([]);
    const [allProductsByDescription, setAllProductsByDescription] = useState([]);
    const [productOne, setProductOne] = useState({});
    const [user, setUser] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const products = await fetchAllProducts();
                setAllProducts(products.data);

                const productsByCategory = await fetchProductsByCategory('furniture');
                setAllProductsByCategory(productsByCategory.data);

                const productsByDescription = await fetchProductsByDescription('furniture');
                setAllProductsByDescription(productsByDescription.data);

                const singleProduct = await fetchProductById(4);
                setProductOne(singleProduct.data);

                const singleUser = await fetchUserById(1);
                setUser(singleUser.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    const handleLogin = async (email, password) => {
        try {
            const response = await loginUser({ email, password });
            if (response.data.errors) {
                setErrors(response.data.errors);
            } else {
                setErrors({});
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <>
            <LoginForm onLogin={handleLogin} errors={errors} />

            <UserInfo user={user} />

            <ProductDetail product={productOne} />

            <ProductList title="All Products by Category *furniture filter*" products={allProductsByCategory} />

            <ProductList title="All Products by Description *furniture filter*" products={allProductsByDescription} />

            <ProductList title="All Products" products={allProducts} />
        </>
    );
}

export default App;

import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000/api';

export const fetchAllProducts = () => {
    return axios.get(`${BASE_URL}/products`);
}

export const fetchProductsByCategory = (category) => {
    return axios.get(`${BASE_URL}/products/category/${category}`);
}

export const fetchProductsByDescription = (description) => {
    return axios.get(`${BASE_URL}/products/description/${description}`);
}

export const fetchProductById = (id) => {
    return axios.get(`${BASE_URL}/products/view/${id}`);
}

export const fetchUserById = (id) => {
    return axios.get(`${BASE_URL}/users/${id}`);
}

export const loginUser = (data) => {
    return axios.post(`${BASE_URL}/users/login`, data);
}

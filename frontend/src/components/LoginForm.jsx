import React, { useState } from "react";

function LoginForm({ onLogin, errors }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onLogin(email, password);
    };

    return (
        <div>
            <h1>Login Form</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    {errors['email'] && <p style={{ color: 'red' }}>{errors['email']}</p>}
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div>
                    <label>Password:</label>
                    {errors['password'] && <p style={{ color: 'red' }}>{errors['password']}</p>}
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LoginForm;

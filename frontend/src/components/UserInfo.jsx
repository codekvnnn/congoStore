// components/UserInfo.jsx
import React from "react";

function UserInfo({ user }) {
    return (
        <div>
            <h1>User Info Axios Call</h1>
            <p>{user.id}</p>
            <p>{user.first_name}</p>
            <p>{user.last_name}</p>
            <p>{user.address}</p>
            <p>{user.email}</p>
        </div>
    );
}

export default UserInfo;

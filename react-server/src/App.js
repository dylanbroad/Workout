import React, { useState, useEffect } from 'react';
import UserList from './components/UserList';
import Form from './components/Form';

function App() {

  const [users, setUsers] = useState([])
  const [editedUser, setEditedUser] = useState(null)


  useEffect(() => {
   fetch('http://127.0.0.1:5000/user', {
      'method':'GET',
      headers: {
          'Contenty-Type':'application/json'
      }
   })
   .then(resp=> resp.json())
   .then(resp=> setUsers(resp))
   .catch(error => console.log(error))
   
  }, [])

  const editUser = (user) => {
    setEditedUser(user)
  }

  return (
      <div>
          <h1>Sign Up</h1>
          
          <UserList users = {users} editUser = {editUser}/>

          {editedUser ? <Form user = {editedUser}/> : null}

          
      </div>

  );
}

export default App
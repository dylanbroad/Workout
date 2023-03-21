import React, { useState } from 'react'

function Form(props) {
    const[username, setUsername] = useState(props.user.username)
    const[password, setPassword] = useState(props.user.password)

    const updateUser = () => {
        
    }



  return (
    <div>
        {props.user ? (
            <div className = "mb-3">

            <label htmlForm = "username" className= "form-label">Username</label>
            <input type="text" className="form-control"
            value = {username}
            placeholder= "Please Enter Username"
            onChange = {(e) => setUsername(e.target.value)}
            />
 
            <label htmlForm = "password" className= "form-label">Password</label>
            <textarea
            rows = "5"
            value = {password}
            onChange = {(e) => setPassword(e.target.value)}
            className = "form-control"
            placeholder=" Please Enter Password"

            />
            <button
            onClick = {updateUser}
            className = "btn btn-success mt-3"
            >Update</button>
        
         </div>
        ):null}
            
            
        
        
        
    </div>
  )
}

export default Form

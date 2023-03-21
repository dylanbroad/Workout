import React from 'react'

function UserList(props) {

    const editUser = (user) => {
        props.editUser(user)
    }

  return (
    <div>
      {props.users && props.users.map(user => {
            return (
              <div key = {user.id}>
                <h2>{user.username}</h2>
                <h2>{user.password}</h2>
                
                <div className= "row">
                    <div className= " col-md-1">
                        <button className= "btn btn-primary"
                        onClick = {() => editUser(user)}
                        >Update</button>

                    </div>
                    <div className= " col">
                        <button className= "btn btn-danger">Delete</button>

                    </div>
                </div>
                <hr/>
              </div>
            )
          })}
    </div>
  )
}

export default UserList

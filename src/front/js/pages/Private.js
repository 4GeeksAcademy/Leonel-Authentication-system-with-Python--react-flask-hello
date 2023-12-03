import React from 'react'
import { useContext } from 'react'
import { Context } from '../store/appContext'
import { useNavigate } from 'react-router-dom'
import "../../styles/private.css"
import { Navbar } from '../component/navbar'

const Private = () => {
  const {store,actions}=useContext(Context)
  const storageToken=sessionStorage.getItem("userToken")
  const storageEmail=sessionStorage.getItem("userEmail")
  const storageUserName=sessionStorage.getItem("userName")
  const storageUserId=sessionStorage.getItem("userId")
  const goToHome=useNavigate()

  const handleLogout=()=>{
    sessionStorage.removeItem("userToken")
    sessionStorage.removeItem("userEmail")
    sessionStorage.removeItem("userName")
    sessionStorage.removeItem("userId")
    goToHome("/")
  }

  return (
    <>
    <Navbar/>
    <div className='container-private'>
      {storageToken?(
        <div className='container-information'><p>Hello! {storageUserName} </p>
        <p>This is your email: {storageEmail} </p>
        <p>You are the user number: {storageUserId} </p>
        <div className='container-button'>
          <button className='button-logout' type='button' onClick={()=>handleLogout()}>Log out</button>
        </div>
        </div>
      ):(
        <div className='container-information'> <p>You are not loggid in</p></div>
      )}

    </div>
    </>
    
  )
}

export default Private
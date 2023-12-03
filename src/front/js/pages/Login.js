import React, { useRef, useState } from 'react'
import '../../styles/login.css'
import { useContext } from 'react'
import { Context } from '../store/appContext'
import { useNavigate,Link } from 'react-router-dom'

const Login = () => {
    
    const {store,actions}=useContext(Context)
    const [login, setLogin]=useState(store.formLogin)
  
    const goToPrivate=useNavigate()

    const formRef= useRef (null)
  
    const handleInputForm = (value,name)=>{
        setLogin({...login,[name]:value})
  
    }
  
    const handleSubmit = async (formLogin)=>{
      
      try{
        console.log(formLogin)
        await actions.loginUserExisting(formLogin)
        // alert(`The user with the name  ${store.messageToShowAlert.user_created} was created succesfully`)
        formRef.current.reset()
        setLogin(store.formLogin)
        const token= store.tokenUser.accessToken
        console.log("iniciamos sesion en el nuevo usuario")
        console.log(token)
        sessionStorage.setItem("userToken",token)
        await actions.getInformationOfToken()

        sessionStorage.setItem("userEmail",store.informationUserLogin.email)
        sessionStorage.setItem("userName",store.informationUserLogin.user_name)
        sessionStorage.setItem("userId",store.informationUserLogin.user_id)

        goToPrivate("/private")
    }
      catch(e){
        console.log("An error was occurred, check it out", e)
      }
    }
  
    return (
      <div className='container-form'>
          <form 
          ref={formRef}
          id='contact-form' className='form-signup'>
              <label className='label-signup' for="email">Email:</label>
              <input className='input-signup' type="email" id="email" name="email" onChange={(e)=>(handleInputForm(e.target.value, e.target.name))} required/>
    
              <label className='label-signup' for="password">Password:</label>
              <input className='input-signup' type="password" id="password" name="password"  onChange={(e)=>(handleInputForm(e.target.value, e.target.name))} required/>
  
              <button className="button-signup" type="button" onClick={()=>handleSubmit(login)}>Login</button>
          </form>

          <div className='goHome-login'>
            <Link to="/">Go to Home</Link>
            </div>

      </div>
    )
}

export default Login
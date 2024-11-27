import { createContext, useEffect, useState } from "react";
import React from 'react'

// creating the AuthContext
export const AuthContext = createContext()

function AuthProvider({children}) {
    const [currentUser, setCurrentUSer] = useState(null)

    // Checking if the token is present
    useEffect(()=>{
        const token = localStorage.getItem("token")
        if (token){
            setCurrentUSer(token)

        }
    }, [])

    const logout = ()=>{
        localStorage.removeItem("token")
        setCurrentUSer(null)
    }


  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUSer, logout }}>
        {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider
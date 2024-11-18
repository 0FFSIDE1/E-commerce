import React, { useContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import AuthContext from './AuthContext'

function ProtectiveRoute(children) {

    const {currentUser} = useContext(AuthContext)
    const navigate = useNavigate()

    // if the user is not logged in, redirect
    useEffect(()=>{
        if(!currentUser){
            return navigate("#")
        }
    }, [])

    // if user is autheticated, you can the protected components
    return children
}

export default ProtectiveRoute
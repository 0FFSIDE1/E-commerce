import React from 'react'
import NavBar from './NavBar'
import Footer from './Footer'

function PageContainer({children, showNav, showFooter}) {
  return (
    <main className='flex flex-col h-screen'>
        {showNav && <NavBar/>}
        <div className="flex-grow">
            {children}
        </div>
        {showFooter && <Footer/>}
    </main>
  )
}

export default PageContainer
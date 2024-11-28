import React from 'react'
import PageContainer from '../components/General/PageContainer'
import Hero from '../components/landing/Hero'
import Footer from '../components/General/Footer'
import Body from '../components/landing/Body'

function Landing() {
  return (
    <PageContainer showNav={true}>
        <Hero/>
        <Body/>
        <Footer/>
    </PageContainer>
  )
}

export default Landing
import React from 'react'
import PageContainer from '../components/General/PageContainer'
import Hero from '../components/landing/Hero'

function Landing() {
  return (
    <PageContainer showNav={true}>
        <Hero/>
    </PageContainer>
  )
}

export default Landing
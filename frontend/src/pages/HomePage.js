import React, { useState } from 'react';
import { mockData } from '../mock';
import Header from '../components/Header';
import AboutSection from '../components/AboutSection';
import ServicesSection from '../components/ServicesSection';
import PortfolioSection from '../components/PortfolioSection';
import ContactSection from '../components/ContactSection';
import Footer from '../components/Footer';

const HomePage = () => {
  const [services, setServices] = useState(mockData.services);
  const [portfolio, setPortfolio] = useState(mockData.portfolio);
  const [contacts, setContacts] = useState(mockData.company);

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50">
      <Header contacts={contacts} />
      <main>
        <AboutSection />
        <ServicesSection services={services} />
        <PortfolioSection portfolio={portfolio} />
        <ContactSection contacts={contacts} />
      </main>
      <Footer contacts={contacts} />
    </div>
  );
};

export default HomePage;
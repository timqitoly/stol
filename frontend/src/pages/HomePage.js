import React, { useState, useEffect } from 'react';
import { servicesAPI, portfolioAPI, contactsAPI, handleAPIError } from '../services/api';
import Header from '../components/Header';
import AboutSection from '../components/AboutSection';
import ServicesSection from '../components/ServicesSection';
import PortfolioSection from '../components/PortfolioSection';
import ContactSection from '../components/ContactSection';
import Footer from '../components/Footer';
import { useToast } from "../hooks/use-toast";

const HomePage = () => {
  const [services, setServices] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [contacts, setContacts] = useState({});
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  const fetchData = async () => {
    try {
      setLoading(true);
      
      const [servicesData, portfolioData, contactsData] = await Promise.all([
        servicesAPI.getAll(),
        portfolioAPI.getAll(),
        contactsAPI.get()
      ]);
      
      setServices(servicesData);
      setPortfolio(portfolioData);
      setContacts(contactsData);
      
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка загрузки данных",
        description: errorInfo.message,
        variant: "destructive",
      });
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-amber-900 text-lg">Загрузка...</p>
        </div>
      </div>
    );
  }

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
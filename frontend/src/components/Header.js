import React from 'react';
import { mockData } from '../mock';
import { Button } from "./ui/button";
import { Phone } from 'lucide-react';

const Header = () => {
  const scrollToContacts = () => {
    document.getElementById('contacts').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-amber-900 via-orange-900 to-red-900 shadow-lg backdrop-blur-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-amber-200 to-orange-300 rounded-full flex items-center justify-center shadow-lg">
              <span className="text-2xl font-bold text-amber-900">КТ</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-amber-100">{mockData.company.name}</h1>
              <p className="text-amber-200 text-sm">{mockData.company.tagline}</p>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#about" className="text-amber-100 hover:text-amber-200 transition-colors">О нас</a>
            <a href="#services" className="text-amber-100 hover:text-amber-200 transition-colors">Услуги</a>
            <a href="#portfolio" className="text-amber-100 hover:text-amber-200 transition-colors">Портфолио</a>
            <a href="#contacts" className="text-amber-100 hover:text-amber-200 transition-colors">Контакты</a>
          </nav>

          <Button 
            onClick={scrollToContacts}
            className="bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white shadow-lg transition-all duration-300 transform hover:scale-105"
          >
            <Phone className="w-4 h-4 mr-2" />
            Связаться в WhatsApp
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
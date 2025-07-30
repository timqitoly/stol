import React from 'react';

const Footer = ({ contacts }) => {
  return (
    <footer className="bg-gradient-to-r from-amber-900 via-orange-900 to-red-900 text-amber-100 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 text-center md:text-left">
            <div>
              <div className="flex items-center justify-center md:justify-start space-x-4 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-amber-200 to-orange-300 rounded-full flex items-center justify-center">
                  <span className="text-lg font-bold text-amber-900">КТ</span>
                </div>
                <h3 className="text-xl font-bold">{contacts.name}</h3>
              </div>
              <p className="text-amber-200">{contacts.tagline}</p>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4">Услуги</h4>
              <ul className="space-y-2 text-amber-200">
                <li>Чистовая отделка деревом</li>
                <li>Столярные услуги</li>
                <li>Изготовление мебели</li>
                <li>Строительство бань</li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4">Контакты</h4>
              <div className="space-y-2 text-amber-200">
                <p>{contacts.phone}</p>
                <p>{contacts.email}</p>
                <p>Москва и область</p>
              </div>
            </div>
          </div>
          
          <div className="border-t border-amber-800 mt-8 pt-8 text-center">
            <p className="text-amber-300">
              © 2024 {contacts.name}. Все права защищены.
            </p>
            <div className="mt-2">
              <a href="/admin" className="text-amber-400 hover:text-amber-300 text-sm">
                Админ-панель
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
import React, { useState } from 'react';
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Phone, Mail, MessageCircle, Send } from 'lucide-react';
import { useToast } from "../hooks/use-toast";

const ContactSection = ({ contacts }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    message: ''
  });
  const { toast } = useToast();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock form submission
    toast({
      title: "Заявка отправлена!",
      description: "Мы свяжемся с вами в ближайшее время.",
    });
    setFormData({ name: '', phone: '', message: '' });
  };

  const openWhatsApp = () => {
    const message = encodeURIComponent("Здравствуйте! Интересует ваша услуга по деревянной отделке.");
    window.open(`https://wa.me/${contacts.whatsapp}?text=${message}`, '_blank');
  };

  return (
    <section id="contacts" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-amber-900 mb-4">Связаться с нами</h2>
            <div className="w-24 h-1 bg-gradient-to-r from-amber-600 to-orange-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Работаем в Москве и области. Доставка и замеры на месте.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <Card className="shadow-lg border border-amber-200">
                <CardHeader>
                  <CardTitle className="text-2xl text-amber-900">Оставить заявку</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                      <Input
                        type="text"
                        name="name"
                        placeholder="Ваше имя"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                        className="border-amber-200 focus:border-amber-500"
                      />
                    </div>
                    <div>
                      <Input
                        type="tel"
                        name="phone"
                        placeholder="+7 (999) 123-45-67"
                        value={formData.phone}
                        onChange={handleInputChange}
                        required
                        className="border-amber-200 focus:border-amber-500"
                      />
                    </div>
                    <div>
                      <Textarea
                        name="message"
                        placeholder="Опишите вашу задачу..."
                        rows={4}
                        value={formData.message}
                        onChange={handleInputChange}
                        className="border-amber-200 focus:border-amber-500"
                      />
                    </div>
                    <Button 
                      type="submit" 
                      className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white"
                    >
                      <Send className="w-4 h-4 mr-2" />
                      Отправить заявку
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card className="shadow-lg border border-amber-200">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-amber-600 to-orange-600 rounded-full flex items-center justify-center">
                      <Phone className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-amber-900">Телефон</h3>
                      <a href={`tel:${contacts.phone}`} className="text-gray-600 hover:text-amber-700">
                        {contacts.phone}
                      </a>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="shadow-lg border border-amber-200">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-amber-600 to-orange-600 rounded-full flex items-center justify-center">
                      <Mail className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-amber-900">Email</h3>
                      <a href={`mailto:${contacts.email}`} className="text-gray-600 hover:text-amber-700">
                        {contacts.email}
                      </a>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Button 
                onClick={openWhatsApp}
                className="w-full bg-green-600 hover:bg-green-700 text-white text-lg py-6 shadow-lg transition-all duration-300 transform hover:scale-105"
              >
                <MessageCircle className="w-6 h-6 mr-2" />
                Написать в WhatsApp
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;
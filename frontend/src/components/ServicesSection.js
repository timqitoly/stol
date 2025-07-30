import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogTrigger } from "./ui/dialog";
import { Eye } from 'lucide-react';

const ServicesSection = ({ services }) => {
  const [selectedService, setSelectedService] = useState(null);

  return (
    <section id="services" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-amber-900 mb-4">Услуги и цены</h2>
            <div className="w-24 h-1 bg-gradient-to-r from-amber-600 to-orange-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Качественная работа по доступным ценам</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8">
            {services.map((service) => (
              <Card key={service.id} className="overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border border-amber-200">
                <div className="relative">
                  <img 
                    src={service.images[0]} 
                    alt={service.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-amber-900/30 to-transparent"></div>
                  <Badge className="absolute top-4 right-4 bg-amber-600 text-white">
                    {service.price}
                  </Badge>
                </div>
                
                <CardHeader>
                  <CardTitle className="text-xl text-amber-900">{service.name}</CardTitle>
                  <CardDescription className="text-gray-600">
                    {service.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button 
                        variant="outline" 
                        className="w-full border-amber-600 text-amber-700 hover:bg-amber-50"
                        onClick={() => setSelectedService(service)}
                      >
                        <Eye className="w-4 h-4 mr-2" />
                        Посмотреть фото
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-4xl">
                      {selectedService && (
                        <div>
                          <h3 className="text-2xl font-bold text-amber-900 mb-4">{selectedService.name}</h3>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {selectedService.images.map((image, index) => (
                              <img 
                                key={index}
                                src={image} 
                                alt={`${selectedService.name} ${index + 1}`}
                                className="w-full h-64 object-cover rounded-lg shadow-lg"
                              />
                            ))}
                          </div>
                          <p className="mt-4 text-gray-700">{selectedService.description}</p>
                          <div className="mt-4 text-center">
                            <Badge className="bg-amber-600 text-white text-lg px-4 py-2">
                              {selectedService.price}
                            </Badge>
                          </div>
                        </div>
                      )}
                    </DialogContent>
                  </Dialog>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;
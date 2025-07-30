import React, { useState } from 'react';
import { mockData } from '../mock';
import { Dialog, DialogContent, DialogTrigger } from "./ui/dialog";
import { Badge } from "./ui/badge";

const PortfolioSection = () => {
  const [selectedImage, setSelectedImage] = useState(null);

  return (
    <section id="portfolio" className="py-20 bg-gradient-to-b from-orange-50 to-amber-50">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-amber-900 mb-4">Наши работы</h2>
            <div className="w-24 h-1 bg-gradient-to-r from-amber-600 to-orange-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Галерея выполненных проектов</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockData.portfolio.map((item) => (
              <Dialog key={item.id}>
                <DialogTrigger asChild>
                  <div 
                    className="relative cursor-pointer group overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    onClick={() => setSelectedImage(item)}
                  >
                    <img 
                      src={item.image} 
                      alt={item.title}
                      className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-amber-900/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    <div className="absolute bottom-4 left-4 right-4 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <h3 className="text-lg font-bold mb-1">{item.title}</h3>
                      <Badge className="bg-amber-600/80 text-white">
                        {item.category}
                      </Badge>
                    </div>
                  </div>
                </DialogTrigger>
                <DialogContent className="max-w-4xl">
                  {selectedImage && (
                    <div className="text-center">
                      <img 
                        src={selectedImage.image} 
                        alt={selectedImage.title}
                        className="w-full max-h-[70vh] object-contain rounded-lg"
                      />
                      <div className="mt-4">
                        <h3 className="text-2xl font-bold text-amber-900">{selectedImage.title}</h3>
                        <Badge className="mt-2 bg-amber-600 text-white">
                          {selectedImage.category}
                        </Badge>
                      </div>
                    </div>
                  )}
                </DialogContent>
              </Dialog>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default PortfolioSection;
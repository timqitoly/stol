import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { Upload, Images } from 'lucide-react';
import ImageUpload from './ImageUpload';
import ImageGallery from './ImageGallery';

const ImageManager = ({ onImageSelect, selectedImages = [], mode = 'single', trigger }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('gallery');

  const handleImageUploaded = (image) => {
    // Switch to gallery tab after upload
    setActiveTab('gallery');
  };

  const handleImageSelect = (images) => {
    if (onImageSelect) {
      onImageSelect(images);
    }
    setIsOpen(false);
  };

  const TriggerButton = trigger || (
    <Button variant="outline" className="border-amber-600 text-amber-700 hover:bg-amber-50">
      <Images className="w-4 h-4 mr-2" />
      Выбрать изображение
    </Button>
  );

  return (
    <>
      <div onClick={() => setIsOpen(true)}>
        {TriggerButton}
      </div>
      
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-6xl max-h-[90vh] overflow-auto">
          <DialogHeader>
            <DialogTitle className="text-2xl text-amber-900">
              Управление изображениями
            </DialogTitle>
          </DialogHeader>
          
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="gallery" className="flex items-center space-x-2">
                <Images className="w-4 h-4" />
                <span>Галерея</span>
              </TabsTrigger>
              <TabsTrigger value="upload" className="flex items-center space-x-2">
                <Upload className="w-4 h-4" />
                <span>Загрузить</span>
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="gallery">
              <ImageGallery
                onImageSelect={handleImageSelect}
                selectedImages={selectedImages}
                mode={mode}
              />
            </TabsContent>
            
            <TabsContent value="upload">
              <div className="space-y-6">
                <ImageUpload onImageUploaded={handleImageUploaded} />
                <div className="text-center">
                  <p className="text-sm text-gray-600">
                    После загрузки изображение появится в галерее
                  </p>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default ImageManager;
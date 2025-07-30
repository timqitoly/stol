import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Input } from "./ui/input";
import { Search, Trash2, Check, Copy, Loader } from 'lucide-react';
import { imagesAPI, handleAPIError } from '../services/api';
import { useToast } from "../hooks/use-toast";

const ImageGallery = ({ onImageSelect, selectedImages = [], mode = 'single' }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedImageIds, setSelectedImageIds] = useState(selectedImages);
  const { toast } = useToast();

  const fetchImages = async () => {
    try {
      setLoading(true);
      const imagesData = await imagesAPI.getAll();
      setImages(imagesData);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка загрузки изображений",
        description: errorInfo.message,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const handleImageSelect = (image) => {
    if (mode === 'single') {
      setSelectedImageIds([image.id]);
      if (onImageSelect) {
        onImageSelect([image]);
      }
    } else {
      const isSelected = selectedImageIds.includes(image.id);
      let newSelection;
      
      if (isSelected) {
        newSelection = selectedImageIds.filter(id => id !== image.id);
      } else {
        newSelection = [...selectedImageIds, image.id];
      }
      
      setSelectedImageIds(newSelection);
      
      if (onImageSelect) {
        const selectedImagesData = images.filter(img => newSelection.includes(img.id));
        onImageSelect(selectedImagesData);
      }
    }
  };

  const handleImageDelete = async (imageId) => {
    try {
      await imagesAPI.delete(imageId);
      toast({
        title: "Изображение удалено",
        description: "Изображение было удалено успешно",
      });
      fetchImages();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка удаления",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  const copyImageUrl = (url) => {
    navigator.clipboard.writeText(url);
    toast({
      title: "URL скопирован",
      description: "URL изображения скопирован в буфер обмена",
    });
  };

  const filteredImages = images.filter(image =>
    image.original_filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle className="text-xl text-amber-900">Галерея изображений</CardTitle>
          <Badge variant="outline" className="text-amber-700">
            {filteredImages.length} изображений
          </Badge>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Поиск по названию файла..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 border-amber-200 focus:border-amber-500"
          />
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center py-8">
            <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-amber-600" />
            <p className="text-amber-700">Загрузка изображений...</p>
          </div>
        ) : filteredImages.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">
              {searchTerm ? 'Изображения не найдены' : 'Изображения не загружены'}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredImages.map((image) => {
              const isSelected = selectedImageIds.includes(image.id);
              
              return (
                <div key={image.id} className="relative">
                  <Card 
                    className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                      isSelected ? 'ring-2 ring-amber-500 shadow-lg' : 'hover:ring-1 hover:ring-amber-300'
                    }`}
                    onClick={() => handleImageSelect(image)}
                  >
                    <div className="relative">
                      <img
                        src={image.url}
                        alt={image.original_filename}
                        className="w-full h-32 object-cover rounded-t-lg"
                      />
                      {isSelected && (
                        <div className="absolute top-2 right-2 bg-amber-600 text-white rounded-full p-1">
                          <Check className="w-4 h-4" />
                        </div>
                      )}
                    </div>
                    <div className="p-3">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {image.original_filename}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {formatFileSize(image.size)}
                      </p>
                    </div>
                  </Card>
                  
                  <div className="absolute top-2 left-2 flex space-x-1">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          variant="outline"
                          size="sm"
                          className="h-8 w-8 p-0 bg-white/80 backdrop-blur-sm hover:bg-white"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-2xl">
                        <DialogHeader>
                          <DialogTitle>Информация об изображении</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          <img
                            src={image.url}
                            alt={image.original_filename}
                            className="w-full max-h-64 object-contain rounded-lg"
                          />
                          <div className="space-y-2">
                            <div>
                              <label className="text-sm font-medium text-gray-700">Название:</label>
                              <p className="text-sm text-gray-600">{image.original_filename}</p>
                            </div>
                            <div>
                              <label className="text-sm font-medium text-gray-700">Размер:</label>
                              <p className="text-sm text-gray-600">{formatFileSize(image.size)}</p>
                            </div>
                            <div>
                              <label className="text-sm font-medium text-gray-700">URL:</label>
                              <div className="flex items-center space-x-2">
                                <Input value={image.url} readOnly className="text-xs" />
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => copyImageUrl(image.url)}
                                >
                                  <Copy className="w-4 h-4" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-8 w-8 p-0 bg-white/80 backdrop-blur-sm hover:bg-red-50 border-red-500 text-red-600"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleImageDelete(image.id);
                      }}
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ImageGallery;
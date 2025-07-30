import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Upload, X, Loader, Image as ImageIcon } from 'lucide-react';
import { imagesAPI, handleAPIError } from '../services/api';
import { useToast } from "../hooks/use-toast";

const ImageUpload = ({ onImageUploaded, accept = "image/*", maxSize = 5 * 1024 * 1024 }) => {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(null);
  const { toast } = useToast();

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    
    // Validate file size
    if (file.size > maxSize) {
      toast({
        title: "Ошибка",
        description: "Размер файла превышает 5MB",
        variant: "destructive",
      });
      return;
    }
    
    // Create preview
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result);
    reader.readAsDataURL(file);
    
    try {
      setUploading(true);
      const response = await imagesAPI.upload(file);
      
      if (response.success) {
        toast({
          title: "Успешно",
          description: response.message,
        });
        
        if (onImageUploaded) {
          onImageUploaded(response.image);
        }
      } else {
        toast({
          title: "Ошибка",
          description: response.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка загрузки",
        description: errorInfo.message,
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  }, [maxSize, onImageUploaded, toast]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: { [accept]: [] },
    maxFiles: 1,
    maxSize,
  });

  const clearPreview = () => {
    setPreview(null);
  };

  return (
    <Card className="border-2 border-dashed border-amber-200 hover:border-amber-400 transition-colors">
      <CardContent className="p-6">
        {preview ? (
          <div className="relative">
            <img 
              src={preview} 
              alt="Preview" 
              className="w-full h-48 object-cover rounded-lg"
            />
            <Button
              variant="outline"
              size="sm"
              className="absolute top-2 right-2 bg-white/80 backdrop-blur-sm"
              onClick={clearPreview}
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        ) : (
          <div
            {...getRootProps()}
            className={`cursor-pointer p-8 text-center transition-colors rounded-lg ${
              isDragActive 
                ? 'bg-amber-50 border-amber-400' 
                : isDragReject 
                ? 'bg-red-50 border-red-400' 
                : 'hover:bg-amber-50'
            }`}
          >
            <input {...getInputProps()} />
            
            {uploading ? (
              <div className="space-y-4">
                <Loader className="w-12 h-12 mx-auto text-amber-600 animate-spin" />
                <p className="text-amber-700">Загрузка изображения...</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex justify-center">
                  {isDragActive ? (
                    <Upload className="w-12 h-12 text-amber-600" />
                  ) : (
                    <ImageIcon className="w-12 h-12 text-amber-400" />
                  )}
                </div>
                
                <div>
                  <p className="text-lg font-medium text-amber-900">
                    {isDragActive ? 'Отпустите файл здесь' : 'Загрузить изображение'}
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    Перетащите файл сюда или нажмите для выбора
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Максимальный размер: 5MB
                  </p>
                </div>
                
                <Button 
                  variant="outline" 
                  className="border-amber-600 text-amber-700 hover:bg-amber-50"
                >
                  Выбрать файл
                </Button>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ImageUpload;
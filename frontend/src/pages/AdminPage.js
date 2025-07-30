import React, { useState } from 'react';
import { mockData, adminData } from '../mock';
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../components/ui/dialog";
import { useToast } from "../../hooks/use-toast";
import { Edit, Save, Trash2, Plus, LogOut, Eye } from 'lucide-react';

const AdminPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginData, setLoginData] = useState({ login: '', password: '' });
  const [services, setServices] = useState(mockData.services);
  const [editingService, setEditingService] = useState(null);
  const [newService, setNewService] = useState({
    name: '',
    description: '',
    price: '',
    images: ['']
  });
  const { toast } = useToast();

  const handleLogin = (e) => {
    e.preventDefault();
    if (loginData.login === adminData.login && loginData.password === adminData.password) {
      setIsAuthenticated(true);
      toast({
        title: "Успешный вход",
        description: "Добро пожаловать в админ-панель!",
      });
    } else {
      toast({
        title: "Ошибка входа",
        description: "Неверный логин или пароль",
        variant: "destructive",
      });
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setLoginData({ login: '', password: '' });
  };

  const handleEditService = (service) => {
    setEditingService({ ...service });
  };

  const handleSaveService = () => {
    setServices(services.map(s => s.id === editingService.id ? editingService : s));
    setEditingService(null);
    toast({
      title: "Услуга обновлена",
      description: "Изменения сохранены успешно!",
    });
  };

  const handleDeleteService = (id) => {
    setServices(services.filter(s => s.id !== id));
    toast({
      title: "Услуга удалена",
      description: "Услуга была удалена из списка",
    });
  };

  const handleAddService = () => {
    const id = Math.max(...services.map(s => s.id)) + 1;
    setServices([...services, { ...newService, id }]);
    setNewService({ name: '', description: '', price: '', images: [''] });
    toast({
      title: "Услуга добавлена",
      description: "Новая услуга была добавлена успешно!",
    });
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100 flex items-center justify-center p-4">
        <Card className="w-full max-w-md shadow-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-amber-900">Вход в админ-панель</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <Input
                type="text"
                placeholder="Логин"
                value={loginData.login}
                onChange={(e) => setLoginData({...loginData, login: e.target.value})}
                className="border-amber-200 focus:border-amber-500"
              />
              <Input
                type="password"
                placeholder="Пароль"
                value={loginData.password}
                onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                className="border-amber-200 focus:border-amber-500"
              />
              <Button 
                type="submit" 
                className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700"
              >
                Войти
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100 p-4">
      <div className="container mx-auto max-w-6xl">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-amber-900">Админ-панель</h1>
          <div className="flex space-x-4">
            <Button 
              variant="outline" 
              onClick={() => window.open('/', '_blank')}
              className="border-amber-600 text-amber-700"
            >
              <Eye className="w-4 h-4 mr-2" />
              Посмотреть сайт
            </Button>
            <Button onClick={handleLogout} variant="outline" className="border-red-500 text-red-600">
              <LogOut className="w-4 h-4 mr-2" />
              Выйти
            </Button>
          </div>
        </div>

        <div className="space-y-6">
          <Card className="shadow-lg">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="text-xl text-amber-900">Управление услугами</CardTitle>
              <Dialog>
                <DialogTrigger asChild>
                  <Button className="bg-green-600 hover:bg-green-700">
                    <Plus className="w-4 h-4 mr-2" />
                    Добавить услугу
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Добавить новую услугу</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-4">
                    <Input
                      placeholder="Название услуги"
                      value={newService.name}
                      onChange={(e) => setNewService({...newService, name: e.target.value})}
                    />
                    <Textarea
                      placeholder="Описание услуги"
                      value={newService.description}
                      onChange={(e) => setNewService({...newService, description: e.target.value})}
                    />
                    <Input
                      placeholder="Цена (например: от 50 000 ₽)"
                      value={newService.price}
                      onChange={(e) => setNewService({...newService, price: e.target.value})}
                    />
                    <Input
                      placeholder="URL изображения"
                      value={newService.images[0]}
                      onChange={(e) => setNewService({...newService, images: [e.target.value]})}
                    />
                    <Button onClick={handleAddService} className="w-full">
                      Добавить услугу
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {services.map((service) => (
                  <div key={service.id} className="border border-amber-200 rounded-lg p-4 bg-white">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg text-amber-900">{service.name}</h3>
                        <p className="text-gray-600 mt-1">{service.description}</p>
                        <p className="font-semibold text-amber-700 mt-2">{service.price}</p>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => handleEditService(service)}
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-2xl">
                            <DialogHeader>
                              <DialogTitle>Редактировать услугу</DialogTitle>
                            </DialogHeader>
                            {editingService && (
                              <div className="space-y-4">
                                <Input
                                  value={editingService.name}
                                  onChange={(e) => setEditingService({...editingService, name: e.target.value})}
                                />
                                <Textarea
                                  value={editingService.description}
                                  onChange={(e) => setEditingService({...editingService, description: e.target.value})}
                                />
                                <Input
                                  value={editingService.price}
                                  onChange={(e) => setEditingService({...editingService, price: e.target.value})}
                                />
                                <Button onClick={handleSaveService} className="w-full">
                                  <Save className="w-4 h-4 mr-2" />
                                  Сохранить изменения
                                </Button>
                              </div>
                            )}
                          </DialogContent>
                        </Dialog>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => handleDeleteService(service.id)}
                          className="border-red-500 text-red-600 hover:bg-red-50"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
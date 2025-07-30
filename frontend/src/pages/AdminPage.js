import React, { useState, useEffect } from 'react';
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { useToast } from "../hooks/use-toast";
import { Edit, Save, Trash2, Plus, LogOut, Eye, Phone, Mail, Loader } from 'lucide-react';
import { servicesAPI, portfolioAPI, contactsAPI, adminAPI, handleAPIError } from '../services/api';

const AdminPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginData, setLoginData] = useState({ login: '', password: '' });
  const [services, setServices] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [contacts, setContacts] = useState({});
  const [loading, setLoading] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [editingPortfolio, setEditingPortfolio] = useState(null);
  const [newService, setNewService] = useState({
    name: '',
    description: '',
    detailedDescription: '',
    price: '',
    images: ['']
  });
  const [newPortfolioItem, setNewPortfolioItem] = useState({
    title: '',
    image: '',
    category: ''
  });
  const { toast } = useToast();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await adminAPI.login(loginData);
      
      if (response.success) {
        setIsAuthenticated(true);
        localStorage.setItem('isAdminAuthenticated', 'true');
        await fetchData();
        toast({
          title: "Успешный вход",
          description: "Добро пожаловать в админ-панель!",
        });
      } else {
        toast({
          title: "Ошибка входа",
          description: response.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка входа",
        description: errorInfo.message,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAdminAuthenticated');
    setLoginData({ login: '', password: '' });
  };

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
    } finally {
      setLoading(false);
    }
  };

  // Services management
  const handleEditService = (service) => {
    setEditingService({ ...service });
  };

  const handleSaveService = async () => {
    try {
      await servicesAPI.update(editingService.id, editingService);
      await fetchData();
      setEditingService(null);
      toast({
        title: "Услуга обновлена",
        description: "Изменения сохранены успешно!",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка сохранения",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  const handleDeleteService = async (id) => {
    try {
      await servicesAPI.delete(id);
      await fetchData();
      toast({
        title: "Услуга удалена",
        description: "Услуга была удалена из списка",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка удаления",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  const handleAddService = async () => {
    try {
      await servicesAPI.create(newService);
      await fetchData();
      setNewService({ name: '', description: '', detailedDescription: '', price: '', images: [''] });
      toast({
        title: "Услуга добавлена",
        description: "Новая услуга была добавлена успешно!",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка добавления",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  // Portfolio management
  const handleEditPortfolio = (item) => {
    setEditingPortfolio({ ...item });
  };

  const handleSavePortfolio = async () => {
    try {
      await portfolioAPI.update(editingPortfolio.id, editingPortfolio);
      await fetchData();
      setEditingPortfolio(null);
      toast({
        title: "Работа обновлена",
        description: "Изменения в портфолио сохранены!",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка сохранения",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  const handleDeletePortfolio = async (id) => {
    try {
      await portfolioAPI.delete(id);
      await fetchData();
      toast({
        title: "Работа удалена",
        description: "Работа была удалена из портфолио",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка удаления",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  const handleAddPortfolio = async () => {
    try {
      await portfolioAPI.create(newPortfolioItem);
      await fetchData();
      setNewPortfolioItem({ title: '', image: '', category: '' });
      toast({
        title: "Работа добавлена",
        description: "Новая работа была добавлена в портфолио!",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка добавления",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  // Contacts management
  const handleSaveContacts = async () => {
    try {
      await contactsAPI.update(contacts);
      toast({
        title: "Контакты обновлены",
        description: "Контактная информация успешно сохранена!",
      });
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast({
        title: "Ошибка сохранения",
        description: errorInfo.message,
        variant: "destructive",
      });
    }
  };

  // Check auth status on mount
  useEffect(() => {
    const authStatus = localStorage.getItem('isAdminAuthenticated');
    if (authStatus === 'true') {
      setIsAuthenticated(true);
      fetchData();
    }
  }, []);

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
                disabled={loading}
              />
              <Input
                type="password"
                placeholder="Пароль"
                value={loginData.password}
                onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                className="border-amber-200 focus:border-amber-500"
                disabled={loading}
              />
              <Button 
                type="submit" 
                className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700"
                disabled={loading}
              >
                {loading ? <Loader className="w-4 h-4 mr-2 animate-spin" /> : null}
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

        <Tabs defaultValue="services" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="services">Услуги</TabsTrigger>
            <TabsTrigger value="portfolio">Наши работы</TabsTrigger>
            <TabsTrigger value="contacts">Контакты</TabsTrigger>
          </TabsList>

          {/* Services Tab */}
          <TabsContent value="services">
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
                        placeholder="Краткое описание услуги"
                        value={newService.description}
                        onChange={(e) => setNewService({...newService, description: e.target.value})}
                      />
                      <Textarea
                        placeholder="Подробное описание услуги"
                        rows={4}
                        value={newService.detailedDescription}
                        onChange={(e) => setNewService({...newService, detailedDescription: e.target.value})}
                      />
                      <Input
                        placeholder="Цена (например: от 50 000 ₽)"
                        value={newService.price}
                        onChange={(e) => setNewService({...newService, price: e.target.value})}
                      />
                      <Input
                        placeholder="URL изображения"
                        value={newService.images[0] || ''}
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
                {loading ? (
                  <div className="text-center py-8">
                    <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-amber-600" />
                    <p className="text-amber-700">Загрузка услуг...</p>
                  </div>
                ) : (
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
                                    <Textarea
                                      placeholder="Подробное описание"
                                      rows={4}
                                      value={editingService.detailedDescription}
                                      onChange={(e) => setEditingService({...editingService, detailedDescription: e.target.value})}
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
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Portfolio Tab */}
          <TabsContent value="portfolio">
            <Card className="shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-xl text-amber-900">Управление портфолио</CardTitle>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button className="bg-green-600 hover:bg-green-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Добавить работу
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl">
                    <DialogHeader>
                      <DialogTitle>Добавить новую работу</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                      <Input
                        placeholder="Название работы"
                        value={newPortfolioItem.title}
                        onChange={(e) => setNewPortfolioItem({...newPortfolioItem, title: e.target.value})}
                      />
                      <Input
                        placeholder="Категория (например: Бани, Беседки, Мебель)"
                        value={newPortfolioItem.category}
                        onChange={(e) => setNewPortfolioItem({...newPortfolioItem, category: e.target.value})}
                      />
                      <Input
                        placeholder="URL изображения"
                        value={newPortfolioItem.image}
                        onChange={(e) => setNewPortfolioItem({...newPortfolioItem, image: e.target.value})}
                      />
                      <Button onClick={handleAddPortfolio} className="w-full">
                        Добавить работу
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-amber-600" />
                    <p className="text-amber-700">Загрузка портфолио...</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {portfolio.map((item) => (
                      <div key={item.id} className="border border-amber-200 rounded-lg p-4 bg-white">
                        <img 
                          src={item.image} 
                          alt={item.title}
                          className="w-full h-32 object-cover rounded mb-3"
                        />
                        <h3 className="font-semibold text-amber-900">{item.title}</h3>
                        <p className="text-sm text-gray-600">{item.category}</p>
                        <div className="flex space-x-2 mt-3">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => handleEditPortfolio(item)}
                              >
                                <Edit className="w-4 h-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-2xl">
                              <DialogHeader>
                                <DialogTitle>Редактировать работу</DialogTitle>
                              </DialogHeader>
                              {editingPortfolio && (
                                <div className="space-y-4">
                                  <Input
                                    value={editingPortfolio.title}
                                    onChange={(e) => setEditingPortfolio({...editingPortfolio, title: e.target.value})}
                                  />
                                  <Input
                                    value={editingPortfolio.category}
                                    onChange={(e) => setEditingPortfolio({...editingPortfolio, category: e.target.value})}
                                  />
                                  <Input
                                    value={editingPortfolio.image}
                                    onChange={(e) => setEditingPortfolio({...editingPortfolio, image: e.target.value})}
                                  />
                                  <Button onClick={handleSavePortfolio} className="w-full">
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
                            onClick={() => handleDeletePortfolio(item.id)}
                            className="border-red-500 text-red-600 hover:bg-red-50"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Contacts Tab */}
          <TabsContent value="contacts">
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-xl text-amber-900">Управление контактами</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-amber-600" />
                    <p className="text-amber-700">Загрузка контактов...</p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-amber-900 mb-2">
                          <Phone className="w-4 h-4 inline mr-1" />
                          Телефон
                        </label>
                        <Input
                          value={contacts.phone || ''}
                          onChange={(e) => setContacts({...contacts, phone: e.target.value})}
                          placeholder="+7 (999) 123-45-67"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-amber-900 mb-2">
                          <Phone className="w-4 h-4 inline mr-1" />
                          WhatsApp (без +)
                        </label>
                        <Input
                          value={contacts.whatsapp || ''}
                          onChange={(e) => setContacts({...contacts, whatsapp: e.target.value})}
                          placeholder="79991234567"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-amber-900 mb-2">
                        <Mail className="w-4 h-4 inline mr-1" />
                        Email
                      </label>
                      <Input
                        value={contacts.email || ''}
                        onChange={(e) => setContacts({...contacts, email: e.target.value})}
                        placeholder="info@knyazhiy-terem.ru"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-amber-900 mb-2">
                        Название компании
                      </label>
                      <Input
                        value={contacts.name || ''}
                        onChange={(e) => setContacts({...contacts, name: e.target.value})}
                        placeholder="Княжий Терем"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-amber-900 mb-2">
                        Слоган
                      </label>
                      <Input
                        value={contacts.tagline || ''}
                        onChange={(e) => setContacts({...contacts, tagline: e.target.value})}
                        placeholder="Мастера чистовой отделки деревом"
                      />
                    </div>
                    
                    <Button onClick={handleSaveContacts} className="w-full">
                      <Save className="w-4 h-4 mr-2" />
                      Сохранить контакты
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminPage;
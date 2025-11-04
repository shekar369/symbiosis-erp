import React, { createContext, useContext, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchApi } from '../utils/api';

const ConfigContext = createContext(null);

export const ConfigProvider = ({ children }) => {
  const { data: configs, isLoading } = useQuery({
    queryKey: ['configurations'],
    queryFn: () => fetchApi('/config'),
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
    retry: false,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    enabled: Boolean(localStorage.getItem('accessToken')), // Only fetch if authenticated
  });

  const getConfigValue = (key) => {
    const config = configs?.find((c) => c.key === key);
    return config?.value;
  };

  const getConfigByCategory = (category) => {
    return configs?.filter((c) => c.category === category) || [];
  };

  const value = {
    configs,
    isLoading,
    getConfigValue,
    getConfigByCategory,
  };

  return (
    <ConfigContext.Provider value={value}>
      {children}
    </ConfigContext.Provider>
  );
};

export const useConfig = () => {
  const context = useContext(ConfigContext);
  if (!context) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
};
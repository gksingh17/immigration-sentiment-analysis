import React, { useState } from 'react';
import { styled } from '@mui/system';
import URLInput from './URLInput';

const AppContainer = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  backgroundColor: '#f2f2f2',
});

const AppTitle = styled('h1')({
  fontSize: '28px',
  fontWeight: 'bold',
  marginBottom: '20px',
  color: '#333',
});

const App = () => {
  const handleURLSubmit = (url) => {
    // Simulate processing the URL
    console.log('Fetching URL:', url);
    // perform any other logic or API calls here
  };

  return (
    <AppContainer>
      <AppTitle>URL Input</AppTitle>
      <URLInput onURLSubmit={handleURLSubmit} />
    </AppContainer>
  );
};

export default App;
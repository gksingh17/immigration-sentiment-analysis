import React from 'react';
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

const AppTitle = styled('h3')({
  fontSize: '28px',
  fontWeight: 'bold',
  marginBottom: '20px',
  color: '#333',
});

const App = () => {
  return (
    <AppContainer>
      <AppTitle>URL Input</AppTitle>
      <URLInput />
    </AppContainer>
  );
};

export default App;
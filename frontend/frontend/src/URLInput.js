import React, { useState } from 'react';
import { styled } from '@mui/system';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const RootContainer = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: '16px',
  padding: '200px', 
  borderRadius: '8px',
  boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#f7f7f7',
  width: '500px', /* width */
});

const useStyles = () => ({
  textField: {
    width: '100%',
  },
  button: {
    fontWeight: 'bold',
    fontSize: '16px', //font size 
  },
  errorText: {
    color: 'red',
    fontSize: '14px',
  },
  animationContainer: {
    width: '48px',
    height: '48px',
    borderRadius: '50%',
    border: '4px solid rgba(0, 0, 0, 0.1)',
    borderTopColor: '#3f51b5',
    animation: 'spin 1s linear infinite',
  },
  animation: {
    '@keyframes spin': {
      from: { transform: 'rotate(0deg)' },
      to: { transform: 'rotate(360deg)' },
    },
  },
});

const URLInput = ({ onURLSubmit }) => {
  const classes = useStyles();
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setUrl(e.target.value);
    setError('');
  };

  const handleSubmit = () => {
    if (url.trim() === '') {
      setError('Please enter a URL');
    } else if (!isValidUrl(url)) {
      setError('Please enter a valid URL');
    } else {
      setIsLoading(true);
      // Simulate loading delay
      setTimeout(() => {
        setIsLoading(false);
        onURLSubmit(url);
      }, 2000);
    }
  };

  const isValidUrl = (url) => {
    // Regex pattern for URL validation
    const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
    return urlRegex.test(url);
  };

  return (
    <RootContainer>
      <TextField
        label="Enter a URL"
        variant="outlined"
        size="medium"
        className={classes.textField}
        value={url}
        onChange={handleInputChange}
        error={!!error}
        helperText={error}
        inputProps={{ style: { textAlign: 'center' } }}
      />
      <Button
        variant="contained"
        color="primary"
        className={classes.button}
        onClick={handleSubmit}
        disabled={isLoading}
      >
        {isLoading ? 'Loading...' : 'Submit'}
      </Button>
      {isLoading && (
        <div className={classes.animationContainer}>
          <div className={classes.animation} />
        </div>
      )}
    </RootContainer>
  );
};

export default URLInput;
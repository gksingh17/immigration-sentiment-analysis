import React, { useState } from 'react';
import { styled } from '@mui/system';
import { TextField, Button, CircularProgress, Alert, AlertTitle, Stack } from '@mui/material';


const RootContainer = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: '16px',
  padding: '300px',
  borderRadius: '8px',
  boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#f7f7f7',
  width: '800px',
});

const useStyles = () => ({
  textField: {
    width: '100%',
  },
  button: {
    fontWeight: 'bold',
    fontSize: '18px',
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
  alertContainer: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
  },
  alert: {
    width: '500px',
  },
});

const URLInput = ({ onURLSubmit }) => {
  const classes = useStyles();
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [isValid, setIsValid] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [successAlertOpen, setSuccessAlertOpen] = useState(false);
  const [errorAlertOpen, setErrorAlertOpen] = useState(false);

  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    setUrl(inputValue);
    setIsValid(isValidUrl(inputValue));
    setError('');
  };

  const handleSubmit = () => {
    if (url.trim() === '') {
      setError('Please enter a URL');
    } else if (!isValid) {
      setError('Please enter a valid URL');
    } else {
      setIsLoading(true);
      // Simulate loading delay
      setTimeout(() => {
        setIsLoading(false);
        setSuccessAlertOpen(true);
        onURLSubmit(url);
      }, 2000);
    }
  };

  const handleCloseAlerts = () => {
    setSuccessAlertOpen(false);
    setErrorAlertOpen(false);
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
        size="large"
        fullWidth
        className={`${classes.textField} ${isValid ? classes.validUrl : ''}`}
        value={url}
        onChange={handleInputChange}
        error={!!error}
        helperText={error}
        inputProps={{ style: { textAlign: 'center' } }}
      />
      <Button
        variant="contained"
        color="primary"
        size="large"
        className={classes.button}
        onClick={handleSubmit}
        disabled={isLoading}
      >
        {isLoading ? (
          <div className={classes.animationContainer}>
            <CircularProgress size={24} />
          </div>
        ) : (
          'Submit'
        )}
      </Button>
      <div className={classes.alertContainer}>
        <Stack spacing={6} className={classes.alert}>
          <Alert
            severity="success"
            onClose={handleCloseAlerts}
            sx={{ display: successAlertOpen ? 'block' : 'none' }}
          >
            <AlertTitle>Success</AlertTitle>
            URL Submitted Successfully!
          </Alert>
          <Alert
            severity="error"
            onClose={handleCloseAlerts}
            sx={{ display: errorAlertOpen ? 'block' : 'none' }}
          >
            <AlertTitle>Error</AlertTitle>
            Error Submitting URL!
          </Alert>
        </Stack>
      </div>
    </RootContainer>
  );
};

export default URLInput;
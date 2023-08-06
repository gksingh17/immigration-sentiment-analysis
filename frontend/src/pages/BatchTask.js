import React, { useState } from "react";
import axios from "axios";
import { Helmet } from 'react-helmet-async';
import { TextField, Button, Typography, Container, Box, Grid, Chip } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";
import { deepOrange, deepPurple, green, blue, red, yellow, teal } from "@mui/material/colors";

export default function BatchTask() {
  
  const [tag, setTag] = useState(""); 

  const colorMap = {
    irish: deepOrange[500],
    immigration: deepPurple[500],
    protest: green[500],
    rightwing: blue[500],
    leftwing: red[500],
    irelandisfull: yellow[600],
    ireland: teal[500]
  };

  const handleSubmit = async (e) => {
    setTag(e.target.value)
    try {
      console.log("Sending keyword:", tag);

      const apiUrl = `${process.env.REACT_APP_NLP_PLATFORM_API_URL}/api/batch`;
      const response = await axios.post(apiUrl, { topic: tag });

      console.log("Response from server:", response.data);
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  return (
    <Container component="main" maxWidth="md">
      <Helmet>
        <title> About our system | Minimal UI </title>
      </Helmet>
      <Typography variant="h4" sx={{ mb: 5 }}>
      Batch Configuration
      </Typography>
      <Box display="flex" flexDirection="column" alignItems="center" marginTop={4}>
        
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={9}>
            {/* <Autocomplete
              id="tags-input"
              options={Object.keys(colorMap)}
              freeSolo
              value={tag}

              onChange={(event, newValue, reason) => {
                // if (reason === "clear") {
                //   // setTag("");
                // } else if (reason === "select-option" || reason === "create-option") {
                //   setTag(newValue);
                // }
                setTag(event.target.value)
              }}
              
              renderTags={(value, getTagProps) =>
                value ? (
                  <Chip
                    variant="filled"
                    label={value}
                    {...getTagProps({ index: 0 })}
                    style={{ backgroundColor: colorMap[value] || blue[200] }}
                  />
                ) : null
              }
              renderInput={(params) => (
                <TextField
                  {...params}
                  fullWidth
                  variant="outlined"
                  label="Keyword"
                  placeholder="Add keyword"
                />
              )}
            /> */}
          <TextField id="outlined-basic" label="Add Keyword" variant="outlined" 
          style={{ width: '100%' }}
           onChange={(event) => {setTag(event.target.value)}
          }/>
          </Grid>
          <Grid item xs={3}>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handleSubmit}
              
            >
              Submit
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}
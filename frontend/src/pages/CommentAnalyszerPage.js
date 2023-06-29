import React, { useState } from 'react';
import { TextField, Button, FormControl, Select, InputLabel, MenuItem } from '@mui/material';
import MyBarChart from '../components/chart/BarChart';

export default function CommentanalyzerPage() {
  const [url, setUrl] = useState('');
  const [numComments, setNumComments] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh' }}>
      <form onSubmit={handleSubmit}
            style={{ display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center',
                gap: '1rem', width: '50%' }}
      >
        <TextField
          label="Enter a URL"
          value={url}
          style={{ width: '50%' }}
          onChange={(e) => setUrl(e.target.value)}
        />
        <FormControl style={{ width: '10%' }}>
          <InputLabel>Number of Comments</InputLabel>
          <Select
            value={numComments}
            onChange={(e) => setNumComments(e.target.value)}
          >
            <MenuItem value={50}>50</MenuItem>
            <MenuItem value={100}>100</MenuItem>
            <MenuItem value={200}>200</MenuItem>
          </Select>
        </FormControl>
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>
      <br/>
      <br/>
      {submitted && <MyBarChart url={url} number={numComments} />}
    </div>
  );
}

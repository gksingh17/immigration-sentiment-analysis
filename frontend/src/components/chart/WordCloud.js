/* eslint-disable */

import React, { useEffect, useState } from 'react';
import { Card, CardHeader, Box, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { TagCloud } from 'react-tagcloud';

function WordCloud({word_cloud_data, title, subheader, ...other }) {
  const [selectedTopic, setSelectedTopic] = useState(word_cloud_data[0]?.id || []);
  const [selectedWords, setSelectedWords] = useState([]);

  const handleTopicChange = (event) => {
    setSelectedTopic(parseInt(event.target.value));
  };

  useEffect(() => {
    setSelectedWords(word_cloud_data.find((topic) => topic.id === selectedTopic)?.words || []);
  });

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} />
      <Box sx={{ p: 3, pb: 1 }} dir="ltr">
        <FormControl variant="standard">
          <InputLabel id="topic-dropdown-label">Select a topic</InputLabel>
          <Select
            labelId="topic-dropdown-label"
            id="topicDropdown"
            value={selectedTopic}
            onChange={handleTopicChange}
            label="Select a topic"
          >
            {word_cloud_data.map((topic) => (
              <MenuItem key={topic.id} value={topic.id}>
                {topic.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <div className="word-cloud-container" style={{ marginTop: '20px' }}>
          <TagCloud minSize={25} maxSize={70} tags={selectedWords} className="tag-cloud" />
        </div>
      </Box>
    </Card>
  );
}

export default WordCloud;
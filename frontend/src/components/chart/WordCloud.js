/* eslint-disable */

import React, { useEffect, useState } from 'react';
import { Card, CardHeader, Box, Tabs, Tab } from '@mui/material';
import { TagCloud } from 'react-tagcloud';

function WordCloud({word_cloud_data, title, subheader, ...other }) {
  const [selectedTopic, setSelectedTopic] = useState(word_cloud_data[0]?.id || []);
  const [selectedWords, setSelectedWords] = useState([]);

  const handleTopicChange = (event, newValue) => {
    setSelectedTopic(newValue);
  };

  useEffect(() => {
    setSelectedWords(word_cloud_data.find((topic) => topic.id === Number(selectedTopic))?.words || []);
  }, [selectedTopic, word_cloud_data]);

  return (
    <Card {...other} sx={{width: '100%', height: '40vh'}}>
      <CardHeader title={title} subheader={subheader} />
      <Box sx={{ p: 3, pb: 1 }} dir="ltr">
        <Tabs
          value={selectedTopic}
          onChange={handleTopicChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          sx={{ marginLeft: '-20px' }} 
        >
          {word_cloud_data.map((topic) => (
            <Tab key={topic.id} value={topic.id} label={topic.name} />
          ))}
        </Tabs>
        <div className="word-cloud-container" style={{ marginTop: '20px' }}>
          <TagCloud minSize={25} maxSize={70} tags={selectedWords} className="tag-cloud" />
        </div>
      </Box>
    </Card>
  );
}

export default WordCloud; 
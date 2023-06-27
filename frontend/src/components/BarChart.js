import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Spinner } from 'react-bootstrap';


const MyBarChart = ({ url, number }) => {
  const [chartData, setChartData] = useState([]);
  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#FF8042', '#0088FE'];

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch('http://0.0.0.0:5000/api/comments', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: url, number: number }),
        });

        const data = await response.json();

        let transformedData = data.map(item => ({
          label: item.label,
          value: item.ratio,
        }));

        console.log(transformedData);

        setChartData(transformedData);

      } catch (error) {
        console.error('Error:', error);
      } finally {
      }
    };

    fetchChartData();
  }, [url, number]);


  return (
    <div>
      {!chartData ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Spinner animation="border" />
        </div>
      ) : (
      <BarChart
        width={500}
        height={300}
        data={chartData}
        margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
      )}
    </div>
  );
};

export default MyBarChart;
